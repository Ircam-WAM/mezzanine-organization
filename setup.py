from setuptools import setup, find_packages
from organization import __version__
import subprocess


def get_long_desc():
    """Use Pandoc to convert the readme to ReST for the PyPI."""
    try:
        return subprocess.check_output(
            ['pandoc', '-f', 'markdown', '-t', 'rst', 'README.mdown']
        )
    except Exception:
        print("WARNING: The long readme wasn't converted properly")


readme = open('README.rst', 'r')
long_desc = readme.read()

setup(
    name='mezzanine-organization',
    version=__version__,
    description='Organization module for the Mezzo CMS',
    long_description=long_desc,
    author='Guillaume Pellerin',
    author_email='guillaume.pellerin@ircam.fr',
    url='https://github.com/Ircam-Web/mezzanine-organization',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
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
    install_requires=[
        "Django==1.11.*",
        "pyquery",
        "humanize",
        "django-modeltranslation==0.12.2",
        "django-meta==1.3.1",
        "django-bower==5.2.0",
        "django-debug-toolbar==1.9.1",
        "django-extensions==2.2.5",
        "django-countries==5.3",
        "django-querysetsequence==0.12",
        "django-autocomplete-light==3.5.1",
        "mezzanine==4.3.1",
        "xlrd==1.0.0",
        "ipython",
        "gitpython",
        "pygraphviz",
        "pandas==1.1.5",
        "xlwt==1.2.0",
        "DateTimeRange==0.2.8",
        "workalendar==1.0.0",
        "django-instagram==0.3.1",
        "django-extra-views==0.8.0",
        "bleach==2.1.3",
        "django-hijack==2.1.10",
        "django-hijack-admin==2.1.10",
        "django-compat==1.0.14",
        "django-guardian==1.4.9",
        "django-auth-ldap==1.2.17",
        "selenium==3.11.0",
        "lxml==4.2.0",
        "django-extended-choices==1.0.2",
        "rdflib",
        "django-postman==3.6.1",
        "coverage==4.5.1",
        "django-taggit==0.22.2",
        "djangorestframework==3.8.2",
        # "django-cors-middleware==1.3.1",
        "django-allauth==0.33.0",
    ],
    dependency_links=[
        "https://github.com/Ircam-Web/django-rdf-io.git@master#egg=django-rdf-io",
        "https://github.com/Ircam-Web/django-skosxl.git@master#egg=django-skosxl"
    ],
)
