from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
# Create your models here.
class Details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Profile_pic = models.ImageField(upload_to = 'profile_picture/')
    status = models.TextField(default = "Available")
    created_at = models.DateTimeField(default = timezone.now)
    isOnline = models.CharField(max_length = 20, default="false")
    lastseen = models.CharField(max_length = 50, default='not available')
    chat_order = models.TextField(default="null")

class Customprofilepic(models.Model):
    custom_DP = models.ImageField(upload_to='custom_DP/')
