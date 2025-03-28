from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from PIL import Image


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return str(self.username)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default="man")
    image = models.ImageField(
        default=(
            "profile_pics/default_woman.jpg"
            if gender == "man"
            else "profile_pics/default_man.jpg"
        ),
        upload_to="profile_pics",
    )
    bio = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} profile"

    def get_absolute_url(self):
        return reverse("profile-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        # Save the instance first to ensure the image path is generated
        super().save(*args, **kwargs)

        # Resize the image only if it's not a default one
        if self.image and "default_" not in self.image.name:
            img = Image.open(self.image.path)

            # Resize while maintaining aspect ratio
            max_size = (300, 300)
            img.thumbnail(max_size)

            img.save(self.image.path)  # Save the optimized image
