from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Users(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.BigIntegerField(unique=True, null=True)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=225)
    date_of_birth = models.DateField(null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username)