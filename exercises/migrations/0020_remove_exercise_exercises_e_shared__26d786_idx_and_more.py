# Generated by Django 4.2 on 2023-05-04 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0019_rename_exercisedetails_exerciseregimeinfo'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='exercise',
            name='exercises_e_shared__26d786_idx',
        ),
        migrations.RemoveIndex(
            model_name='exerciseregime',
            name='exercises_e_shared__08aa51_idx',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='id',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='likers',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='media',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='posted_at',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='shared_id',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='shared_type',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='text',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='id',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='likers',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='media',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='posted_at',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='shared_id',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='shared_type',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='exerciseregime',
            name='text',
        ),
    ]
