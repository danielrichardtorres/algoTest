# Generated by Django 4.0.6 on 2022-07-24 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_appinstance_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appinstance',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appinstance',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]