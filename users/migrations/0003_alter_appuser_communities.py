# Generated by Django 4.1.7 on 2023-03-17 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_communitymembers'),
        ('users', '0002_appuser_chat_groups_appuser_communities_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='communities',
        ),
        migrations.AddField(
            model_name='appuser',
            name='communities',
            field=models.ManyToManyField(through='community.CommunityMembers', to='community.community'),
        ),
    ]
