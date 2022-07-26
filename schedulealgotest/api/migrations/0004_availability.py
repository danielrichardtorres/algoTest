# Generated by Django 4.0.6 on 2022-07-24 04:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_reoccuringapp_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(default='', max_length=10)),
                ('start_time', models.TimeField(default=datetime.time(10, 0))),
                ('end_time', models.TimeField(default=datetime.time(14, 30))),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.teacher')),
            ],
            options={
                'ordering': ['day'],
            },
        ),
    ]
