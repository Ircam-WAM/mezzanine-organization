from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_positive(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s must be positive'),
            params={'value': value},
        )


def is_percent(value):
    if value < 0 and value > 100:
        raise ValidationError(
            _('%(value)s must be an integer between 0 and 100'),
            params={'value': value},
        )

