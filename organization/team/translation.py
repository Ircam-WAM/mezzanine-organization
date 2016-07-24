from modeltranslation.translator import translator, register, TranslationOptions

from organization.team.models import *


@register(Organization)
class OrganizationTranslationOptions(TranslationOptions):

    fields = ('description',)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    pass

@register(Team)
class TeamTranslationOptions(TranslationOptions):
    pass

@register(Person)
class PersonTranslationOptions(TranslationOptions):

    fields = ('bio',)


@register(Activity)
class ActivityTranslationOptions(TranslationOptions):

    fields = ('description', 'content')
