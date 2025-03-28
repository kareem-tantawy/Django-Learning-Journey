from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Created by {self.author} at {self.created_at}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by("created_at")

    @property
    def is_parent(self):
        return self.parent is None

    @property
    def level(self):
        """
        Calculate the nesting level of the comment.
        Root comments have level 0, first-level replies have level 1, and so on.
        """
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level

    def get_all_children(self):
        """
        Recursively get all child comments
        """
        children = list(self.replies.all())
        for child in self.replies.all():
            children.extend(child.get_all_children())
        return children