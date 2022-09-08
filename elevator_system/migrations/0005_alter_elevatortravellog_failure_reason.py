# Generated by Django 4.1 on 2022-09-04 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_system', '0004_alter_elevatortravellog_floor_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevatortravellog',
            name='failure_reason',
            field=models.PositiveSmallIntegerField(choices=[(1, 'None of the Elevators in available'), (2, 'All Working Elevators are stuck on some other floor, please try after some time'), (3, 'Invalid request')], default=None, null=True),
        ),
    ]