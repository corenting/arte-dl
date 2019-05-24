"""Packaging settings."""
from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from arte_dl import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--junitxml=test-results.xml', '--cov=arte_dl', 'tests/'])
        raise SystemExit(errno)


class RunLint(Command):
    """Run lint."""
    description = 'run lint'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run lint!"""
        errno = call(['flake8', '--exclude=venv', '--max-line-length=120'])
        raise SystemExit(errno)


setup(
    name='arte-dl',
    version=__version__,
    description='CLI video downloader for arte.tv.',
    long_description=long_description,
    url='https://github.com/corenting/arte_dl',
    author='corenting',
    author_email='corenting@gmail.com',
    license='UNLICENSE',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='cli',
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests'],
    extras_require={
        'dev': ['coverage', 'flake8', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'arte_dl=arte_dl.cli:main',
        ],
    },
    cmdclass={
        'test': RunTests,
        'lint': RunLint
    }
)
