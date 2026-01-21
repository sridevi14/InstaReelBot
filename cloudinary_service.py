import cloudinary
import cloudinary.uploader

class CloudinaryService:
    """Service for handling Cloudinary operations"""

    def __init__(self, config):
        """Initialize Cloudinary with credentials"""
        cloudinary.config(
            cloud_name=config.CLOUDINARY_CLOUD_NAME,
            api_key=config.CLOUDINARY_API_KEY,
            api_secret=config.CLOUDINARY_API_SECRET,
            secure=True
        )

    def upload_video(self, video_path):
        """Upload video to Cloudinary"""
        try:
            upload_result = cloudinary.uploader.upload_large(
                video_path,
                resource_type="video",
                chunk_size=6000000
            )

            video_url = upload_result['secure_url']
            public_id = upload_result['public_id']

            print(f"✓ Video uploaded to Cloudinary: {video_url}")

            return video_url, public_id

        except Exception as e:
            raise Exception(f"Failed to upload video to Cloudinary: {str(e)}")

    def delete_video(self, public_id):
        """Delete video from Cloudinary"""
        try:
            delete_result = cloudinary.uploader.destroy(public_id, resource_type="video")

            if delete_result.get('result') == 'ok':
                print(f"✓ Video deleted from Cloudinary: {public_id}")
                return True
            else:
                print(f"✗ Failed to delete video from Cloudinary: {delete_result}")
                return False

        except Exception as e:
            print(f"Error deleting video from Cloudinary: {str(e)}")
            return False