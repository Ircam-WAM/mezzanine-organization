from mezzanine.accounts.forms import ProfileForm
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms


class SignUpForm(ProfileForm):
    """
    Overload Mezzanine's form to add a TOS checkbox
    """
    privacy_checkbox = forms.BooleanField(
        label=mark_safe(_('I have read and I accept the terms of use and <a href="https://www.starts.eu/starts-privacy-policy/">privacy policy of the STARTS platform</a>')),
        widget=forms.CheckboxInput,
        required=True
        )
