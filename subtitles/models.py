from django.db import models
# get_user_model
from django.contrib.auth import get_user_model

User = get_user_model()


class Subtitle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    length = models.IntegerField()  # in seconds
    thumbnail_url = models.URLField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, default='pending')
    cost = models.IntegerField()
    error = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=200, default='en')
    file_path = models.CharField(max_length=200, null=True, blank=True)
