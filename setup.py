#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
manga-downloader
===================
A file compactor
"""
from setuptools import setup, find_packages

install_requires = [
    'numpy>=1.11.0',
    'ipdb>=0.9.0',
    'optparse-pretty>=0.1.1',
    'beautifulsoup4>=4.4.1',
    'lxml>=3.6.0',
]


setup(
    name="manga-downloader",
    version='0.1.2',
    author='Luiz Oliveira',
    author_email='ziuloliveira@gmail.com',
    url='https://github.com/Ziul/manga-downloader/',
    entry_points={
        'console_scripts': [
            'manga-downloader = manga:main',
            # 'main-test = main:test',
        ]},
    description='A program to download mangas',
    long_description=__doc__,
    license='GPLv3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    test_suite="tests.run.runtests",
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3',
        'Topic :: Utilities',
    ],
)
