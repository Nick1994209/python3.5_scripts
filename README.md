### Some scripts

##### download video:
    * youtube
    * coursera


```
from youtube_download import YouTube
YouTube('https://www.youtube.com/watch?v=VhXMkswfASE').download()
```

```
from coursera_downloader import Coursera
coursera = Coursera(username, password)
coursera.list_courses()
coursera.download_course(your_course)
```

```
from coursera_downloader import Coursera
coursera = Coursera(username, password)
coursera.list_courses()
coursera.download_course(your_course)
```

##### Translate "srt" subtitles

```
from sub_translator import directory_subs_translate

directory_subs_translate('./coursera/')
```