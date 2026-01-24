from moviepy.editor import VideoFileClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import textwrap
import emoji

def split_text_emoji(text):
    """Split text into segments of regular text and emojis"""
    emojis = emoji.emoji_list(text)
    segments = []
    last_end = 0
    for e in emojis:
        if e['match_start'] > last_end:
            segments.append((text[last_end:e['match_start']], False))
        segments.append((e['emoji'], True))
        last_end = e['match_end']
    if last_end < len(text):
        segments.append((text[last_end:], False))
    return segments

def create_text_overlay(text, config):
    """
    Create a text overlay image tightly around text
    with rounded rectangle, shadow, padding, emoji support,
    and proper line height.
    """

    # Load fonts
    font = ImageFont.truetype(config.FONT_PATH, config.FONT_SIZE)

    try:
        emoji_font_sizes = [136, 109, 72, 56, 40, 32, 28, 24, 20]
        target_size = int(config.FONT_SIZE * 0.95)
        closest_size = min(emoji_font_sizes, key=lambda x: abs(x - target_size))

        font_emoji = ImageFont.truetype(
            config.EMOJI_FONT_PATH,
            closest_size
        )
    except Exception:
        font_emoji = font

    # Wrap text
    lines = textwrap.wrap(text, width=config.MAX_CHARS_PER_LINE)

    # Measure text
    line_widths = []
    line_heights = []

    for line in lines:
        segments = split_text_emoji(line)
        total_w = 0
        max_h = 0

        for part, is_emoji in segments:
            bbox = (
                font_emoji.getbbox(part)
                if is_emoji
                else font.getbbox(part)
            )
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            total_w += w
            max_h = max(max_h, h)

        # Apply line height multiplier
        line_height = int(max_h * config.LINE_HEIGHT_MULTIPLIER)

        line_widths.append(total_w)
        line_heights.append(line_height)

    # Box size
    box_w = max(line_widths) + config.PADDING_X * 2
    box_h = sum(line_heights) + config.PADDING_Y * 2

    shadow_space = config.SHADOW_BLUR + config.SHADOW_OFFSET

    # Base image
    img = Image.new(
        "RGBA",
        (box_w + shadow_space * 2, box_h + shadow_space * 2),
        (0, 0, 0, 0)
    )

    x = shadow_space
    y = shadow_space

    # Shadow
    shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.rounded_rectangle(
        [
            (x + config.SHADOW_OFFSET, y + config.SHADOW_OFFSET),
            (x + box_w + config.SHADOW_OFFSET, y + box_h + config.SHADOW_OFFSET),
        ],
        radius=config.BORDER_RADIUS,
        fill=(0, 0, 0, 80),
    )
    shadow_layer = shadow_layer.filter(
        ImageFilter.GaussianBlur(config.SHADOW_BLUR)
    )

    # Background
    bg_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg_layer)
    bg_draw.rounded_rectangle(
        [(x, y), (x + box_w, y + box_h)],
        radius=config.BORDER_RADIUS,
        fill=config.BG_COLOR,
    )

    # Composite
    img = Image.alpha_composite(img, shadow_layer)
    img = Image.alpha_composite(img, bg_layer)

    draw = ImageDraw.Draw(img)

    # Draw text
    current_y = y + config.PADDING_Y

    for i, line in enumerate(lines):
        text_x = x + (box_w - line_widths[i]) // 2
        current_x = text_x

        segments = split_text_emoji(line)

        for part, is_emoji in segments:
            bbox = (
                font_emoji.getbbox(part)
                if is_emoji
                else font.getbbox(part)
            )
            w = bbox[2] - bbox[0]

            draw.text(
                (current_x, current_y),
                part,
                font=font_emoji if is_emoji else font,
                fill=config.TEXT_COLOR,
            )

            current_x += w

        current_y += line_heights[i]

    return img

def create_video(overlay_text, config):
    """Create video with text overlay and music"""
    # Load video
    video = VideoFileClip(config.VIDEO_TEMPLATE)

    # Load and process audio
    audio = AudioFileClip(config.MUSIC_FILE) \
            .subclip(0, video.duration) \
            .volumex(config.AUDIO_VOLUME) \
            .set_fps(44100)

    # Create text overlay
    main_overlay = create_text_overlay(overlay_text, config)

    caption_text = "Read caption and Save Reel for Upcoming Interviews 👇"

    caption_overlay = create_text_overlay(caption_text, config)


    def add_text(get_frame, t):
        frame = get_frame(t)
        pil_im = Image.fromarray(frame)

        # Center position
        center_x = pil_im.width // 2
        center_y = pil_im.height // 2

        # Main overlay (only for first 10 seconds) at center
        if t < 5:
            top_x = center_x - main_overlay.width // 2
            top_y = center_y - main_overlay.height // 2
            pil_im.paste(main_overlay, (top_x, top_y), main_overlay)

        # Caption overlay after 10 seconds at center
        if t >= 5:
            caption_x = center_x - caption_overlay.width // 2
            caption_y = center_y - caption_overlay.height // 2
            pil_im.paste(caption_overlay, (caption_x, caption_y), caption_overlay)

        return np.array(pil_im)

    video_with_text = video.fl(add_text)
    final_video = video_with_text.set_audio(audio)

    # Export video
    final_video.write_videofile(
        config.OUTPUT_VIDEO,
        fps=config.VIDEO_FPS,
        codec="libx264",
        audio_codec="aac",
        audio_bitrate=config.AUDIO_BITRATE,
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )

    print(f"Video created: {config.OUTPUT_VIDEO}")
    print(f"Duration: {final_video.duration}s")
    print(f"Has audio: {final_video.audio is not None}")

    return config.OUTPUT_VIDEO