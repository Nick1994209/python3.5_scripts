"""
Run http server on server

$ ssh $SERVER_PATH
$ cd /home/records/audio/
$ python3 -m http.server 8000 --bind 0.0.0.0
"""

from downloaders.file import download_file

file_names = """
do_obeda_show_nashe_radio2020-03-10_11-00-00.mp3
do_obeda_show_nashe_radio2020-03-12_11-00-00.mp3
do_obeda_show_nashe_radio2020-03-12_21-11-00.mp3
do_obeda_show_nashe_radio2020-03-14_12-04-55.mp3
do_obeda_show_nashe_radio2020-03-17_11-00-00.mp3
do_obeda_show_nashe_radio2020-03-19_11-00-00.mp3
do_obeda_show_nashe_radio2020-03-19_21-11-00.mp3
do_obeda_show_nashe_radio2020-03-24_11-00-00.mp3
do_obeda_show_nashe_radio2020-03-26_11-00-00.mp3
do_obeda_show_nashe_radio2020-03-26_21-11-00.mp3
do_obeda_show_nashe_radio2020-03-29_09-11-47.mp3
do_obeda_show_nashe_radio2020-03-31_11-00-00.mp3
"""

for file_name in file_names.strip().split():
    download_file(f'http://****:8000/{file_name}',
                  file_name, download_to='files/nashe_radio')
