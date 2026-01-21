from moviepy.editor import VideoFileClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import textwrap

def create_text_overlay(text, config):
    """
    Create a text overlay image tightly around text with rounded rectangle, shadow, and padding
    """
    font = ImageFont.truetype(config.FONT_PATH, config.FONT_SIZE)

    # Wrap text into multiple lines
    lines = textwrap.wrap(text, width=config.MAX_CHARS_PER_LINE)

    # Measure text size
    line_widths = []
    line_heights = []
    for line in lines:
        bbox = font.getbbox(line)
        line_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1]
        line_widths.append(line_w)
        line_heights.append(line_h)

    # Box size including padding
    box_w = max(line_widths) + config.PADDING_X * 2
    line_spacing = 5
    box_h = sum(line_heights) + config.PADDING_Y * 2 + (len(lines) - 1) * line_spacing

    shadow_space = config.SHADOW_BLUR + config.SHADOW_OFFSET

    # Create image just large enough to hold box + shadow
    img = Image.new("RGBA", (box_w + shadow_space * 2, box_h + shadow_space * 2), (0, 0, 0, 0))

    x = shadow_space
    y = shadow_space

    # Draw shadow
    shadow_layer = Image.new("RGBA", img.size, (0,0,0,0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.rounded_rectangle(
        [(x + config.SHADOW_OFFSET, y + config.SHADOW_OFFSET),
         (x + box_w + config.SHADOW_OFFSET, y + box_h + config.SHADOW_OFFSET)],
        radius=config.BORDER_RADIUS,
        fill=(0,0,0,80)
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(config.SHADOW_BLUR))

    # Draw background rectangle
    bg_layer = Image.new("RGBA", img.size, (0,0,0,0))
    bg_draw = ImageDraw.Draw(bg_layer)
    bg_draw.rounded_rectangle([(x,y),(x+box_w,y+box_h)], radius=config.BORDER_RADIUS, fill=config.BG_COLOR)

    # Composite shadow + background
    img = Image.alpha_composite(img, shadow_layer)
    img = Image.alpha_composite(img, bg_layer)

    # CREATE NEW DRAW OBJECT AFTER COMPOSITING
    draw = ImageDraw.Draw(img)

    # Draw text centered
    current_y = y + config.PADDING_Y
    for i, line in enumerate(lines):
        text_w = line_widths[i]
        text_x = x + (box_w - text_w)//2
        draw.text((text_x, current_y), line, font=font, fill=config.TEXT_COLOR)
        current_y += line_heights[i] + line_spacing

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

    caption_text = "Read caption below"

    caption_overlay = create_text_overlay(caption_text, config)


    def add_text(get_frame, t):
        frame = get_frame(t)
        pil_im = Image.fromarray(frame)

        # Center position
        center_x = pil_im.width // 2
        center_y = pil_im.height // 2

        # Main overlay (only for first 5 seconds) at center
        if t < 5:
            top_x = center_x - main_overlay.width // 2
            top_y = center_y - main_overlay.height // 2
            pil_im.paste(main_overlay, (top_x, top_y), main_overlay)

        # Caption overlay after 5 seconds at center
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