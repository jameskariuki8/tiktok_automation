# Generated manually to relax constraints - Timestamp: 4321
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('comments_ai', '0002_knowledgedocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsuggestion',
            name='tiktok_video_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='commentsuggestion',
            name='comment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='commentsuggestion',
            name='commenter_username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
