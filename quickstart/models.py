from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django import forms

# Create your models here.


class List(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    # FOR IMAGES ALSO PIP INSTALL PILLOW
    img = models.ImageField(upload_to='tutorial/images', blank=True, null=True)
    vid = models.FileField(upload_to='tutorial/videos', blank=True, null=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    age = models.IntegerField(null=True)
    location = models.CharField(max_length=50, null=True)

    def __str__(self):
        print(self.user)
        return str(self.user)


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
