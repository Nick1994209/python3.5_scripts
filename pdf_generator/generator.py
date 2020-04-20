import os

from fpdf import FPDF
from PIL import Image
import re


def get_chapters(directory):
    chapter = {}

    for file in sorted(os.listdir(directory), key=get_sorted_func()):
        path = os.path.join(directory, file)
        if os.path.isdir(path):
            chapter[file] = get_pdf_images(path, recursive=True)
    return chapter


def make_pdf(pdf_file_name, list_pages, directory=''):
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    cover = Image.open(list_pages[0])
    width, height = cover.size

    if width > height:
        raise Exception('Manga fail!!!')

    pdf = FPDF(unit="pt", format=[width, height])

    for image_path in list_pages:
        pdf.add_page()
        pdf.image(image_path, 0, 0)

    pdf.output(os.path.join(directory, pdf_file_name + ".pdf"), "F")


def get_pdf_images(directory, recursive=True, img_formats=frozenset({'jpg', 'png'})):
    files = []

    for file in sorted(os.listdir(directory), key=get_sorted_func()):
        path = os.path.join(directory, file)
        if os.path.isdir(path) and recursive:
            files.extend(get_pdf_images(path, recursive=recursive))
        elif file.rsplit('.')[-1].lower() in img_formats:
            files.append(path)
    return files


def get_sorted_func(is_started_from_chapter=True, number_zeros=3):
    """
    :param is_started_from_chapter: True if filename is Dorohedoro_v01_p001 else False (Dorohedoro_p001_v01)
    """

    def sorted_func(file_name):
        matches = re.findall(r'\d+', file_name)
        if not matches:
            return file_name
        else:
            if not is_started_from_chapter:
                # for Dorohedoro_v02_p001 -> 001-002
                matches.reverse()
            return '-'.join(f'{int(match):0{number_zeros}n}' for match in matches)
    return sorted_func


if __name__ == '__main__':
    chapters = get_chapters(r'E:\Downloads\torrents\Dorohedoro')
    print(list(chapters))

    for index, (chapter_name, list_images) in enumerate(chapters.items()):
        print(index, chapter_name, list_images)
        make_pdf(chapter_name, list_pages=list_images, directory='dorohedoro')
