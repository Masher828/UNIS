# Generated by Django 3.0.6 on 2020-06-02 10:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200602_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 2, 15, 35, 6, 881847)),
        ),
    ]