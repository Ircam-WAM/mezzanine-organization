from modeltranslation.translator import translator, register, TranslationOptions

from organization.team.models import *


@register(Organization)
class OrganizationTranslationOptions(TranslationOptions):

    fields = ('description',)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(Team)
class TeamTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(Person)
class PersonTranslationOptions(TranslationOptions):

    fields = ('bio',)


@register(Activity)
class ActivityTranslationOptions(TranslationOptions):

    fields = ('description', 'content')
