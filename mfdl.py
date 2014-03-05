#!/usr/bin/env python
# encoding: utf-8


"""Mangafox Download Script by Kunal Sarkhel <theninja@bluedevs.net>"""

__author__ = 'Kunal Sarkhel. Revised by Luiz Fernando Gomes de Oliveira'
__version__ = '0.8'

import sys
import os
import urllib
import glob
import shutil
import re
from multiprocessing import Pool
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

URL_BASE = "http://mangafox.me/"
MAX_PEERS = 15

import optparse
_parser = optparse.OptionParser(
		usage = "%prog MANGA_NAME [RANGE_START] [RANGE_END]",
		description = "Build CBZ files from each chapter of the selected Manga",
		version = __version__
		)
#quiet options
_parser.add_option("-q", "--quiet",
	dest = "verbose",
	action = "store_false",
	help = "suppress non error messages",
	default = True
)
#conservative options
_parser.add_option("-c",
	dest = "conservative",
	action = "store_true",
	help = "Avoid removing the *.jpg after have built the *.cbz",
	default = False
)

(_options, args) = _parser.parse_args()
def get_page_soup(url):
	"""Download a page and return a BeautifulSoup object of the html"""
	with closing(urllib.urlopen(url)) as html_file:
		return BeautifulSoup(html_file.read())


def get_chapter_urls(manga_name):
	"""Get the chapter list for a manga"""
	replace = lambda s, k: s.replace(k, '_')
	manga_url = reduce(replace, [' ', '-'], manga_name.lower())
	url = '{0}manga/{1}'.format(URL_BASE, manga_url)
	#print('Url: ' + url)
	soup = get_page_soup(url)
	manga_does_not_exist = soup.find('form', {'id': 'searchform'})
	if manga_does_not_exist:
		search_sort_options = 'sort=views&order=za'
		url = '{0}/search.php?name={1}&{2}'.format(URL_BASE,
												   manga_url,
												   search_sort_options)
		soup = get_page_soup(url)
		results = soup.findAll('a', {'class': 'series_preview'})
		error_text = 'Error: Manga \'{0}\' does not exist'.format(manga_name)
		error_text += '\nDid you meant one of the following?\n  * '
		error_text += '\n  * '.join([manga.text for manga in results][:10])
		sys.exit(error_text)
	warning = soup.find('div', {'class': 'warning'})
	if warning and 'licensed' in warning.text:
		sys.exit('Error: ' + warning.text)
	chapters = OrderedDict()
	links = soup.findAll('a', {'class': 'tips'})
	if(len(links) == 0):
		sys.exit('Error: Manga either does not exist or has no chapters')
	replace_manga_name = re.compile(re.escape(manga_name.replace('_', ' ')),
									re.IGNORECASE)
	for link in links:
		chapters[replace_manga_name.sub('', link.text).strip()] = link['href']
	return chapters


def get_page_numbers(soup):
	"""Return the list of page numbers from the parsed page"""
	raw = soup.findAll('select', {'class': 'm'})[0]
	return (html['value'] for html in raw.findAll('option'))


def get_chapter_image_urls(url_fragment):
	"""Find all image urls of a chapter and return them"""
	#print('Getting chapter urls')
	url_fragment = os.path.dirname(url_fragment) + '/'
	chapter_url = url_fragment
	chapter = get_page_soup(chapter_url)
	pages = get_page_numbers(chapter)
	image_urls = []
	#print('Getting image urls...')
	for page in pages:
		#print('url_fragment: {0}'.format(url_fragment))
		#print('page: {0}'.format(page))
		#print('Getting image url from {0}{1}.html'.format(url_fragment, page))
		page_soup = get_page_soup(chapter_url + page + '.html')
		images = page_soup.findAll('img', {'id': 'image'})
		if images:
			image_urls.append(images[0]['src'])
	return image_urls


def get_chapter_number(url_fragment):
	"""Parse the url fragment and return the chapter number."""
	return ''.join(url_fragment.rsplit("/")[5:-1])


def download_urls(image_urls, manga_name, chapter_number):
	"""Download all images from a list"""
	download_dir = '{0}/{1}/'.format(manga_name, chapter_number)
	if os.path.exists(download_dir):
		shutil.rmtree(download_dir)
	os.makedirs(download_dir)
	for i, url in enumerate(image_urls):
		filename = './{0}/{1}/{2:03}.jpg'.format(manga_name, chapter_number, i)
		#print('Downloading {0} to {1}'.format(url, filename))
		urllib.urlretrieve(url, filename)


def make_cbz(dirname):
	"""Create CBZ files for all JPEG image files in a directory."""
	zipname = dirname + '.cbz'
	images = glob.glob(os.path.abspath(dirname) + '/*.jpg')
	with closing(ZipFile(zipname, 'w')) as zipfile:
		for filename in images:
			#print('writing {0} to {1}'.format(filename, zipname))
			zipfile.write(filename)


def download_manga_range(manga_name, range_start, range_end):
	"""Download a range of a chapters"""
	print('Getting chapter urls')
	chapter_urls = get_chapter_urls(manga_name)
	iend = chapter_urls.keys().index(range_start) + 1
	istart = chapter_urls.keys().index(range_end)
	for url_fragment in islice(chapter_urls.itervalues(), istart, iend):
		chapter_number = get_chapter_number(url_fragment)
		print('===============================================')
		print('Chapter ' + chapter_number)
		print('===============================================')
		image_urls = get_chapter_image_urls(url_fragment)
		download_urls(image_urls, manga_name, chapter_number)
		download_dir = './{0}/{1}'.format(manga_name, chapter_number)
		make_cbz(download_dir)
		if not _options.conservative:
			shutil.rmtree(download_dir)

def get_manga(data):
	""" Fast sequence to get a manga """
	manga_name = sys.argv[1]
	chapter_number = data[0]
	url_fragment = data[1]
	chapter_number = get_chapter_number(url_fragment)
	#print('===============================================')
	print('Chapter ' + chapter_number)
	#print('===============================================')
	image_urls = get_chapter_image_urls(url_fragment)
	download_urls(image_urls, manga_name, chapter_number)
	download_dir = './{0}/{1}'.format(manga_name, chapter_number)
	make_cbz(download_dir)
	if not _options.conservative:
			shutil.rmtree(download_dir)

def download_manga(manga_name, chapter_number=None):
	"""Download all chapters of a manga"""
	_pool = Pool(processes=MAX_PEERS)
	chapter_urls = get_chapter_urls(manga_name)
	if chapter_number:
		if chapter_number in chapter_urls:
			url_fragment = chapter_urls[chapter_number]
		else:
			error_text = 'Error: Chapter {0} does not exist'
			sys.exit(error_text.format(chapter_number))
		chapter_number = get_chapter_number(url_fragment)
		print('===============================================')
		print('Chapter ' + chapter_number)
		print('===============================================')
		image_urls = get_chapter_image_urls(url_fragment)
		download_urls(image_urls, manga_name, chapter_number)
		download_dir = './{0}/{1}'.format(manga_name, chapter_number)
		make_cbz(download_dir)
		if not _options.conservative:
			shutil.rmtree(download_dir)
	else:
		result = _pool.map_async(get_manga, chapter_urls.items())
		result.wait()		

if __name__ == '__main__':
	if len(args) == 3:
		download_manga_range(args[0], args[1], args[2])
	elif len(args) == 2:
		download_manga(args[0], args[1])
	elif len(args) == 1:
		download_manga(args[0])
	else:
		print('USAGE: mfdl.py [MANGA_NAME]')
		print('       mfdl.py [MANGA_NAME] [CHAPTER_NUMBER]')
		print('       mfdl.py [MANGA_NAME] [RANGE_START] [RANGE_END]')