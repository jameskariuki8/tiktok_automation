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

        # Place holder for TikTok API logic
        # In Phase 3, we will implement the actual TikTok API call here
        logger.info(f"Publishing post {post_id} to TikTok...")
        
        # Simulate success
        post.status = 'published'
        post.tiktok_post_id = "simulated_tiktok_id"
        post.save()

        return f"Successfully published post {post_id}"
    except Exception as e:
        if 'post' in locals():
            post.status = 'failed'
            post.error_message = str(e)
            post.save()
        return f"Failed to publish post {post_id}: {str(e)}"
