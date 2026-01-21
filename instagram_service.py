import requests
import time

class InstagramService:
    """Service for handling Instagram API operations"""

    def __init__(self, config):
        """Initialize Instagram service with credentials"""
        self.account_id = config.ACCOUNT_ID
        self.access_token = config.ACCESS_TOKEN
        self.max_attempts = config.MAX_STATUS_ATTEMPTS
        self.check_interval = config.STATUS_CHECK_INTERVAL

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

    def create_media_container(self, video_url, caption):
        """Create Instagram media container"""
        url = f"https://graph.instagram.com/v23.0/{self.account_id}/media"

        payload = {
            "video_url": video_url,
            "media_type": "REELS",
            "caption": caption
        }

        try:
            resp = requests.post(url, headers=self.headers, json=payload).json()

            if "id" not in resp:
                raise Exception(f"Error creating media container: {resp}")

            creation_id = resp["id"]
            print(f"✓ Media container created: {creation_id}")

            return creation_id

        except Exception as e:
            raise Exception(f"Failed to create media container: {str(e)}")

    def wait_for_processing(self, creation_id):
        """Wait for Instagram to process the video"""
        print("⏳ Waiting for media to be processed...")

        attempt = 0

        while attempt < self.max_attempts:
            status_url = f"https://graph.instagram.com/v23.0/{creation_id}"
            status_params = {
                "fields": "status_code",
                "access_token": self.access_token
            }

            try:
                status_resp = requests.get(status_url, params=status_params).json()

                if "status_code" in status_resp:
                    status = status_resp["status_code"]
                    print(f"  Status: {status} (Attempt {attempt + 1}/{self.max_attempts})")

                    if status == "FINISHED":
                        print("✓ Media processing complete!")
                        return True

                    elif status == "ERROR":
                        raise Exception(f"Media processing failed: {status_resp}")

                attempt += 1
                time.sleep(self.check_interval)

            except Exception as e:
                raise Exception(f"Error checking media status: {str(e)}")

        raise Exception("Timeout waiting for media to be processed")

    def publish_media(self, creation_id):
        """Publish the processed media to Instagram"""
        publish_url = f"https://graph.instagram.com/v23.0/{self.account_id}/media_publish"

        publish_payload = {
            "creation_id": creation_id
        }

        try:
            publish_resp = requests.post(
                publish_url,
                headers=self.headers,
                json=publish_payload
            ).json()

            if "id" not in publish_resp:
                raise Exception(f"Error publishing media: {publish_resp}")

            post_id = publish_resp["id"]
            post_url = f"https://www.instagram.com/reel/{post_id}/"

            print(f"✓ Upload successful! {post_url}")

            return post_id, post_url

        except Exception as e:
            raise Exception(f"Failed to publish media: {str(e)}")

    def post_video(self, video_url, caption):
        """Complete workflow to post video to Instagram"""
        # Step 1: Create media container
        creation_id = self.create_media_container(video_url, caption)

        # Step 2: Wait for processing
        self.wait_for_processing(creation_id)

        # Step 3: Publish
        post_id, post_url = self.publish_media(creation_id)

        return post_id, post_url