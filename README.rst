mezzanine-organization
=======================

The main module for Mezzo_, a complete CMS for organizations with complex workflows

.. _Mezzo: https://github.com/Ircam-Web/Mezzo

# Local install

You may want to install the project on your local environment instead of docker to use different tools (linter etc..).  
If you're using OSX, you may want to avoid using Docker For Mac because of a [high CPU utilization issue](https://github.com/docker/for-mac/issues/1759)

## Dependencies

```bash
# Python
sudo apt install \
   python-pip python3-pip pipenv

# Build libraries
sudo apt install libsasl2-dev python-dev libldap2-dev libssl-dev
sudo apt install libxml2-dev libxslt1-dev
sudo apt install install zlib1g-dev
sudo apt install zlib1g-dev
```

Tested on debian 10 (buster)

## Install

```bash
pipenv install --skip-lock --dev
touch Pipfile.lock
```

Warning: `--skip-lock` has to be used because the dependencies (Django) are not compatible.
Without this option, you'll get the following error: `Could not find a version that matches Django<1.11,<1.12,==1.10.8,>=1.11,>=1.4,>=1.6,>=1.8,>=1.8.0`

However, the Pipfile.lock has to exist in order to let IDE and editor plugins (at least for vim/ale) know that this is a Pipenv project (so they know where to find formatters binaries).
