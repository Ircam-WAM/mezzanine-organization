#!/bin/sh

cd /srv/doc
make install_deps
make html
make publish
make readme
