from celery import shared_task
from .models import ScheduledPost
import logging

logger = logging.getLogger(__name__)

@shared_task
def publish_scheduled_post(post_id):
    try:
        post = ScheduledPost.objects.get(id=post_id)
        if post.status != 'scheduled':
            return f"Post {post_id} is not in scheduled status."

        post.status = 'publishing'
        post.save()

        from tiktok.services import TikTokApiService
        tiktok_service = TikTokApiService(post.user.tiktok_accounts.first())
        
        # Real TikTok API call
        try:
            result = tiktok_service.upload_video(post.video_file.path, post.caption)
        except Exception as api_err:
            logger.error(f"TikTok API Error: {str(api_err)}")
            result = False
        
        if result:
            post.status = 'published'
            post.tiktok_post_id = "uploaded_to_drafts"
            post.save()
            return f"Successfully uploaded post {post_id} to TikTok Drafts"
        else:
            raise Exception("TikTok API rejected the upload. Check if you allowed 'video.upload' permission.")
    except Exception as e:
        if 'post' in locals():
            post.status = 'failed'
            post.error_message = str(e)
            post.save()
        return f"Failed to publish post {post_id}: {str(e)}"
