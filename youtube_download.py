import os
import subprocess


class YouTube:
    """
        YouTube video downloader
        
        Need install youtube-dl on you platform
    """
    pref_settings = ' -f "bestvideo[height=720]+best[ext=mp4]" '
    sub_extension = 'srt'
    ru_sub = property(lambda self: 'ru.' + self.sub_extension)
    en_sub = property(lambda self: 'en.' + self.sub_extension)
    directory = 'youtube'

    def __init__(self, video_url, directory=None):
        self.video_url = video_url
        self.directory = directory or self.directory

    def download(self):
        file_path = os.path.join(self.directory, ' %(playlist_index)s-%(title)s.%(ext)s')
        subs = (' --all-subs --write-auto-sub '
                '--convert-subs="{sub_format}"'.format(sub_format=self.sub_extension))
        command = ('youtube-dl '
                   '"{video_url}" '
                   '-o "{file_path}" ') + subs + self.pref_settings
        self.run_command(command.format(video_url=self.video_url, file_path=file_path))
        self.delete_unnecessary_subtitles()

    def run_command(self, command):
        subprocess.check_call(command, shell=True, env=self.get_environ())

    def delete_unnecessary_subtitles(self):
        all_files = os.listdir(self.directory)
        for f in all_files:
            if f.endswith(self.sub_extension) and (
                        not f.endswith(self.en_sub) and not f.endswith(self.ru_sub)):
                sub_path = os.path.join(self.directory, f)
                os.remove(sub_path)

    @staticmethod
    def get_environ():
        current_environ = os.environ
        current_environ['PATH'] = current_environ.get('PATH', '') + ':/usr/local/bin'
        return current_environ


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
