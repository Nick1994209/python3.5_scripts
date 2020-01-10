from youtube_download import YouTubeDownloader
from credentials import GoogleServicesCredential

downloader = YouTubeDownloader(**GoogleServicesCredential.get_credentials())


def download_video_best(path, directory):
    downloader.download(
        path,
        download_playlist=False,
        directory=f'youtube/{directory}',
        ignore_errors=False,
        video_format='[height>=720]',
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
    'https://www.youtube.com/watch?v=qT95d_W5kpU&list=PL_L_HiHe5k_1VLeL9hta_6IIXN71pf_-H&index=3',
    'team_lead_conf',
)
