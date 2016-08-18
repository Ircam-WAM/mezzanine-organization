from dal import autocomplete

import dal_queryset_sequence
import dal_select2_queryset_sequence

from organization.magazine.models import Article, Topic, Brief
from organization.core.models import BasicPage
from mezzanine_agenda.models import Event

class BriefForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            Event.objects.all(),
            BasicPage.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('object-autocomplete'),
    )

    class Meta:
        model = Brief
        fields = ('__all__')
