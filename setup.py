from setuptools import setup, find_packages
from codecs import open
from os import path
import io
import re


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


with io.open("reki/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


setup(
    name='takler',

    version=version,

    description='',
    long_description=long_description,

    url='https://github.com/perillaroc/takler',

    author='perillaroc',
    author_email='perillaroc@gmail.com',

    license='Apache License, Version 2.0',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],

    keywords='',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'click',
        'Twisted',
        'thrift',
        'pyparsing'
    ],

    extras_require={
        'tests': ['pytest'],
    },

    entry_points={}
)