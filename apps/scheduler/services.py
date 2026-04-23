from .models import ScheduledPost
from django.utils import timezone
from .tasks import publish_scheduled_post

class SchedulerService:
    @staticmethod
    def schedule_post(post_id):
        """
        Triggers the celery task for a specific post.
        """
        post = ScheduledPost.objects.get(id=post_id)
        if post.status == 'draft':
            post.status = 'scheduled'
            post.save()
            
            # Triggering synchronously for now to bypass Celery queue issues on Railway
            from .tasks import publish_scheduled_post
            publish_scheduled_post(post_id)
            return True
        return False

    @staticmethod
    def get_upcoming_posts(user):
        return ScheduledPost.objects.filter(user=user, scheduled_time__gte=timezone.now()).order_by('scheduled_time')
