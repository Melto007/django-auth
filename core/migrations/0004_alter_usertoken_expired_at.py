# Generated by Django 4.2.4 on 2023-09-03 05:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_usertoken_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 3, 5, 43, 6, 709493)),
        ),
    ]