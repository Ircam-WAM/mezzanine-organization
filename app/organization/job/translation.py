from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from organization.job.models import *


@register(JobOffer)
class JobOfferTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(JobResponse)
class JobResponseTranslationOptions(TranslationOptions):

    pass

@register(Candidacy)
class JobResponseTranslationOptions(TranslationOptions):

    fields = ('title', 'content', 'text_button_internal', 'text_button_external', )


@register(CandidacyImage)
class JobResponseTranslationOptions(TranslationOptions):

    pass
