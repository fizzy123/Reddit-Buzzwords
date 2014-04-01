from django.db import models
import datetime

class Post(models.Model):
    title = models.CharField(max_length=400)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
