# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools.dist import Distribution


with open(os.path.join(os.path.dirname(__file__), 'README')) as f:
    doc = f.read()


class BinaryDistribution(Distribution):

    def is_pure(self):
        return False


setup(
    name='yajs',
    version='1.0.2',
    url='https://github.com/fireteam/yajs',
    license='BSD',
    author='Fireteam Ltd.',
    author_email='info@fireteam.net',
    description='A small wrapper around YAJL\'s lexer',
    long_description=doc,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    packages=['yajs'],
    include_package_data=True,
    distclass=BinaryDistribution,
)
