from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tiktok', '0002_add_stealth_column'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='tiktokaccount',
            table='tiktok_account_v2',
        ),
    ]
