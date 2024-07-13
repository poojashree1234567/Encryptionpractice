from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
import uuid

class Base(models.Model):
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Userprofile(Base):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    COUNTRY_CHOICES = [
        ('india', 'India'),
        ('usa', 'USA'),
        ('canada', 'Canada'),
        ('uk', 'UK'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)

    def __str__(self):
        return f"{self.name} {self.surname}"

class UserPhotos(Base):
    user_profile = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='photos/')

    def __str__(self):
        return f"Photo for {self.user_profile.name} {self.user_profile.surname}"
