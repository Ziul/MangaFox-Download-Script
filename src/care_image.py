#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
from os import listdir
from scipy.stats import mode

_width = 758
_height = 1024


class MeanImages(object):

    """docstring for MeanImages"""

    def __init__(self, root):
        super(MeanImages, self).__init__()
        self.files = []

        for files_name in listdir(root):
            if '.jpg' in files_name:
                self.files.append(root + '/' + files_name)

    def find_mode(self):
        self.sizes = []
        for _file in self.files:
            img = Image.open('./' + _file)
            self.sizes.append(img.size)
            # print str(_file) + ' -> ' + str(img.size)

        _width, _height = mode(self.sizes)[0][0]

    def resize_files(self):
        # self.find_mode()
        for _file in self.files:
            img = Image.open('./' + _file)
            img.thumbnail((_width, _height), Image.ANTIALIAS)
            img.save('./' + _file)


def resize_files_from_dir(root):
    k = MeanImages(root)
    print "Resising files in " + root
    k.resize_files()
