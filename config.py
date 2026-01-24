import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""

    # Google Sheets
    GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

    # Instagram
    ACCOUNT_ID = os.getenv("ACCOUNT_ID")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

    # Twilio
    TWILIO_SID = os.getenv("TWILIO_SID")
    TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
    TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
    TWILIO_WHATSAPP_TO = os.getenv("TWILIO_WHATSAPP_TO")

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    VIDEO_TEMPLATE = os.path.join(BASE_DIR, "template.mp4")
    OUTPUT_VIDEO = os.path.join(BASE_DIR, "output.mp4")
    FONT_PATH = os.path.join(BASE_DIR, "fonts", "Roboto-Bold.ttf")
    EMOJI_FONT_PATH = os.path.join(BASE_DIR, "fonts", "emoji.ttf")

    MUSIC_FILE = os.path.join(BASE_DIR, "music.mp3")

    # Video settings
    VIDEO_FPS = 24
    AUDIO_BITRATE = "192k"
    AUDIO_VOLUME = 0.7

    # Text overlay settings
    SECONDARY_TEXT_COLOR = "yellow"
    MAX_CHARS_PER_LINE = 25
    FONT_SIZE = 64
    LINE_HEIGHT_MULTIPLIER = 1.3
    PADDING_X = 40
    PADDING_Y = 30
    BORDER_RADIUS = 28
    SHADOW_BLUR = 20
    SHADOW_OFFSET = 6
    TEXT_COLOR = (255, 255, 255, 255)
    BG_COLOR = (20, 20, 20, 220)


    # Instagram API settings
    MAX_STATUS_ATTEMPTS = 30
    STATUS_CHECK_INTERVAL = 10

    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        required_vars = {
            "GOOGLE_SHEET_URL": cls.GOOGLE_SHEET_URL,
            "ACCOUNT_ID": cls.ACCOUNT_ID,
            "ACCESS_TOKEN": cls.ACCESS_TOKEN,
            "TWILIO_SID": cls.TWILIO_SID,
            "TWILIO_TOKEN": cls.TWILIO_TOKEN,
            "TWILIO_WHATSAPP_FROM": cls.TWILIO_WHATSAPP_FROM,
            "TWILIO_WHATSAPP_TO": cls.TWILIO_WHATSAPP_TO,
            "CLOUDINARY_CLOUD_NAME": cls.CLOUDINARY_CLOUD_NAME,
            "CLOUDINARY_API_KEY": cls.CLOUDINARY_API_KEY,
            "CLOUDINARY_API_SECRET": cls.CLOUDINARY_API_SECRET,
        }

        missing = [key for key, value in required_vars.items() if not value]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return True

    @classmethod
    def ensure_directories(cls):
        """Ensure output directories exist"""
        os.makedirs(os.path.dirname(cls.OUTPUT_VIDEO), exist_ok=True)
        os.makedirs(os.path.join(cls.BASE_DIR, "assets", "fonts"), exist_ok=True)