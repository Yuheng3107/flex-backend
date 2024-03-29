# Generated by Django 4.1.7 on 2023-03-04 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.PositiveSmallIntegerField()),
                ('content', models.CharField(max_length=10000)),
                ('image', models.ImageField(upload_to='')),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commented_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=5000)),
                ('likes', models.PositiveSmallIntegerField()),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.post')),
            ],
        ),
    ]
