#!/usr/bin/env python3
# encoding: utf-8

import urllib
from urllib.request import urlopen
import os
from numpy import arange
from contextlib import closing
from mangargs import _parser
from bs4 import BeautifulSoup


_URL_BASE = {}
_URL_BASE['MangaFox'] = ["http://mangafox.me/",
                         'http://z.mfcdn.net/store/manga/19709/001.0/compressed/j001.jpg']

(_options, _args) = _parser.parse_args()
URL_BASE = _URL_BASE['MangaFox'][0]


class Manga(object):

    """docstring for Manga"""

    url = ''
    volume = 0
    chapter = 0.0
    name = ''
    images = {}

    def __init__(self, arg):
        super(Manga, self).__init__()
        self.chapter = arg
        self.images['url'] = []
        self.images['path'] = []

    def __str__(self):
        return str(self.images['url'])
        if self.chapter == int(self.chapter):
            return "Chapter {0:2.0f}   [ {1} ]:{2} ".format(self.chapter, self.name.decode('utf-8'), self.url)
        else:
            return "Chapter {0:2.1f} [ {1} ]:{2} ".format(self.chapter, self.name.decode('utf-8'), self.url)

    def get_url(self):
        pass


class MangaVolume(object):

    """docstring for MangaVolume"""

    volume = 0
    chapters = []
    url = ''

    def __init__(self, arg):
        super(MangaVolume, self).__init__()
        self.volume = arg

    def sort(self):
        self.chapters = sorted(self.chapters, key=lambda x: x.chapter)

    def append(self, item):
        self.chapters.append(item)

    def __str__(self):
        data = '%s #%s:\n' % (self.name, self.volume)
        for i in reversed(self.chapters):
            try:
                data += "\t%s\n" % str(i)
            except Exception as e:
                print("error with chapter %.1f (%s)" % (i.chapter, str(e)))
        return str(data)


class MangaBook(MangaVolume):

    """docstring for MangaBook"""

    title = ''
    volumes = []
    url = ''

    def __init__(self, arg, verbose=False):
        # super(MangaBook, self).__init__(arg)
        self.name = arg
        self.get_url()
        self.verbose = verbose

    def get_url(self):
        replace = lambda s, k: s.replace(k, '_')
        manga_url = self.name.lower().replace(' ', '-')
        self.url = '{0}manga/{1}/'.format(URL_BASE, manga_url)

    def get_chapters(self):
        """Download a page and return a BeautifulSoup object of the html"""
        url_fragment = os.path.dirname(self.url) + '/'
        with closing(urlopen(url_fragment)) as html_file:
            soup = BeautifulSoup(html_file.read(), 'lxml')
            # raw = soup.findAll('select', {'class': 'm'})
            names = soup.findAll('span', {'class': 'title nowrap'})
            raw = soup.findAll('a', {'class': 'tips'})
            volume = 0
            v = MangaVolume(volume)
            for r, n in zip(raw, names):
                # print "%s (%s): %s " % (r.string, n.string, r['href'])
                m = Manga(float(r.string.split(' ')[-1]))
                m.name = n.string.encode('utf-8')
                m.url = r['href']
                m.get_url()
                if volume == m.url.split('/')[-3].split("v")[-1]:
                    v.append(m)
                else:
                    volume = m.url.split('/')[-3].split("v")[-1]
                    self.append(v)
                    v.name = self.name
                    del v
                    v = MangaVolume(volume)
                    v.append(m)
        return (html.findAll('title nowrap')['title nowrap'] for html in raw)

    def append(self, item):
        self.volumes.append(item)

    def sort(self):
        self.volumes = sorted(self.volumes, key=lambda x: x.volumes)

    def __str__(self):
        data = '%s (%d volumes)' % (self.name, len(self.volumes))
        if self.verbose:
            for volume in self.volumes:
                data += '\n' + str(volume)
        return data


def main():
    v = MangaBook(' '.join(_args), verbose=_options.verbose)
    v.get_chapters()
    print(v)

if __name__ == '__main__':
    v = MangaBook("Shingeki no Kyojin")
    v.get_chapters()
    print(v.volumes[0])
    v.sort()
    # print(v)
