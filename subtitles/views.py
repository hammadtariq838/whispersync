import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import yt_dlp

from subtitles.models import Subtitle
from .utils import convert_seconds_to_hms
import openai
from .tasks import download_audio


openai.api_key = settings.WHISPER_API_KEY


@login_required
def home(request):
    return render(request, 'subtitles/home.html')


@login_required
def youtube_info(request):
    url = request.POST.get('url')
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': True,
            'extract_flat': 'in_playlist',
            'forcejson': True,
            'simulate': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                context = {
                    'title': info['title'],
                    'length': convert_seconds_to_hms(info['duration']),
                    'thumbnail_url': info['thumbnail'],
                    'url': url,
                    'dollars': (int(info['duration'] / 10) + 1) / 100,
                    'credits': int(info['duration'] / 10) + 1,
                }
                return render(request, 'subtitles/youtube_info.html', context)
            except yt_dlp.DownloadError as e:
                print(f"Error extracting video info: {e}")
                error_message = 'Failed to get video info'
                return render(request, 'subtitles/youtube_info.html', {'error_message': error_message})
    except Exception as e:
        print(e)
        error_message = 'Failed to get video info'
        return render(request, 'subtitles/youtube_info.html', {'error_message': error_message})


@login_required
def download_subtitles(request):
    url = request.POST.get('url')
    # verify that the user has enough credits
    credits = int(request.POST.get('credits'))
    user = request.user
    if user.profile.credits < credits:
        messages.error(
            request, 'You do not have enough credits to download this video')
        return redirect('purchase_credits')

    # get the video info to create a subtitle object
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'ignoreerrors': True,
            'extract_flat': 'in_playlist',
            'forcejson': True,
            'simulate': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                subtitle = Subtitle.objects.create(
                    user=user,
                    url=url,
                    title=info['title'],
                    length=info['duration'],
                    thumbnail_url=info['thumbnail'],
                    cost=credits,
                )
                subtitle_id = subtitle.id

                # call the celery task to download the audio; it will handle the payment
                download_audio.delay(subtitle_id)

                messages.success(
                    request, 'Your video has been successfully scheduled for processing')
                return redirect('transactions')
            except yt_dlp.DownloadError as e:
                print(f"Error extracting video info: {e}")
                messages.error(
                    request, 'Failed to get video info. Please try again.')
                return redirect('home')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Failed to get video info. Please try again.')
        return redirect('home')


# def download_audio(request):
#     if request.method == 'POST':
#         url = request.POST.get('url')
#         try:
#             ydl_opts = {
#                 'format': 'bestaudio/best',
#                 'outtmpl': f'{settings.MEDIA_ROOT}/%(title)s.%(ext)s',
#                 'postprocessors': [{
#                     'key': 'FFmpegExtractAudio',
#                     'preferredcodec': 'aac',
#                     'preferredquality': '32',
#                 }],
#                 'quiet': True,
#                 'ignoreerrors': True,
#             }

#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=True)
#                 audio_file_path = ydl.prepare_filename(info)
#                 print(audio_file_path)
#                 base, _ = os.path.splitext(audio_file_path)
#                 new_file = base + '.m4a'
#                 print(new_file)

#             return HttpResponse(audio_file_path)
#         except Exception as e:
#             print(e)
#             error_message = 'Failed to download audio'
#             return render(request, 'subtitles/download_audio.html', {'error_message': error_message})
#     else:
#         return render(request, 'subtitles/download_audio.html')
