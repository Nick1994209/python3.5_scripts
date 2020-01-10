### Some scripts for python3.7

##### download video:
    * youtube
    * coursera


#### mac preinstall

    brew install ffmpeg libav #(for convert vtt to srt)
    install xclode  (from appstore)

```python
from youtube_download import YouTubeDownloader

youtube = YouTubeDownloader(username='****@gmail.com',
                            password='****')
youtube.download(
    'https://www.youtube.com/watch?v=VIDEO',
    download_playlist=False,
    directory='youtube/flask',
    ignore_errors=True,
    video_format='best',
    with_subtitles=True,
    need_translate=True,
)
```

```python
from coursera_downloader import Coursera
coursera = Coursera(username, password)
coursera.list_courses()
coursera.download_course(your_course)
```

```python
from coursera_downloader import Coursera
coursera = Coursera(username, password)
coursera.list_courses()
coursera.download_course(your_course)
```

##### Translate "srt" subtitles

```python
from sub_translator import directory_subs_translate

directory_subs_translate('./coursera/')
```