from django.urls import path
from .views import home, youtube_info, download_subtitle, transactions, subtitle_details

urlpatterns = [
    path('', home, name='home'),
    path('verify-info/', youtube_info, name='verify_info'),
    path('download-subtitle/', download_subtitle, name='download_subtitle'),
    path('transactions/', transactions, name='transactions'),
    path('subtitle/<int:subtitle_id>/',
         subtitle_details, name='subtitle_details'),
]
