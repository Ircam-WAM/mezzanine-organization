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

from django.db.models.fields import CharField


class Nationality(object):
    """
    Class represents a nationality.

    >>> hungarian = Nationality('HU')
    >>> hungarian.code
    u'HU'
    >>> hungarian.name
    u'Hungarian'

    """

    def __init__(self, code):
        """
        Constructor accepts ISO 3166-1 country code.
        """
        self.code = code

    def __unicode__(self):
        return str(self.code or '')

    def __eq__(self, other):
        return self.code == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        return cmp(self.code, str(other))  # noqa: F821

    def __hash__(self):
        return hash(self.code)

    @property
    def name(self):
        """
        Return verbose name of nationality.
        """
        from .nationalities import NATIONALITIES
        for code, name in NATIONALITIES:
            if self.code == code:
                return name
        return None


class NationalityDescriptor(object):
    """
    A descriptor for nationality fields on model instances. Returns a
    Nationality when accessed.

    >>> instance.nationality.name
    u'Hungarian'

    """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))
        return Nationality(code=instance.__dict__[self.field.name])

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = str(value)


class NationalityField(CharField):
    """
    A nationality field for Django models that provides all nationalities as
    choices.
    """

    descriptor_class = NationalityDescriptor

    def __init__(self, *args, **kwargs):
        from .nationalities import NATIONALITIES
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', NATIONALITIES)
        super(CharField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def contribute_to_class(self, cls, name):
        super(NationalityField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

    def get_prep_lookup(self, lookup_type, value):
        if hasattr(value, 'code'):
            value = value.code
        return super(NationalityField, self).get_prep_lookup(lookup_type, value)

    def pre_save(self, *args, **kwargs):
        "Returns field's value just before saving."
        value = super(CharField, self).pre_save(*args, **kwargs)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        "Returns field's value prepared for saving into a database."
        # Convert the Nationality to unicode for database insertion.
        if value is None:
            return None
        return str(value)


# If south is installed, ensure that NationalityField will be introspected just
# like a normal CharField.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r"^nationalities\.fields\.NationalityField"])
except ImportError:
    pass
