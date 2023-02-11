from django.db import models

# Create your models here.

class Witness(models.Model):
    full_name = models.CharField(max_length=100,unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
