import os
from setuptools import setup

'''
A module for use with a vidispine database. Classes for defining database, items and storages
'''
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'vidispine',
    version = '1.0',
    author = 'Peter Lambro',
    author_email = 'peterlambro@gmail.com',
    description = ('a set of classes and functions for working with a vidispine database'
        ),
    license = 'MIT',
    keywords = 'vidispine',
    url = 'https://github.com/lambrocalrissian/vidispine',
    packages=['vidispine'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia',
        'License :: OSI Approved :: MIT License',
    ],
)