import os
import subprocess


class YouTube:
    """
        YouTube video downloader
        
        Need install youtube-dl on you platform
    """
    pref_settings = ' -f "bestvideo[height=720]+best[ext=mp4]" '
    sub_extension = 'srt'
    sub_extensions = ['srt', 'vtt']
    languages = ['en', 'ru']
    directory = 'youtube'

    def __init__(self, video_url, directory=None):
        self.video_url = video_url
        self.directory = directory or self.directory

    def download(self):
        file_path = os.path.join(self.directory, ' %(playlist_index)s-%(title)s.%(ext)s')
        subs = (' --all-subs --write-auto-sub '
                '--convert-subs="{sub_format}"'.format(sub_format=self.sub_extension))
        youtube_dl_params = ('"{video_url}" '
                             '-o "{file_path}" ') + subs + self.pref_settings
        filled_params = youtube_dl_params.format(video_url=self.video_url, file_path=file_path)

        self.run_command('youtube-dl ' + filled_params)
        self.delete_unnecessary_subtitles()

    def download_py(self):
        import youtube_dl
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_url])

    def run_command(self, command):
        subprocess.check_call(command, shell=True, env=self.get_environ())

    def delete_unnecessary_subtitles(self):
        from deleter_unnecesary_files import DeleteUnnecessaryFiles

        need_leave_files_with_ends = DeleteUnnecessaryFiles.get_need_leave_files_with_ends(
            self.languages, self.sub_extensions)
        DeleteUnnecessaryFiles(self.directory, self.sub_extensions, need_leave_files_with_ends)

    @staticmethod
    def get_environ():
        current_environ = os.environ
        current_environ['PATH'] = current_environ.get('PATH', '') + ':/usr/local/bin'
        return current_environ


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


if __name__ == '__main__':
    YouTube('https://www.youtube.com/'
            'watch?annotation_id=annotation_3706615519&feature='
            'iv&src_vid=JNXOBN8kJrM&v=uh0Ri9440BQ').download()


# class YouTubeDownloader:
#     resolutions = ['720p', '480p', '360p', '240p']
#     extension = 'mp4'
#     subtitles = ['en', 'ru']
#     chunk_size = 8 * 1024
#     # subtitles_download_api = 'http://video.google.com/timedtext?lang={lang}&v={video_id}'
#
#     def __init__(self, video_url):
#         self.video_url = video_url
#         self.yt = YouTube(video_url)
#
#     def download(self, download_dir='.', with_subtitles=True):
#         self.get_video().download(download_dir, on_progress=self.loader_show, force_overwrite=True)
#
#     def loader_show(self, _bytes_received, file_size, start):
#         if _bytes_received == self.chunk_size:
#             print('\n  **** **** \n  LOAD file {} '.format(self.yt.filename))
#             print('  file_size {0:0.2f} = mb'.format(file_size / 8 / 1024 / 1024))
#         max_count_points = 30
#         current_count_percents = int(float(_bytes_received) / file_size * max_count_points)
#         line = '*' * current_count_percents + '_' * (max_count_points - current_count_percents)
#         print(line, end="\r")
#
#     def get_video(self):
#         return self.yt.get(**self.get_resolution())

    # def get_resolution(self):
    #     for resolution in self.resolutions:
    #         if self.yt.filter(self.extension, resolution=resolution):
    #             return {'extension': self.extension, 'resolution': resolution}

# yt = YouTueDownloader("https://www.youtube.com/watch?v=Q1wHkuzJAV0")
# yt = YouTubeDownloader("https://www.youtube.com/watch?v=edWI4ZnWUGg")
# yt = YouTubeDownloader("https://www.youtube.com/watch?v=AjFfsOA7AQI")
# yt.download()
