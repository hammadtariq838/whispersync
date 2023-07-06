from django.db import models
# get_user_model
from django.contrib.auth import get_user_model
from .utils import convert_seconds_to_hms

User = get_user_model()


class Subtitle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=200)
    length = models.IntegerField()  # in seconds
    thumbnail_url = models.URLField(max_length=200)
    status = models.CharField(max_length=200, default='pending')
    cost = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    error = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=200, default='en')
    file_path = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.status}'

    def get_display_length(self):
        return convert_seconds_to_hms(self.length)

    def get_display_cost(self):
        return f'{self.cost / 100}'
