Mangafox Download Script
========================

About
-----
Mangafox Download Script is a manga downloader similar to old Onemanga Download Script (although onemanga.com shut down). It works by scraping the image URL from every page in a manga chapter. It then it downloads all the images.
This is a fork from https://github.com/techwizrd/MangaFox-Download-Script using [Multiprocessing Pool](https://docs.python.org/2/library/multiprocessing.html) to download a entire manga.

Dependencies
------------

  * Python 2.7
  * BeautifulSoup (``pip install beautifulsoup`` OR ``pip install beautifulsoup4``)

Tested on Ubuntu Linux 12.04 LTS and 12.10. It should work on any Linux, OS X, or Windows machine as long as the dependencies are installed.

Usage
-----
To download an entire series:

    ~ $ python mfdl.py [MANGA_NAME]

To download a specific chapter:

    ~ $ python mfdl.py [MANGA_NAME] [CHAPTER_NUMBER]

To download a range of manga chapter:

    ~ $ python mfdl.py [MANGA_NAME] [RANGE_START] [RANGE_END]

Examples
--------
Download all of The World God Only Knows:

    ~ $ python mfdl.py "The World God Only Knows"

Download The World God Only Knows chapter 222.5:

    ~ $ python mfdl.py "The World God Only Knows" 222.5

Download The World God Only Knows chapters 190-205:

    ~ $ python mfdl.py "The World God Only Knows" 190 205

Notes
-----
Please do not overuse and abuse this and destroy Mangafox. If you've got some cash, why not donate some to them and help them keep alive and combat server costs? I really would not like people to destroy Mangafox because of greedy downloading. Use this wisely and don't be evil.
