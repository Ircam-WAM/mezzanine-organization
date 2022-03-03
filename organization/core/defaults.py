from mezzanine.conf import register_setting
from django.utils.translation import ugettext_lazy as _


register_setting(
    name="TINYMCE_SETUP_JS",
    description=_(
        "URL for the JavaScript file (relative to ``STATIC_URL``) "
        "that handles configuring TinyMCE when the default "
        "``RICHTEXT_WIDGET_CLASS`` is used."
    ),
    editable=True,
    default="mezzanine/js/tinymce_setup.js",
)
