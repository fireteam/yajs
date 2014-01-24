# -*- coding: utf-8 -*-
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README')) as f:
    doc = f.read()


setup(
    name='json-stream',
    version='1.0',
    url='http://fireteam.net/',
    license='BSD',
    author='Fireteam Ltd.',
    author_email='armin@fireteam.net',
    description='A small wrapper around YAJL\'s lexer',
    long_description=doc,
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
