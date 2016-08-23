from modeltranslation.translator import translator, register, TranslationOptions

from organization.network.models import *


@register(Organization)
class OrganizationTranslationOptions(TranslationOptions):

    fields = ('description',)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):

    fields = ('name', 'description')

@register(Team)
class TeamTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(DepartmentPage)
class DepartmentTranslationOptions(TranslationOptions):

    fields = ('sub_title', 'content',)

@register(TeamPage)
class TeamTranslationOptions(TranslationOptions):

    fields = ('sub_title', 'content',)


@register(Person)
class PersonTranslationOptions(TranslationOptions):

    fields = ('bio',)


@register(PersonActivity)
class PersonActivityTranslationOptions(TranslationOptions):

    fields = ('description', 'content')


@register(PersonLink)
class PersonTranslationOptions(TranslationOptions):

    pass
