#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from ctypes import *
from PIL import Image
import logging
import requests
from urlparse import urlsplit
from StringIO import StringIO


log = logging.getLogger(__name__)


class TessPageSegMode():
    (PSM_OSD_ONLY, PSM_AUTO_OSD, PSM_AUTO_ONLY, PSM_AUTO, PSM_SINGLE_COLUMN, PSM_SINGLE_BLOCK_VERT_TEXT,
     PSM_SINGLE_BLOCK, PSM_SINGLE_LINE, PSM_SINGLE_WORD, PSM_CIRCLE_WORD, PSM_SINGLE_CHAR, PSM_SPARSE_TEXT,
     PSM_SPARSE_TEXT_OSD, PSM_COUNT) = range(0, 14)


class Tesseract():

    MODE_TO_BPP = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32, 'CMYK': 32, 'YCbCr': 24, 'I': 32,
                   'F': 32}

    def __init__(self, lang='rus', tpath='tessdata'):
        self.tpath = tpath
        self.tesseract = cdll.LoadLibrary('libtesseract302.dll')

        self.tesseract.TessVersion.restype = c_char_p
        log.debug('TessVersion %s', self.tesseract.TessVersion())

        self.tesseract.TessBaseAPICreate.restype = c_void_p
        self.api = self.tesseract.TessBaseAPICreate()

        self.tesseract.TessBaseAPIInit3.argtypes = [c_void_p, c_char_p, c_char_p]
        self.tesseract.TessBaseAPIInit3.restype = c_int
        rc = self.tesseract.TessBaseAPIInit3(self.api, self.tpath, lang)

        self.tesseract.TessBaseAPIDelete.argtypes = [c_void_p, ]
        self.tesseract.TessBaseAPIClear.argtypes = [c_void_p, ]
        self.tesseract.TessBaseAPIEnd.argtypes = [c_void_p, ]

        if rc:
            self.tesseract.TessBaseAPIDelete(self.api)
            raise Exception("Could not initialize tesseract.")

        self.tesseract.TessBaseAPISetPageSegMode.argtypes = [c_void_p, c_int]
        self.tesseract.TessBaseAPISetVariable.argtypes = [c_void_p, c_char_p, c_char_p]
        self.tesseract.TessBaseAPIRect.argtypes = [c_void_p, c_char_p, c_int, c_int, c_int, c_int, c_int, c_int]
        self.tesseract.TessBaseAPIRect.restype = c_char_p

    def set_variable(self, s, v):
        self.tesseract.TessBaseAPISetVariable(self.api, s, v)

    def set_pagemode(self, mode):
        self.tesseract.TessBaseAPISetPageSegMode(self.api, mode)

    def from_image(self, image, basewidth=100, whitelist=None):
        if isinstance(image, Image.Image):
            log.debug('process PIL')
            if image.size[0] < basewidth:
                wpercent = (basewidth/float(image.size[0]))
                hsize = int((float(image.size[1])*float(wpercent)))
                image = image.resize((basewidth, hsize))
            if image.mode == 'RGBA':
                whiteimage = Image.new('RGB', image.size, (255, 255, 255))
                whiteimage.paste(image, (0, 0), image)
                image = whiteimage
            if image.mode != 'L':
                image = image.convert('L')
            buff_img = image.tobytes()
            w, h = image.size
            depth = self.MODE_TO_BPP[image.mode]

        if whitelist is not None:
            self.set_variable('tessedit_char_whitelist', whitelist)
        else:
            self.set_variable('tessedit_char_whitelist', '')

        rc = self.tesseract.TessBaseAPIRect(self.api, buff_img, depth/8, w*depth/8, 0, 0, w, h)
        if not rc:
            rc = ''
        return rc.strip()

    def from_url(self, url, *args, **kwargs):
        egg = urlsplit(url)
        referer = egg.geturl()
        response = requests.get(url, headers={'Referer': referer})
        img = Image.open(StringIO(response.content))
        return self.from_image(img, *args, **kwargs)

    def from_fs(self, url, *args, **kwargs):
        img = Image.open(url)
        return self.from_image(img, *args, **kwargs)

    def recognize(self, url, *args, **kwargs):
        if isinstance(url, Image.Image):
            return self.from_image(url, *args, **kwargs)
        elif url[:3].lower() in ['htt', 'ftp']:
            return self.from_url(url, *args, **kwargs)
        else:
            return self.from_fs(url, *args, **kwargs)

    def shutdown(self):
        self.tesseract.TessBaseAPIEnd(self.api)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    t = Tesseract()
    t.set_pagemode(TessPageSegMode.PSM_SINGLE_LINE)

    print t.recognize('d:\\work\\cm2\\test\\tess\\test.png', whitelist='0123456789')

    t.shutdown()
