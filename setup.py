# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='twitterbias',
    version='0.1.0',
    description='Twitter Sentiment Analysis',
    long_description=readme,
    author='Josh Hicks',
    author_email='josh.hicks@live.com',
    url='https://github.com/johicks/twitterbias',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

