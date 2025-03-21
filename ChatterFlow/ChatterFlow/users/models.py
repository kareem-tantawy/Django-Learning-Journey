from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, default='man')
    image = models.ImageField(default='profile_pics/default_woman.jpg' if gender =='man' else 'profile_pics/default_man.jpg' , upload_to='profile_pics')
    bio = models.TextField(default='')
   
    def __str__(self) -> str:
        return str(self.username)
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        width, height = img.size
        min_size = min(width, height)
        img = img.crop((0, 0, min_size, min_size))
        
        img.save(self.image.path)
    