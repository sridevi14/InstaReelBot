#!/usr/bin/env python3
"""
Instagram Automation Script
Automatically creates and posts videos to Instagram based on Google Sheets schedule
"""

import sys
import traceback

from config import Config
from data_loader import get_today_content
from video_creator import create_video
from cloudinary_service import CloudinaryService
from instagram_service import InstagramService
from notification_service import NotificationService


def main():
    """Main application workflow"""
    try:
        # Step 1: Validate configuration
        print("=" * 60)
        print("INSTAGRAM AUTOMATION WORKFLOW")
        print("=" * 60)

        Config.validate()
        Config.ensure_directories()
        print("✓ Configuration validated")

        # Step 2: Load today's content from Google Sheets
        print("\n[1/5] Loading content from Google Sheets...")
        overlay_text, caption, today = get_today_content(Config.GOOGLE_SHEET_URL)

        if not overlay_text or not caption:
            print(f"✗ No content found for today: {today}")
            print("Exiting...")
            sys.exit(0)

        print(f"✓ Content loaded for {today}")
        print(f"  Overlay Text: {overlay_text[:50]}...")
        print(f"  Caption: {caption[:50]}...")

        # Step 3: Create video
        print(f"\n[2/5] Creating video...")
        video_path = create_video(overlay_text, Config)
        print(f"✓ Video created successfully")

        # Step 4: Upload to Cloudinary
        print(f"\n[3/5] Uploading to Cloudinary...")
        cloudinary_service = CloudinaryService(Config)
        video_url, public_id = cloudinary_service.upload_video(video_path)

        # Step 5: Post to Instagram
        print(f"\n[4/5] Posting to Instagram...")
        instagram_service = InstagramService(Config)
        post_id, post_url = instagram_service.post_video(video_url, caption)

        # Step 6: Cleanup - Delete from Cloudinary
        print(f"\n[5/5] Cleaning up...")
        cloudinary_service.delete_video(public_id)

        # Step 7: Send success notification
        print(f"\n[✓] Sending notification...")
        notification_service = NotificationService(Config)
        notification_service.send_success_notification(today, post_url)

        # Final summary
        print("\n" + "=" * 60)
        print("SUCCESS! Video posted to Instagram")
        print("=" * 60)
        print(f"📅 Date: {today}")
        print(f"🔗 URL: {post_url}")
        print(f"📝 Caption: {caption[:100]}...")
        print("=" * 60)

        return 0

    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR OCCURRED")
        print("=" * 60)
        print(f"❌ {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("=" * 60)

        # Send error notification
        try:
            from datetime import date
            notification_service = NotificationService(Config)
            notification_service.send_error_notification(date.today(), str(e))
        except:
            print("Failed to send error notification")

        return 1


if __name__ == "__main__":
    sys.exit(main())