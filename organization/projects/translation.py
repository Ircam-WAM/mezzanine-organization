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


@register(ProjectProgram)
class ProjectProgramTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(ProjectProgramType)
class ProjectProgramTypeTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(ProjectTopic)
class ProjectTopicTranslationOptions(TranslationOptions):

    fields = ('name', 'description')
