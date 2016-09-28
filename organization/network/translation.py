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

    fields = ('bio',)


@register(PersonActivity)
class PersonActivityTranslationOptions(TranslationOptions):

    fields = ('comments',)


@register(PersonAudio)
class PersonAudioTranslationOptions(TranslationOptions):

    pass


@register(PersonVideo)
class PersonVideoTranslationOptions(TranslationOptions):

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


@register(OrganizationAudio)
class OrganizationAudioTranslationOptions(TranslationOptions):

    pass


@register(OrganizationVideo)
class OrganizationVideoTranslationOptions(TranslationOptions):

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
