# Generated by Django 5.1.1 on 2024-10-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_height_alter_userprofile_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
