from modeltranslation.translator import translator, register, TranslationOptions

from organization.project.models import *


@register(Project)
class ProjectTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):

    fields = ('description',)


@register(ProjectLink)
class ProjectLinkTranslationOptions(TranslationOptions):
    pass


@register(ProjectBlock)
class ProjectBlockTranslationOptions(TranslationOptions):

    fields = ('title', 'content', )
