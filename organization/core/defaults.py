from mezzanine.conf import register_setting
from django.utils.translation import ugettext_lazy as _


register_setting(
    name="TINYMCE_SETUP_JS",
    description=_("URL for the JavaScript file (relative to ``STATIC_URL``) "
        "that handles configuring TinyMCE when the default "
        "``RICHTEXT_WIDGET_CLASS`` is used."),
    editable=True,
    default="mezzanine/js/tinymce_setup.js",
)

# register_setting(
#     name="HAL_URL_CSS",
#     label="HAL URL CSS",
#     description="custom css style",
#     editable=True,
#     #default="&css=//%s/static/css/index.min.css",
#     default="coucou",
#     translatable=False
# )

# register_setting(
#     name="HAL_LIMIT_PUB",
#     label="HAL LIMIT PUB",
#     description="Parameter to limit number of publications",
#     editable=True,
#     default="&NbAffiche=",
# )

# register_setting(
#     name="HAL_LABOS_EXP",
#     label="HAL LABOS EXP",
#     description="Parameter labos exp",
#     editable=True,
#     default="&labos_exp=",
#     translatable=False
# )

# register_setting(
#     name="HAL_YEAR_BEGIN",
#     label="HAL YEAR BEGIN",
#     description="Minimum year to request publications",
#     editable=True,
#     default=1977,
#     translatable=False
# )

# register_setting(
#     name="HAL_URL",
#     label="HAL URL",
#     description="Base url for HAL requests",
#     editable=True,
#     default="//haltools.archives-ouvertes.fr/Public/afficheRequetePubli.php?affi_exp=Ircam&CB_auteur=oui&CB_titre=oui" \
#                         "&CB_article=oui&langue=Anglais&tri_exp=annee_publi&tri_exp2=typdoc&tri_exp3=date_publi" \
#                         "&ordre_aff=TA&Fen=Aff&Formate=Oui",
#     translatable=False
# )