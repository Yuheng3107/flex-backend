# Generated by Django 4.1.7 on 2023-03-12 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0006_remove_exerciseregime_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='likes',
            new_name='likes',
        ),
        migrations.RenameField(
            model_name='exerciseregime',
            old_name='likes',
            new_name='likes',
        ),
        migrations.AlterField(
            model_name='exercise',
            name='posted_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='exerciseregime',
            name='posted_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
