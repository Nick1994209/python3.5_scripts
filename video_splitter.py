#!/usr/bin/env python

import csv
import subprocess
import re
import math
import json
import os
from optparse import OptionParser

from tqdm import tqdm

length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
re_length = re.compile(length_regexp)


def split_by_seconds(filename, split_length=None, split_count=None, vcodec="copy", acodec="copy",
                     extra="", **kwargs):
    if split_length and split_length <= 0:
        print ("Split length can't be 0")
        raise SystemExit

    if not split_count and not split_length:
        raise Exception

    if split_length and split_count:
        raise Exception('cannot split by video length and count chunks!')

    video_duration_raw = subprocess.Popen("ffmpeg -i '" + filename + "' 2>&1 | grep 'Duration'",
                                          shell=True,
                                          stdout=subprocess.PIPE
                                          ).stdout.read().decode()
    matches = re_length.search(video_duration_raw)
    if matches:
        video_length = int(matches.group(1)) * 3600 + \
                       int(matches.group(2)) * 60 + \
                       int(matches.group(3))
        print("Video length in seconds: " + str(video_length))
    else:
        print("Can't determine video length.")
        raise SystemExit

    if split_length:
        split_count = int(math.ceil(video_length/float(split_length)))
    elif split_count:
        split_length = video_length / split_count

    split_cmd = "ffmpeg '%s' -vcodec %s -acodec %s %s" % (filename, vcodec, acodec, extra)
    # split_cmd = "ffmpeg -i '%s' -vcodec %s -acodec %s %s" % (filename, vcodec, acodec, extra)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in tqdm(range(0, split_count)):
        split_str = ""
        if n == 0:
            split_start = 0
        else:
            split_start = split_length * n

        split_str += " -ss "+str(split_start)+" -t "+str(split_length) + \
                    " '"+filebase + "-" + str(n) + "." + fileext + \
                    "'"
        print ("About to run: "+split_cmd+split_str)
        output = subprocess.Popen(split_cmd+split_str, shell = True, stdout =
                               subprocess.PIPE).stdout.read()


megabyte = 1024 * 1024 * 1024


def split_file_for_size(video_file_path, max_file_size=4*megabyte):
    print(video_file_path)
    print(os.stat(video_file_path).st_size)
    file_size = os.stat(video_file_path).st_size
    count_chunks = file_size // max_file_size + 1
    if count_chunks < 1:
        return
    split_by_seconds(video_file_path, split_count=count_chunks)


if __name__ == '__main__':
    split_file_for_size('/Users/n.korolkov/Documents/Under2.mkv')
    # main()
