#!/usr/bin/env python3

"""Trello mini CLI"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='trello-cli',
    version='0.1.0',
    url='https://github.com/tobijk/trello-cli',
    author='Tobias Koch',
    author_email='tobias.koch@gmail.com',
    license='MIT',
    packages=['de.tobijk.trello'],
    package_dir={'': 'lib'},
    platforms=['Linux'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],

    keywords='trello cli api client',
    description='Very simple Trello API client and CLI',
    long_description='Very simple Trello API client and CLI',

    entry_points = {'console_scripts': [
            "trello-cli = de.tobijk.trello.cli:Cli.main"
        ]
    }
)

