#!/usr/bin/env python
# encoding: utf-8

from os import walk, system, path, makedirs

from sys import argv
import sys
import optparse
from functools import reduce
import urllib
import glob
import shutil
import threading
from functools import partial
from os import listdir, path
import re
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from zipfile import ZipFile
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
from contextlib import closing
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from itertools import islice

__version__ = '0.8'
URL_BASE = "http://mangafox.me/"
_MAX_PEERS = 2

_parser = optparse.OptionParser(
    usage="""%prog MANGA_NAME RANGE_START RANGE_END

Examples:
Download all of The World God Only Knows:

    ~ $ python mfdl.py "The World God Only Knows"

Download The World God Only Knows chapter 222.5:

    ~ $ python mfdl.py "The World God Only Knows" 222.5

Download The World God Only Knows chapters 190-205:

    ~ $ python mfdl.py "The World God Only Knows" 190 205
        """,
    description="Build CBZ files from each chapter of the selected Manga",
    version='Mangafox Download Script v' + __version__
)

try:
    if len(argv) < 2:
        argv[2] = ''
        argv[3] = ''
    _parser.add_option("-q", "--quiet",
                       dest="verbose",
                       action="store_false",
                       help="suppress non error messages",
                       default=True
                       )
    _parser.add_option("-n", "--name",
                       dest="manga_name",
                       action="store",
                       help="Name of the Manga",
                       default=argv[1]
                       )
    _parser.add_option("-f", "--first",
                       dest="first",
                       action="store",
                       help="First chapter number from the manga to be download",
                       # default=argv[2]
                       )
    _parser.add_option("-l", "--last",
                       dest="last",
                       action="store",
                       help="Last chapter number from the manga to be download",
                       # default=argv[3]
                       )

    _parser.add_option("-r", "--resize",
                       dest="resize",
                       action="store_true",
                       help="suppress non error messages",
                       default=False
                       )
except IndexError:
    _parser.print_help()
    exit(-1)
(_options, _args) = _parser.parse_args()
L = threading.Lock()


def order(name1, name2):
    name1 = name1.split('/')[-1]
    name2 = name2.split('/')[-1]
    return int(float(name2.split('c')[1]) - float(name1.split('c')[1]))


def DoVolumes(dirsl):
        root, k = dirsl[0].split('/')
        k = k.split('c')[0][1:]
        dirname = ''
        print "\nMounting volume %s: " % k
        for i in reversed(dirsl):
            dirname = './%s' % i
            images = glob.glob(dirname + '/*.jpg')
            zipname = glob.glob(path.abspath(root))[
                0] + '/%s_%s.cbz' % (root, k)
            with ZipFile(zipname, 'a') as zipfile:
                # if _options.verbose:
                #     print('writing {0} to {1}'.format(i, zipname))
                for filename in images:
                    # print filename
                    zipfile.write(filename)
                closing(zipfile)


def Dir2Cbz(root):
    if(root[-1] == '/'):
        root = root[:-1]
    dirl = [x[0] for x in walk(root)]
    dirsl = dirl[1:]
    dirs = ''
    volumes = {}

    _pool = ThreadPool(processes=20)
    for i in dirsl:
        name = i.split('/')[-1]
        if name.split('c')[0][1:] not in volumes:
            volumes[name.split('c')[0][1:]] = []
        volumes[name.split('c')[0][1:]].append(i)

    if _options.resize:
        from care_image import resize_files_from_dir
        result = _pool.map(resize_files_from_dir, dirsl)

    result = _pool.map(DoVolumes, [x[1] for x in volumes.items()])


def Dir2Pdf(root):
    if(root[-1] == '/'):
        root = root[:-1]
    dirl = [x[0] for x in walk(root)]
    dirsl = dirl[1:]
    dirs = ''
    volumes = {}

    # _pool = Pool(processes=_MAX_PEERS)
    for i in dirsl:
        print i
        name = i.split('/')[-1]
        if name.split('c')[0][1:] not in volumes:
            volumes[name.split('c')[0][1:]] = []
        volumes[name.split('c')[0][1:]].append(i)

    #result = _pool.map(DoVolumes, [x[1] for x in volumes.items()])
    for k in volumes.keys():
        dirsl = sorted(volumes[k], cmp=order)
        dirs = ''
        for i in reversed(dirsl):
            dirs += ' \"%s\"/*' % i
        cmd = "convert " + dirs + ' \"%s/%s_%s.pdf\"' % (root, root, k)

        print "Mounting volume %s: " % k
        # print cmd
        system(cmd)


if __name__ == '__main__':
    if(_options.manga_name[-1] == '/'):
        _options.manga_name = _options.manga_name[:-1]
    Dir2Cbz(_options.manga_name)
