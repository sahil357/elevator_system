# Generated by Django 4.1 on 2022-09-04 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_system', '0006_alter_elevatortravellog_request_door'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevatortravellog',
            name='elevator_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elevator_system.elevator'),
        ),
    ]