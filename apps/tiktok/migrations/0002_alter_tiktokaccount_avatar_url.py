from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tiktok', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiktokaccount',
            name='avatar_url',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
