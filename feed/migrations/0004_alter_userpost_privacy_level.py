# Generated by Django 4.1.7 on 2023-03-06 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_rename_comment_userpostcomment_communitypostcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='privacy_level',
            field=models.SmallIntegerField(default=0),
        ),
    ]
