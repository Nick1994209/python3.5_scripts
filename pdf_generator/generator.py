import os

from fpdf import FPDF
from PIL import Image
import re


def make_pdf(pdf_file_name, list_pages, directory=''):
    cover = Image.open(list_pages[0])
    width, height = cover.size

    if width > height:
        raise Exception('Manga fail!!!')

    pdf = FPDF(unit="pt", format=[width, height])

    for image_path in list_pages:
        pdf.add_page()
        pdf.image(image_path, 0, 0)

    pdf.output(os.path.join(directory, pdf_file_name + ".pdf"), "F")


def get_pdf_images(directory, recursive=True, img_formates=frozenset({'jpg'})):
    def sorted_func(file_name):
        maths = re.findall(r'\d+', file_name)
        if not maths:
            return file_name
        else:
            return maths[0]

    files = []

    for file in sorted(os.listdir(directory), key=sorted_func):
        path = os.path.join(directory, file)
        if os.path.isdir(path) and recursive:
            files.extend(get_pdf_images(path, recursive=recursive))
        elif file.rsplit('.')[-1].lower() in img_formates:
            print(file)
            files.append(path)
        print(file)
    return files


if __name__ == '__main__':
    list_images = get_pdf_images('/Users/n.korolkov/Downloads')
    print(list_images)
    make_pdf('aaa', list_pages=list_images)
