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
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following_set", blank=True
    )

    def get_absolute_url(self):
        return reverse("profile-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        """
        Method to crop image and store it with less storage
        """

        # Save the instance first to ensure the image path is generated
        super().save(*args, **kwargs)

        # Resize the image only if it's not a default one
        if self.image and "default_" not in self.image.name:
            img = Image.open(self.image.path)

            # Resize while maintaining aspect ratio
            max_size = (300, 300)
            img.thumbnail(max_size)

            img.save(self.image.path)  # Save the optimized image

    def follow(self, profile_to_follow):
        """
        Method to follow a user
        """
        if profile_to_follow != self:
            self.following_set.add(profile_to_follow)

    def is_following(self, other_profile):
        """
        Method to check the following status
        """
        return other_profile in self.following_set.all()

    def unfollow(self, profile_to_unfollow):
        """
        Method to unfollow a user
        """
        if self.is_following(profile_to_unfollow):
            self.following_set.remove(profile_to_unfollow)

    def remove_follower(self, profile_to_remove):
        """
        Method to remove a follower from user followers set
        """
        if profile_to_remove in self.following_set.all():
            self.followers.remove(profile_to_remove)

    def get_followers_count(self):
        """
        Return the number of followers
        """
        return self.followers.count()

    def get_following_count(self):
        """
        Return the total number of profiles this user is following
        """
        return self.following_set.count()

    def __str__(self):
        return f"{self.user.username} profile"
