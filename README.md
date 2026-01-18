# 📹 InstaReelBot – Automated Instagram Video Poster with WhatsApp Notification

## Overview

InstaReelBot is a Python automation tool that:

- Fetches content (overlay text + caption) for today from a Google Sheet
- Generates a video by overlaying styled text on a video template
- Uploads the video to Instagram automatically
- Sends a WhatsApp notification with the post link after upload

This enables fully automated Instagram posting for daily content with minimal effort.

## Features

- ✅ Fetch required data from Google Sheet
- ✅ Add rounded, shadowed, wrapped overlay text to video
- ✅ Sync background music to video duration
- ✅ Upload video to Instagram with caption
- ✅ Send WhatsApp notification with post link

## Demo

Here's an example of the generated video with overlay text:

[🎥 View Example Video](https://res.cloudinary.com/dgjarosa2/video/upload/v1768711347/output_nvjihq.mp4)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sridevi14/InstaReelBot.git
   cd InstaReelBot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

- moviepy
- pandas
- Pillow
- numpy
- instagrapi
- twilio
- python-dotenv

## Configuration

1. **Create a `.env` file in the project root with the following variables:**

   ```env
   IG_USERNAME=your_instagram_username
   IG_PASSWORD=your_instagram_password
   IG_SESSION=base64_instagram_session
   GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/...
   TWILIO_SID=ACxxxxxxxxxxxxxxxx
   TWILIO_TOKEN=xxxxxxxxxxxx
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   TWILIO_WHATSAPP_TO=whatsapp:+91XXXXXXXXXX
   ```

   > **Tip:** Join the Twilio Sandbox from your personal WhatsApp to receive messages.

2. **Add Assets**

   Place these files in the project root:

   - `template.mp4` → Video template
   - `music.mp3` → Background music
   - `fonts/Roboto-Bold.ttf` → Font for overlay

## Usage

Run the bot:

```bash
python main.py
```

### What happens:

1. Reads today's row from Google Sheet (OverlayText + Caption)
2. Generates a video with overlay text and background music
3. Uploads the video to Instagram using the saved session
4. Sends WhatsApp notification with post URL:

   ```
   ✅ Instagram video posted successfully!
   📅 2026-01-18
   🔗 https://www.instagram.com/p/XXXXXXXXX/
   ```

## File Structure

```
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
```

## Support

If you like this project, you can support it:

☕ [Buy me a coffee](https://www.buymeacoffee.com/yourusername)

## License

MIT License – free to use, modify, and distribute.
