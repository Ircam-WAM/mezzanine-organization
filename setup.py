from setuptools import setup, find_packages
from organization import __version__
import subprocess

def get_long_desc():
    """Use Pandoc to convert the readme to ReST for the PyPI."""
    try:
        return subprocess.check_output(['pandoc', '-f', 'markdown', '-t', 'rst', 'README.mdown'])
    except:
        print("WARNING: The long readme wasn't converted properly")

readme = open('README.rst', 'r')
long_desc = readme.read()

setup(name='mezzanine-organization',
    version=__version__,
    description='Organization module for the Mezzo CMS',
    long_description=long_desc,
    author='Guillaume Pellerin',
    author_email='guillaume.pellerin@ircam.fr',
    url='https://github.com/Ircam-Web/mezzanine-organization',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Django==1.9.11',
        'mezzanine==4.2.3',
        'pyquery==1.2.17',
        'humanize==0.5.1',
        'django-modeltranslation==0.12',
        'django-meta==1.3.1',
        'django-bower==5.2.0',
        'django-debug-toolbar==1.6',
        'django-extensions==1.7.4',
        'django-countries==4.0',
        'django-querysetsequence==0.6.1',
        'django-autocomplete-light==3.2.1',
        'cartridge==0.12.0',
        'xlrd==1.0.0',
        'ipython',
        'gitpython',
        'pygraphviz==1.3.1',
        'sphinx_rtd_theme==0.2.4',
        'pandas==0.19.2',
        'xlwt==1.2.0',
        'DateTimeRange==0.2.8',
        'workalendar==1.0.0',
        'django-instagram==0.2.0a1',
        'django-extra-views==0.8.0',
        'bleach==2.0.0',
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
