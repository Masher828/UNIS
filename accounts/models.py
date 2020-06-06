from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Profile_pic = models.ImageField(upload_to = 'profile_picture/')
    status = models.TextField(default = "Available")
    created_at = models.DateTimeField(default = datetime.now())
    isOnline = models.CharField(max_length = 20, default="false")
    lastseen = models.CharField(max_length = 50, default='not available')
