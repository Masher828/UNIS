# Generated by Django 3.0.5 on 2020-06-05 13:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20200604_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chatimages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='chat_images/')),
            ],
        ),
        migrations.AlterField(
            model_name='details',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 5, 19, 13, 25, 491516)),
        ),
    ]
