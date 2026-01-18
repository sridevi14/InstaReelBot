📹 InstaReelBot – Automated Instagram Video Poster with WhatsApp Notification

Overview

InstaReelBot is a Python automation tool that:

Fetches the content (overlay text + caption) for today from a Google Sheet

Generates a video by overlaying styled text on a video template

Uploads the video to Instagram automatically

Sends a WhatsApp notification with the post link after upload

This enables fully automated Instagram posting for daily content with minimal effort.

Features

✅ Fetch required data from Google Sheet

✅ Add rounded, shadowed, wrapped overlay text to video

✅ Sync background music to video duration

✅ Upload video to Instagram with caption

✅ Send WhatsApp notification with post link

Example

Overlay Preview →

Final uploaded video → You can add your video file or a link here, e.g., [output.mp4](example_video.mp4)

WhatsApp notification screenshot → optional: add image like [WhatsApp Screenshot](example_whatsapp.png)

✅ Make sure your images/videos are hosted online (Cloudinary, GitHub, etc.) or include locally in repo. Your URL above is fine if accessible publicly.

Setup
1️⃣ Install Python dependencies
git clone https://github.com/yourusername/InstaReelBot.git
cd InstaReelBot
python -m venv venv
# Activate virtual environment
venv\Scripts\activate   # Windows
# or
source venv/bin/activate # macOS/Linux
pip install -r requirements.txt


Dependencies include:

moviepy
pandas
Pillow
numpy
instagrapi
twilio
python-dotenv

2️⃣ Configure environment variables

Create a .env file in project root:

IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
IG_SESSION=base64_instagram_session
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/...
TWILIO_SID=ACxxxxxxxxxxxxxxxx
TWILIO_TOKEN=xxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+91XXXXXXXXXX


Tip: Join Twilio Sandbox from your personal WhatsApp to receive messages.

3️⃣ Add Assets

Place these files in the project root:

template.mp4 → Video template

music.mp3 → Background music

fonts/Roboto-Bold.ttf → Font for overlay

Usage

Run the bot:

python main.py


What happens:

Reads today’s row from Google Sheet (OverlayText + Caption)

Generates a video with overlay text and background music

Uploads the video to Instagram using the saved session

Sends WhatsApp notification with post URL:

✅ Instagram video posted successfully!
📅 2026-01-18
🔗 https://www.instagram.com/p/XXXXXXXXX/

File Structure
InstaReelBot/
│
├─ fonts/
│   └─ Roboto-Bold.ttf
├─ template.mp4
├─ music.mp3
├─ main.py
├─ requirements.txt
├─ .env
└─ README.md

Optional: Support / Buy Me a Coffee

If you like this project, you can support it:
☕ Buy me a coffee

License

MIT License – free to use, modify, and distribute.
