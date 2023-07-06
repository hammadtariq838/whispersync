from django.urls import path
from .views import home, youtube_info, download_subtitles

urlpatterns = [
    path('', home, name='home'),
    path('verify-info/', youtube_info, name='verify_info'),
    path('download-audio/', download_subtitles, name='download_audio'),
]
