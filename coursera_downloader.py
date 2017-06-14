# pip install coursera-dl
# https://pypi.python.org/pypi/coursera-dl

import os
import subprocess


class Coursera:
    coursera_auth = 'coursera-dl -u {username} -p {password} '
    """
optional arguments:
  -h, --help            show this help message and exit
  --list-courses        list course names (slugs) and quit. Listed course
                        names can be put into program arguments
  --resume              resume incomplete downloads (default: False)
  -o, --overwrite       whether existing files should be overwritten (default:
                        False)
  --verbose-dirs        include class name in section directory name
  --quiet               omit as many messages as possible (only printing
                        errors)
  -r, --reverse         download sections in reverse order
  --combined-section-lectures-nums
                        include lecture and section name in final files
  --unrestricted-filenames
                        Do not limit filenames to be ASCII-only

Basic options:
  class_names           name(s) of the class(es) (e.g. "ml-005")
  -u USERNAME, --username USERNAME
                        coursera username
  -p PASSWORD, --password PASSWORD
                        coursera password
  --jobs JOBS           number of parallel jobs to use for downloading
                        resources. (Default: 1)
  --download-delay DOWNLOAD_DELAY
                        number of seconds to wait before downloading next
                        course. (Default: 60)
  -b, --preview         get videos from preview pages. (Default: False)
  --path PATH           path to where to save the file. (Default: current
                        directory)
  -sl SUBTITLE_LANGUAGE, --subtitle-language SUBTITLE_LANGUAGE
                        Choose language to download subtitles and transcripts.
                        (Default: all)Use special value "all" to download all
                        available.To download subtitles and transcripts of
                        multiple languages,use comma(s) (without spaces) to
                        seperate the names of the languages, i.e., "en,zh-
                        CN".To download subtitles and transcripts of
                        alternative language(s) if only the current language
                        is not available,put an "|<lang>" for each of the
                        alternative languages after the current language,
                        i.e., "en|fr,zh-CN|zh-TW|de", and make sure the
                        parameter are wrapped with quotes when "|" presents.

Selection of material to download:
  --only-syllabus       download only syllabus, skip course content. (Default:
                        False)
  --download-quizzes    download quiz and exam questions. (Default: False)
  --about               download "about" metadata. (Default: False)
  -f FILE_FORMATS, --formats FILE_FORMATS
                        file format extensions to be downloaded in quotes
                        space separated, e.g. "mp4 pdf" (default: special
                        value "all")
  --ignore-formats IGNORE_FORMATS
                        file format extensions of resources to ignore
                        (default: None)
  -sf SECTION_FILTER, --section_filter SECTION_FILTER
                        only download sections which contain this regex
                        (default: disabled)
  -lf LECTURE_FILTER, --lecture_filter LECTURE_FILTER
                        only download lectures which contain this regex
                        (default: disabled)
  -rf RESOURCE_FILTER, --resource_filter RESOURCE_FILTER
                        only download resources which match this regex
                        (default: disabled)
  --video-resolution VIDEO_RESOLUTION
                        video resolution to download (default: 540p); only
                        valid for on-demand courses; only values allowed:
                        360p, 540p, 720p
  --disable-url-skipping
                        disable URL skipping, all URLs will be downloaded
                        (default: False)

    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.coursera = self.coursera_auth.format(username=username, password=password)

    def get_list_courses(self):
        self.run_command(self.coursera + '--list-courses')

    def download_course(self, name, download_path='coursera'):
        command = self.coursera + ' --jobs=3 --path="{}" --resume '.format(download_path) + name
        self.run_command(command)

    @staticmethod
    def run_command(command):
        current_environ = os.environ
        current_environ['PATH'] = current_environ.get('PATH', '') + ':/usr/local/bin'
        subprocess.check_call(command, shell=True, env=current_environ)


if __name__ == '__main__':
    from credentials import CourseraCredential
    user_coursera = Coursera(**CourseraCredential.get_credentials())
    # user_coursera = Coursera('login', 'password')

    # user_coursera.get_list_courses()
    user_coursera.download_course('machine-learning')
