from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import yt_dlp

from subtitles.models import Subtitle
from .utils import convert_seconds_to_hms
from .tasks import generate_subtitle


@login_required
def youtube_info(request):
    if request.method == 'POST':
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
    else:
        return render(request, 'subtitles/home.html')


@login_required
def subtitles(request):
    user = request.user
    subtitles = Subtitle.objects.filter(user=user).order_by('-created_at')
    context = {
        'subtitles': subtitles,
    }
    return render(request, 'subtitles/subtitles.html', context)


@login_required
def subtitle_details(request, subtitle_id):
    user = request.user
    subtitle = Subtitle.objects.get(id=subtitle_id)
    if subtitle.user != user:
        messages.error(request, 'You are not authorized to view this page')
        return redirect('youtube_info')
    context = {
        'subtitle': subtitle,
    }
    return render(request, 'subtitles/subtitle_details.html', context)


@login_required
def download_subtitle(request):
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
                    status='scheduled'
                )
                subtitle_id = subtitle.id

                generate_subtitle.delay(subtitle_id)  # celery task

                messages.success(
                    request, 'Your video has been successfully scheduled for processing')
                return redirect('subtitles')
            except yt_dlp.DownloadError as e:
                print(f"Error extracting video info: {e}")
                messages.error(
                    request, 'Failed to get video info. Please try again.')
                return redirect('youtube_info')
    except Exception as e:
        print(e)
        messages.error(
            request, 'Failed to get video info. Please try again.')
        return redirect('youtube_info')


@login_required
def retry_download(request, subtitle_id):
    subtitle = Subtitle.objects.get(id=subtitle_id)
    if subtitle.status == 'failed':
        subtitle.status = 'scheduled'
        subtitle.save()
        generate_subtitle.delay(subtitle_id)
        messages.success(
            request, 'Your video has been successfully scheduled for processing')
        return redirect('subtitles')
    else:
        messages.error(
            request, 'This video is not in a failed state. Please try again.')
        return redirect('subtitles')
