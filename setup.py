"""Setup file"""
import codecs
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "readme.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Run tasks as a DAG'
LONG_DESCRIPTION = 'Allows you to run multiple processes as DAG'

setup(
    name="python-dag-runner",
    version=VERSION,
    author="Jatin Lal",
    author_email="jatinlal1994@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    url='https://github.com/jatinlal1994/python-dag-runner',
    install_requires=['networkx'],
    keywords=['python', 'dag', "runner"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
