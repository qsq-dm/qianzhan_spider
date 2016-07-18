# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from PIL import Image
import cv2
import numpy
import pytesseract


def convert_to_jpg(gif_file):
    o_filename = gif_file[:-4] + '.jpg'

    im = Image.open(gif_file)
    background = Image.new("RGB", im.size, (255, 255, 255))
    background.paste(im)
    background.save(o_filename, 'JPEG', quality=80)
    return o_filename


def format_img(jpg_file):
    im = cv2.imread(jpg_file)

    vector = [0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 4, 4, 3, 1, 0, 0, -1, -2, -3, -4, -5, -5, -5, -5, -4, -4, -3, -1]  # 右移向量

    # im2 = im.copy()
    for i in range(len(im)):
        im[i] = numpy.append(im[i][-vector[i]:], im[i][:-vector[i]], axis=0)

    cv2.imwrite(jpg_file, im)

    return jpg_file


def read_gif_img_to_string(gif_file):
    return pytesseract.image_to_string(Image.open(format_img(convert_to_jpg(gif_file))), 'eng+chi_sim')


def main():
    pass


if __name__ == "__main__":
    main()
    pass
