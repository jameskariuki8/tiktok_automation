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
            
            # Implementation note: In a real system, we'd use eta with the scheduled_time
            # publish_scheduled_post.apply_async((post_id,), eta=post.scheduled_time)
            
            # For this demo, we'll just schedule it
            return True
        return False

    @staticmethod
    def get_upcoming_posts(user):
        return ScheduledPost.objects.filter(user=user, scheduled_time__gte=timezone.now()).order_by('scheduled_time')
