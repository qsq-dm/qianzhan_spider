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
    im.save("verifyimage.gif")
    background = Image.new("RGB", im.size, (255, 255, 255))
    background.paste(im)
    background.save(o_filename, 'JPEG', quality=255)
    return o_filename


def _format_img(jpg_file):
    im = cv2.imread(jpg_file)

    vector = [0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 4, 4, 3, 1, 0, 0, -1, -2, -3, -4, -5, -5, -5, -5, -4, -4, -3, -1]  # 右移向量

    # im2 = im.copy()
    for i in range(len(im)):
        im[i] = numpy.append(im[i][-vector[i]:], im[i][:-vector[i]], axis=0)

    o_filename = 'verifyimage_2.jpg'
    cv2.imwrite(o_filename, im)

    return o_filename


def read_body_to_string(body):
    return pytesseract.image_to_string(Image.open(_format_img(_convert_to_jpg(io.BytesIO(body)))), 'eng')


def read_gif_file_to_string(gif_file):
    return pytesseract.image_to_string(Image.open(_format_img(_convert_to_jpg(gif_file))), 'eng')


def test():
    print read_gif_file_to_string('varifyimage.gif')

    # jpg_file = _convert_to_jpg('varifyimage.gif')

    pass

    # test()
