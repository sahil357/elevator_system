# Generated by Django 4.1 on 2022-09-04 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elevatortravellog',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]