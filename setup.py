# -*- coding: utf-8 -*-
"""
JSON Stream
~~~~~~~~~~~

JSON stream is a simple package that provides a wrapper to the YAJL
JSON lexer functions that allow tokenization of streams of JSON data
without having to buffer up the whole data.
"""
from setuptools import setup


setup(
    name='json-stream',
    version='1.0',
    url='http://fireteam.net/',
    license='BSD',
    author='Fireteam Ltd.',
    author_email='armin@fireteam.net',
    description='A small wrapper around YAJL\'s lexer',
    long_description=__doc__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    packages=['jsonstream'],
    include_package_data=True,
)
