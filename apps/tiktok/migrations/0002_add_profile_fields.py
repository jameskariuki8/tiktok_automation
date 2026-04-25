from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tiktok', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tiktokaccount',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tiktokaccount',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
