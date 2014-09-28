# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import shutil
import sys
import os
import os.path


# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-cities-teryt',
    version='1.0.0',
    description='Polish region and city data for Django.',
    author='Łukasz Banasiak',
    author_email='lukas.banasiak@gmail.com',
    url='https://github.com/lukaszbanasiak/django-cities-teryt',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'),
    license='MIT',
    keywords='django cities teryt gus provinces counties municipalities villages districts',
    install_requires=[
        'django-autoslug',
        'lxml',
        'Unidecode',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

