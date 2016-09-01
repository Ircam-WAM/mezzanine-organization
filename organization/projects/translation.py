from modeltranslation.translator import translator, register, TranslationOptions

from organization.projects.models import *


@register(Project)
class ProjectTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(ProjectVideo)
class ProjectVideoTranslationOptions(TranslationOptions):

    pass


@register(ProjectAudio)
class ProjectAudioTranslationOptions(TranslationOptions):

    pass


@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):

    pass


@register(ProjectBlock)
class ProjectBlockTranslationOptions(TranslationOptions):

    pass


@register(ProjectLink)
class ProjectLinkTranslationOptions(TranslationOptions):

    pass
