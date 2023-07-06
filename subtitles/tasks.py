# celery task download_audio takes subtitle_id as an argument and uses it to get the subtitle object from the database. It then calls the download_audio method on the subtitle object to download the audio and create a transaction object.

import os
import yt_dlp
from celery import shared_task
from django.conf import settings
from .models import Subtitle
# , Transaction
from users.models import Profile


def download_audio(subtitle_id):
    # subtitle = Subtitle.objects.get(id=subtitle_id)
    # profile = Profile.objects.get(user=subtitle.user)
    # # transaction = Transaction.objects.create(subtitle=subtitle, profile=profile)
    # # transaction.save()
    # # subtitle.transaction = transaction
    # # subtitle.save()
    # # subtitle.download_audio()
    # # subtitle.transaction = None
    # # subtitle.save()
    # subtitle.download_audio()
    pass
