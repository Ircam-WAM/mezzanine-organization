from modeltranslation.translator import translator, register, TranslationOptions
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from organization.job.models import *


@register(JobOffer)
class JobOfferTranslationOptions(TranslationOptions):

    fields = ('title', 'content')
