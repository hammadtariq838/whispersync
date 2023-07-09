from django.urls import path
from .views import youtube_info, download_subtitle, subtitles, subtitle_details, retry_download

urlpatterns = [
    path('verify-info/', youtube_info, name='verify_info'),
    path('download-subtitle/', download_subtitle, name='download_subtitle'),
    path('subtitles/', subtitles, name='subtitles'),
    path('subtitles/<int:subtitle_id>/',
         subtitle_details, name='subtitle_details'),
    path('subtitles/<int:subtitle_id>/retry/',
         retry_download, name='retry_download'),
]
