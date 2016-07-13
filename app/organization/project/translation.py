from modeltranslation.translator import translator, register, TranslationOptions

from organization.project.models import *


@register(Project)
class ProjectTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')
