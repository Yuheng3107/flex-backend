# Generated by Django 4.2 on 2023-05-23 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0023_remove_exerciseregimeinfo_set_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='posted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='exerciseregime',
            name='posted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]