# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from PIL import Image
import cv2
import numpy
import pytesseract

def _format_img(img_file):
    im = cv2.imread(img_file)

    vector = (0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 4, 4, 3, 1,
              0, 0, -1, -2, -3, -4, -5, -5, -5, -5, -4, -4, -3, -1)  # 右移向量

    for i in range(len(im)):
        im[i] = numpy.append(im[i][-vector[i]:], im[i][:-vector[i]], axis=0)

    o_filename = '3.png'
    cv2.imwrite(o_filename, im)

    return o_filename


def read_img_file_to_string(img_file, x, y, w, h):
    im = Image.open(img_file)

    region = im.crop((x, y, x + w, y + h))

    region = region.resize((64, 28), Image.ANTIALIAS)
    region.save('2.png')

    return pytesseract.image_to_string(Image.open(_format_img('2.png')))
