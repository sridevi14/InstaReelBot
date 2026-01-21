from twilio.rest import Client as TwilioClient

class NotificationService:
    """Service for sending WhatsApp notifications via Twilio"""

    def __init__(self, config):
        """Initialize Twilio client"""
        self.client = TwilioClient(
            config.TWILIO_SID,
            config.TWILIO_TOKEN
        )
        self.whatsapp_from = config.TWILIO_WHATSAPP_FROM
        self.whatsapp_to = config.TWILIO_WHATSAPP_TO

    def send_whatsapp(self, message):
        """Send WhatsApp message"""
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.whatsapp_from,
                to=self.whatsapp_to
            )
            print(f"✓ WhatsApp notification sent: {msg.sid}")
            return True

        except Exception as e:
            print(f"✗ Failed to send WhatsApp notification: {str(e)}")
            return False

    def send_success_notification(self, date, post_url):
        """Send success notification"""
        message = (
            f"✅ Instagram video posted successfully!\n"
            f"📅 {date}\n"
            f"🔗 {post_url}"
        )
        return self.send_whatsapp(message)

    def send_error_notification(self, date, error):
        """Send error notification"""
        message = (
            f"❌ Instagram video posting failed!\n"
            f"📅 {date}\n"
            f"⚠️ Error: {error}"
        )
        return self.send_whatsapp(message)