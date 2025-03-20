from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default='Man')
    image = models.ImageField(default='profile_pics/default_woman.jpg' if gender =='man' else 'profile_pics/default_man.jpg' , upload_to='profile_pics')
    bio = models.TextField(default='')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        width, height = img.size
        min_size = min(width, height)
        img = img.crop((0, 0, min_size, min_size))
        
        img.save(self.image.path)
    