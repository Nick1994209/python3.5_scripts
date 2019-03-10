import os
import youtube_dl
from edit_subtitles import DirectorySubtitlesRepair, DirectoryUnionSubtitles
from sub_translator import directory_subs_translate

'''
YouTube example use
YouTubeDownloader().download(
    'https://www.youtube.com/watch?v=uaBp0uiLvKQ&list=PLj8oar3hwqiXIQr-m25rocuCdsjOAx_xp',
    download_playlist=True,
    directory='youtube/neural_networks_microsoft',
    ignore_errors=False
)
'''


class YouTubeDownloader:
    """
        YouTube video downloader
    """
    sub_extension = 'srt'
    sub_extensions = ['srt', 'vtt']
    languages = ['en', 'ru']

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def download(
            self, url, download_playlist=False, directory='youtube',
            no_check_ssl=True, ignore_errors=False, video_format='43', before_filename='',
            with_subtitles=False, need_translate=False, union_subtitles=True,
    ):
        # default video_format='43' - for best speed download
        # else [height=720] [height=360]

        file_name = before_filename + (
            '%(playlist_index)s-%(title)s.%(ext)s' if download_playlist else '%(title)s.%(ext)s'
        )

        postprocessors = [
            {
                'key': 'FFmpegSubtitlesConvertor',
                'format': self.sub_extension,  # (currently supported: srt|ass|vtt)')
            }
        ]
        ydl_opts = {
            'nocheckcertificate': no_check_ssl,
            'outtmpl': os.path.join(directory, file_name),
            'ignoreerrors': ignore_errors,
            'allsubtitles': with_subtitles,
            'writeautomaticsub': with_subtitles,
            'postprocessors': postprocessors,
            # 'format': 'bestvideo[height=720]',
            # 'format': 'bestvideo+bestaudio/best',
            'progress_with_newline': False,  # TODO передать в Downloader
            'noplaylist': not download_playlist,

            # for speed up download
            # 'external_downloader': 'aria2c',
            'format': video_format,
            # 'format': 'bestvideo[height=720]`+43',

            'username': self.username,
            'password': self.password,
            'logger': MyLogger(),
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # def to_screen(message, skip_eol=False):
            #     """Print message to stdout if not in quiet mode."""
            #     print(message, end="\r")
            #     # return ydl.to_stdout(message, skip_eol=-1, check_quiet=True)
            # ydl.to_screen = to_screen

            ydl.download([url])

        self.post_download_process(directory, with_subtitles, need_translate)

    def post_download_process(self, directory, with_subtitles, need_translate):
        self.delete_unnecessary_subtitles(directory)
        if with_subtitles:
            DirectorySubtitlesRepair.find_subtitles_and_edit(directory)
            if need_translate:
                directory_subs_translate(directory, 'en', 'ru')
            DirectoryUnionSubtitles(directory).find_subtitles_and_union()

    def delete_unnecessary_subtitles(self, directory):
        from work_with_files import DeleteUnnecessaryFiles

        need_leave_files_with_ends = DeleteUnnecessaryFiles.get_need_leave_files_with_ends(
            self.languages, self.sub_extensions)
        DeleteUnnecessaryFiles(directory, self.sub_extensions, need_leave_files_with_ends).main()


class MyLogger(object):
    def debug(self, msg):
        print('DEBUG-----', msg)

    def warning(self, msg):
        print('WARNING----', msg)

    def error(self, msg):
        print('ERROR-----', msg)


'''    
    pref_settings = ' -f "bestvideo[height={video_height}]" '  # +best[ext=mp4]" '

    def download_command_line(self, url, directory='youtube', no_check_ssl=False,
                              still_try_download=False):
        """
            Need install youtube-dl on you platform
        """

        file_path = os.path.join(directory, ' %(playlist_index)s-%(title)s.%(ext)s')
        youtube_dl_start_params = ' "{video_url}" -o "{file_path}" --ignore-errors '
        youtube_dl_params = youtube_dl_start_params
        if no_check_ssl:
            youtube_dl_params = ' --no-check-certificate ' + youtube_dl_params
        if self.with_subtitles:
            subs = (' --all-subs --write-auto-sub '
                    '--convert-subs="{sub_format}"'.format(sub_format=self.sub_extension))
            youtube_dl_params += subs

        filled_params = youtube_dl_params.format(video_url=url, file_path=file_path)

        try:
            print(
                'youtube-dl ' + filled_params + self.pref_settings.format(
                    video_height=self.video_height)
            )
            self.run_command('youtube-dl ' + filled_params + self.pref_settings.format(
                video_height=self.video_height))
        except subprocess.CalledProcessError:
            self.run_command('youtube-dl ' + filled_params)
            try:
                self.run_command('youtube-dl ' + filled_params)
            except subprocess.CalledProcessError:
                if still_try_download:
                    filled_params = youtube_dl_start_params.format(video_url=url,
                                                                   file_path=directory + '_try3')
                    self.run_command('youtube-dl ' + filled_params)
                else:
                    raise
        self.post_download_process(directory)

    def run_command(self, command):
        subprocess.check_call(command, shell=True, env=self.get_environ())

    @staticmethod
    def get_environ():
        current_environ = os.environ
        current_environ['PATH'] = current_environ.get('PATH', '') + ':/usr/local/bin'
        return current_environ


'''

if __name__ == '__main__':
    youtube = YouTubeDownloader(username='google_email', password='password')

    youtube.download(
        'https://www.youtube.com/watch?v=5VNfDa0MlXA&list=PLv_zOGKKxVpigCYSm1pVIezNiq1uV803U',
        download_playlist=True,
        directory='youtube/moscowpython63',
        ignore_errors=True,
        video_format='[height=720]',
        # before_filename='',
        with_subtitles=False,
        need_translate=False,
    )
