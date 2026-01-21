# InstaReelBot

A simple bot that automates creating and posting Instagram Reels. It generates videos, uploads them to Cloudinary, and posts to Instagram with notifications via Twilio.

## What It Does

- Creates short videos for Instagram Reels
- Uploads videos to Cloudinary for storage
- Posts reels to Instagram automatically
- Sends SMS notifications about the process using Twilio

## Basic Requirements

- Python 3.8 or higher
- API keys for:
  - Instagram (for posting)
  - Cloudinary (for video storage)
  - Twilio (for SMS notifications)
- Virtual environment (recommended)

## Environment Setup

1. **Clone or download the project** to your local machine.
 ```bash
   git clone https://github.com/sridevi14/InstaReelBot.git
   cd InstaReelBot
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   Create a `.env` file in the project root with your API keys:
   ```
   INSTAGRAM_ACCESS_TOKEN=your_instagram_token
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=your_twilio_number
   NOTIFICATION_PHONE_NUMBER=your_phone_number
   ```

6. **Run the bot**:
   ```
   python main.py
   ```

## Support

If you like this project, you can support it:

☕ [Buy me a coffee](https://buymeacoffee.com/sridevimanju)
### Connect with me

📸 [Follow me on Instagram](https://www.instagram.com/sridevi.tech)
## License

MIT License – free to use, modify, and distribute.
