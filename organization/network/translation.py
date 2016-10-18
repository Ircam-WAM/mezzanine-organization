from modeltranslation.translator import translator, register, TranslationOptions

from organization.network.models import *


@register(Organization)
class OrganizationTranslationOptions(TranslationOptions):

    fields = ('description',)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(DepartmentPage)
class DepartmentPageTranslationOptions(TranslationOptions):

    fields = ('sub_title', 'content',)


@register(Team)
class TeamTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(TeamPage)
class TeamTranslationOptions(TranslationOptions):

    fields = ('sub_title', 'content',)


@register(Person)
class PersonTranslationOptions(TranslationOptions):

    fields = ('description','bio',)


@register(PersonActivity)
class PersonActivityTranslationOptions(TranslationOptions):

    fields = ('comments',)


@register(PersonPlaylist)
class PersonPlaylistTranslationOptions(TranslationOptions):

    pass


@register(PersonLink)
class PersonLinkTranslationOptions(TranslationOptions):

    pass


@register(PersonImage)
class PersonImageTranslationOptions(TranslationOptions):

    pass


@register(PersonFile)
class PersonFileTranslationOptions(TranslationOptions):

    pass


@register(PersonBlock)
class PersonBlockTranslationOptions(TranslationOptions):

    pass


@register(OrganizationPlaylist)
class OrganizationTranslationOptions(TranslationOptions):

    pass


@register(OrganizationLink)
class OrganizationLinkTranslationOptions(TranslationOptions):

    pass


@register(OrganizationImage)
class OrganizationImageTranslationOptions(TranslationOptions):

    pass


@register(OrganizationBlock)
class OrganizationBlockTranslationOptions(TranslationOptions):

    pass


@register(PersonListBlock)
class PersonListBlockTranslationOptions(TranslationOptions):

    pass


@register(PersonListBlockInline)
class PersonListBlockInlineTranslationOptions(TranslationOptions):

    pass


@register(PageCustomPersonListBlockInline)
class PageCustomPersonListBlockInlineTranslationOptions(TranslationOptions):

    pass


@register(ActivityGrade)
class ActivityGradeTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(ActivityFunction)
class ActivityFunctionTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(ActivityFramework)
class ActivityFrameworkTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(ActivityStatus)
class ActivityGradeTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(TrainingTopic)
class TrainingTopicTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(TrainingType)
class TrainingTypeTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(TrainingLevel)
class TrainingLevelTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(TrainingSpeciality)
class TrainingSpecialityTranslationOptions(TranslationOptions):

    fields = ['name', 'description']
