# Generated by Django 4.0.6 on 2022-07-25 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_reoccuringapp_day_alter_timeslot_day'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reoccuringapp',
            old_name='time',
            new_name='time_slot',
        ),
        migrations.RemoveField(
            model_name='reoccuringapp',
            name='day',
        ),
    ]