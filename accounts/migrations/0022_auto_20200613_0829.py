# Generated by Django 3.0.6 on 2020-06-13 02:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20200606_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customprofilepic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_DP', models.ImageField(upload_to='custom_DP/')),
            ],
        ),
        migrations.AlterField(
            model_name='details',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 13, 8, 29, 31, 44340)),
        ),
    ]