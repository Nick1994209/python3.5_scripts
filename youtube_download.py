import os
import youtube_dl
from edit_subtitles_times import DirectoryWithSubtitlesEditImpositionTime
from sub_translator import directory_subs_translate

'''
YouTube example use
youtube_with_subs = YouTube(with_subtitles=True, need_translate=True, video_height=720,
                            username='nick1994209@gmail.com', password='NICK785665')
youtube_without_subs = YouTube(with_subtitles=False, need_translate=False, video_height=720,
                               username='nick1994209@gmail.com', password='NICK785665')

youtube_without_subs.download(
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
    pref_settings = ' -f "bestvideo[height={video_height}]" '  # +best[ext=mp4]" '
    sub_extension = 'srt'
    sub_extensions = ['srt', 'vtt']
    languages = ['en', 'ru']

    def __init__(self, with_subtitles=True, need_translate=False,
                 video_height=720, username=None, password=None):
        self.with_subtitles = with_subtitles
        self.need_translate = need_translate
        self.video_height = video_height
        self.username = username
        self.password = password

    def download(self, url, download_playlist=False, directory='youtube',
                 no_check_ssl=True, ignore_errors=False):

        postprocessors = [
            {
                'key': 'FFmpegSubtitlesConvertor',
                'format': self.sub_extension,  # (currently supported: srt|ass|vtt)')
            }
        ]
        ydl_opts = {
            'nocheckcertificate': no_check_ssl,
            'outtmpl': os.path.join(directory, '%(playlist_index)s-%(title)s.%(ext)s'),
            'ignoreerrors': ignore_errors,
            'allsubtitles': self.with_subtitles,
            'writeautomaticsub': self.with_subtitles,
            'postprocessors': postprocessors,
            # 'format': 'bestvideo[height=720]',
            # 'format': 'bestvideo+bestaudio/best',
            'progress_with_newline': False,  # TODO передать в Downloader
            'noplaylist': not download_playlist,

            # for speed up download
            # 'external_downloader': 'aria2c',
            'format': '43',

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

        self.post_download_process(directory)

    def post_download_process(self, directory):
        self.delete_unnecessary_subtitles(directory)
        DirectoryWithSubtitlesEditImpositionTime.find_subtitles_and_edit(directory)
        if self.need_translate:
            directory_subs_translate(directory, 'en', 'ru')

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