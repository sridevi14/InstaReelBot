from moviepy.editor import VideoFileClip,AudioFileClip
import pandas as pd
from instagrapi import Client
from datetime import date
from PIL import Image, ImageDraw, ImageFont,ImageFilter
import numpy as np
import textwrap
import re
from instagrapi import Client

# ENV
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("IG_USERNAME")

print("USERNAME:", os.getenv("IG_USERNAME"))
PASSWORD = os.getenv("IG_PASSWORD")
print("PASSWORD:", os.getenv("IG_PASSWORD"))

GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

print("GOOGLE_SHEET_URL:", os.getenv("GOOGLE_SHEET_URL"))


if not USERNAME or not PASSWORD or GOOGLE_SHEET_URL:
    raise ValueError("Instagram credentials or GOOGLE_SHEET_URL not found in environment variables")
# ---------- CONFIG ----------
VIDEO_TEMPLATE = "template.mp4"
OUTPUT_VIDEO = "output.mp4"



def load_google_sheet(url):
    sheet_id = re.search(r"/d/([a-zA-Z0-9-_]+)", url).group(1)
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(csv_url)

# ---------- READ EXCEL ----------
df = load_google_sheet(GOOGLE_SHEET_URL)
df["Date"] = pd.to_datetime(df["Date"]).dt.date
today = date.today()

today_rows = df[df["Date"] == today]
if today_rows.empty:
    print("No content found for today:", today)
    exit()

row = today_rows.iloc[0]
overlay_text = str(row["OverlayText"])
caption = str(row["Caption"])


# ---------- LOAD VIDEO ----------
video = VideoFileClip(VIDEO_TEMPLATE)
audio = AudioFileClip("music.mp3") \
        .subclip(0, video.duration) \
        .volumex(0.7) \
        .set_fps(44100)


w, h = video.size

# ---------- STYLE SETTINGS ----------
border_radius = 25           # Rounded corner radius
bg_color = (255, 255, 255, 240)  # White with slight transparency
shadow_offset = 8            # Shadow distance
shadow_blur = 15             # Shadow blur radius
text_color = "black"
font_size = 60
padding_x = 50
padding_y = 40

# ---------- CREATE TEXT OVERLAY IMAGE ----------
# Create image larger to accommodate shadow
shadow_space = shadow_blur + shadow_offset
img = Image.new("RGBA", (w + shadow_space * 2, h + shadow_space * 2), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype("arialbd.ttf", font_size)

# Wrap text
max_chars_per_line = 25
lines = textwrap.wrap(overlay_text, width=max_chars_per_line)

# Calculate box size
line_heights = []
line_widths = []
for line in lines:
    bbox = draw.textbbox((0, 0), line, font=font)
    line_w = bbox[2] - bbox[0]
    line_h = bbox[3] - bbox[1]
    line_widths.append(line_w)
    line_heights.append(line_h)

box_w = max(line_widths) + padding_x * 2
box_h = sum(line_heights) + padding_y * 2 + (len(lines) - 1) * 10

# Position (accounting for shadow space)
x = (w - box_w) // 2 + shadow_space
y = (h - box_h) // 2 + shadow_space

# ---------- DRAW SHADOW ----------
shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow_layer)
shadow_draw.rounded_rectangle(
    [(x + shadow_offset, y + shadow_offset),
     (x + box_w + shadow_offset, y + box_h + shadow_offset)],
    radius=border_radius,
    fill=(0, 0, 0, 80)  # Semi-transparent black
)
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))

# ---------- DRAW ROUNDED RECTANGLE BACKGROUND ----------
bg_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
bg_draw = ImageDraw.Draw(bg_layer)
bg_draw.rounded_rectangle(
    [(x, y), (x + box_w, y + box_h)],
    radius=border_radius,
    fill=bg_color
)

# Composite shadow and background
img = Image.alpha_composite(img, shadow_layer)
img = Image.alpha_composite(img, bg_layer)

# ---------- DRAW TEXT ----------
draw = ImageDraw.Draw(img)
current_y = y + padding_y
for i, line in enumerate(lines):
    # Center each line
    bbox = draw.textbbox((0, 0), line, font=font)
    line_w = bbox[2] - bbox[0]
    text_x = x + (box_w - line_w) // 2

    draw.text(
        (text_x, current_y),
        line,
        font=font,
        fill=text_color
    )
    current_y += line_heights[i] + 10

# Crop back to original size (remove shadow space)
img = img.crop((shadow_space, shadow_space, w + shadow_space, h + shadow_space))

# ---------- APPLY OVERLAY ON EACH FRAME ----------
def add_text(get_frame, t):
    frame = get_frame(t)
    pil_im = Image.fromarray(frame)
    pil_im.paste(img, (0, 0), img)
    return np.array(pil_im)

video_with_text = video.fl(add_text)
final_video = video_with_text.set_audio(audio)
# ---------- EXPORT ----------
final_video.write_videofile(
    OUTPUT_VIDEO,
    fps=24,
    codec="libx264",
    audio_codec="aac",
    audio_bitrate="192k",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True
)

print("Final duration:", final_video.duration)
print("Has audio:", final_video.audio is not None)
# ---------- UPLOAD TO INSTAGRAM ----------
# Login
cl = Client()
cl.login(USERNAME, PASSWORD)

# Upload photo
photo_path = "output.mp4"
cl.video_upload(photo_path, caption)

print("Upload successful!")


