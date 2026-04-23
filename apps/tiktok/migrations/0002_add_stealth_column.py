from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tiktok', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tiktokaccount',
            name='stealth_token',
            field=models.TextField(blank=True, help_text='Paste your sessionid cookie here', null=True),
        ),
    ]
