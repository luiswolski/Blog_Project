from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


class Comment(models.Model):
    name_comment = models.CharField(max_length=150)
    email_comment = models.EmailField()
    comment = models.TextField()
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    date_comment = models.DateTimeField(default=timezone.now)
    published_comment = models.BooleanField(default=False)


    def __str__(self):
        return self.name_comment