from setuptools import setup, find_packages
from organization import __version__
import subprocess
import json


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

conf = json.loads(open('conf.json', 'r').read())


def get_requirements():
    requirements = [
        "Django==2.2.*",
        # "mezzanine==v5.0.0-rc.1", not availbale on Pip and we use fork
        "django-modeltranslation==0.17.3",
        "django-meta==2.0",
        "django-bower==5.2.0",
        "django-debug-toolbar==3.2.1",
        "django-extensions==2.2.5",
        "django-countries==5.3",
        "django-querysetsequence==0.12",
        "django-autocomplete-light==3.8.2",
        "django-hijack==3.0.0",
        "django-instagram==0.3.1",
        "django-compat==1.0.15",
        "django-guardian==1.4.9",
        "django-auth-ldap==1.2.17",
        "django-extra-views==0.8.0",
        "django-extended-choices==1.3",
        # "django-postman==3.6.1", useless
        "django-taggit==0.22.2",
        "djangorestframework==3.8.2",
        # "django-cors-middleware==1.3.1",  Deprectated : https://github.com/zestedesavoir/django-cors-middleware  # noqa: E501
        "django-allauth==0.34.0",
        "xlrd==1.0.0",
        "pytz==2021.1",
        "pandas==1.1.5",
        "xlwt==1.2.0",
        "DateTimeRange==0.2.8",
        "workalendar==1.0.0",
        "bleach==2.1.3",
        "lxml==4.2.0",

        "pyquery",
        "humanize",
        "ipython",
        "gitpython",
        "pygraphviz",
        "selenium==3.11.0",
        "coverage>=5.1",
    ]
    if conf["onthology"]:
        requirements += "rdflib",
    return requirements


def get_dependency_links():
    if conf["onthology"]:
        return [
            "https://github.com/Ircam-Web/django-rdf-io.git@master#egg=django-rdf-io",
            "https://github.com/Ircam-Web/django-skosxl.git@master#egg=django-skosxl"
        ]
    else:
        return []


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
    install_requires=get_requirements(),
    dependency_links=get_dependency_links(),
)
