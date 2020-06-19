from django.db import models

# Create your models here.
class Chatimages(models.Model):
    image = models.ImageField(upload_to = 'chat_images/')
