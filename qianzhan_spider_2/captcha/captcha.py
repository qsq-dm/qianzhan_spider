# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

from PIL import Image
import cv2
import numpy
import pytesseract
import io


def _convert_to_jpg(gif_file):
    o_filename = 'verifyimage.jpg'

    im = Image.open(gif_file)
    background = Image.new("RGB", im.size, (255, 255, 255))
    background.paste(im)
    background.save(o_filename, 'JPEG', quality=8)
    return o_filename


def _format_img(jpg_file):
    im = cv2.imread(jpg_file)

    vector = [0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 4, 4, 3, 1, 0, 0, -1, -2, -3, -4, -5, -5, -5, -5, -4, -4, -3, -1]  # 右移向量

    # im2 = im.copy()
    for i in range(len(im)):
        im[i] = numpy.append(im[i][-vector[i]:], im[i][:-vector[i]], axis=0)

    cv2.imwrite(jpg_file, im)

    return jpg_file


def read_body_to_string(body):
    return pytesseract.image_to_string(Image.open(_format_img(_convert_to_jpg(io.BytesIO(body)))), 'eng')
