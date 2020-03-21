from youtube_download import YouTubeDownloader
from credentials import GoogleServicesCredential

downloader = YouTubeDownloader(**GoogleServicesCredential.get_credentials())


def download_video_best(path, directory, video_format='[height>=720]'):
    downloader.download(
        path,
        download_playlist=False,
        directory=f'youtube/{directory}',
        ignore_errors=False,
        video_format=video_format,
        # video_format='bestvideo',
        with_subtitles=False,
        need_translate=False,
        before_filename='',
    )


def download_multiple_best_video(playlist_list, directory):
    downloader.download(
        playlist_list,
        download_playlist=True,
        directory=f'youtube/{directory}',
        ignore_errors=False,
        video_format='[height>=720]',
        with_subtitles=False,
        need_translate=False,
        before_filename='',
    )


def download_multiple_normal_video(playlist_list, directory):
    downloader.download(
        playlist_list,
        download_playlist=True,
        directory=f'youtube/{directory}',
        ignore_errors=False,
        video_format='[height>=360]',
        with_subtitles=False,
        need_translate=False,
        before_filename='',
    )


def download_video_bad_quality(path, directory):
    for video_format in ['133', '134', '135', '160', '43']:
        try:
            return downloader.download(
                path,
                directory=f'youtube/{directory}',
                video_format=video_format,
            )
        except Exception as e:
            print(f'raised {e} video_format={video_format}')
    raise Exception('Can not download video')


def download_audio(path, directory):
    downloader.download(
        path,
        directory=f'youtube/{directory}',
        video_format='140',  # m4a
    )


download_video_bad_quality(
    'https://www.youtube.com/watch?v=6I6chocTcIo&list=WL&index=2&t=1192s',
    'my_playlist',
)

download_video_bad_quality(
    'https://www.youtube.com/watch?v=h10qZGq36DE&list=WL&index=7&t=0s',
    'my_playlist',
)

download_video_best(
    'https://www.youtube.com/watch?v=P13KVYTu0eU&list=WL&index=4&t=535s',
    'my_playlist',
    video_format='[height>=360]',
)
