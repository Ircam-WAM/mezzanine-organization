from dal import autocomplete

import dal_queryset_sequence
import dal_select2_queryset_sequence
from mezzanine.core.models import Orderable
from organization.magazine.models import Article, Topic, Brief
from organization.pages.models import CustomPage
# from mezzanine_agenda.models import Event
from organization.pages.models import DynamicContentHomeSlider, DynamicContentHomeBody

class DynamicContentHomeSliderForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            # Event.objects.all(),
            CustomPage.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-home-slider'),
    )
    # js = [static("mezzanine/js/admin/dynamic_inline.js")]

    class Meta:
        model = DynamicContentHomeSlider
        fields = ('content_object',)




class DynamicContentHomeBodyForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            # Event.objects.all(),
            CustomPage.objects.all(),
            Brief.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-home-body'),
    )

    class Meta:
        model = DynamicContentHomeBody
        fields = ('content_object',)
