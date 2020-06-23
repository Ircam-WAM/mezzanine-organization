# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- encoding: utf-8 -*-
# This file is distributed under the same license as the Django package.
#
from __future__ import unicode_literals

# The *_FORMAT strings use the Django date format syntax,
# see http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
DATE_FORMAT = 'j F Y'
DATE_EVENT_FORMAT = 'D j F'
DATE_EVENT_FORMAT_Y = 'D j F Y'
WEEK_DAY_FORMAT = 'D j'
WEEK_DAY_FORMAT_Y = 'D j Y'
TIME_FORMAT = 'H\hi'
DATETIME_FORMAT = 'j F Y H:i'
YEAR_MONTH_FORMAT = 'F Y'
MONTH_DAY_FORMAT = 'j F'
SHORT_DATE_FORMAT = 'j N Y'
SHORT_DATETIME_FORMAT = 'j N Y H:i'
FIRST_DAY_OF_WEEK = 1  # Monday

# The *_INPUT_FORMATS strings use the Python strftime format syntax,
# see http://docs.python.org/library/datetime.html#strftime-strptime-behavior
DATE_INPUT_FORMATS = [
    '%d/%m/%Y', '%d/%m/%y',  # '25/10/2006', '25/10/06'
    '%d.%m.%Y', '%d.%m.%y',  # Swiss [fr_CH), '25.10.2006', '25.10.06'
    # '%d %B %Y', '%d %b %Y', # '25 octobre 2006', '25 oct. 2006'
]
DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y %H:%M:%S',     # '25/10/2006 14:30:59'
    '%d/%m/%Y %H:%M:%S.%f',  # '25/10/2006 14:30:59.000200'
    '%d/%m/%Y %H:%M',        # '25/10/2006 14:30'
    '%d/%m/%Y',              # '25/10/2006'
    '%d.%m.%Y %H:%M:%S',     # Swiss [fr_CH), '25.10.2006 14:30:59'
    '%d.%m.%Y %H:%M:%S.%f',  # Swiss (fr_CH), '25.10.2006 14:30:59.000200'
    '%d.%m.%Y %H:%M',        # Swiss (fr_CH), '25.10.2006 14:30'
    '%d.%m.%Y',              # Swiss (fr_CH), '25.10.2006'
]
DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '\xa0'  # non-breaking space
NUMBER_GROUPING = 3
