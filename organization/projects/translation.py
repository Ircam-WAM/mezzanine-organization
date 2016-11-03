from modeltranslation.translator import translator, register, TranslationOptions

from organization.projects.models import *


@register(Project)
class ProjectTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(ProjectPlaylist)
class ProjectPlaylistTranslationOptions(TranslationOptions):

    pass


@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):

    pass


@register(ProjectFile)
class ProjectFileTranslationOptions(TranslationOptions):

    pass


@register(ProjectBlock)
class ProjectBlockTranslationOptions(TranslationOptions):

    pass


@register(ProjectLink)
class ProjectLinkTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(ProjectProgram)
class ProjectProgramTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(ProjectProgramType)
class ProjectProgramTypeTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(ProjectTopic)
class ProjectTopicTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(ProjectTopicPage)
class ProjectTopicPageTranslationOptions(TranslationOptions):

    fields = ('sub_title',)


@register(ProjectDemo)
class ProjectDemoTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)
