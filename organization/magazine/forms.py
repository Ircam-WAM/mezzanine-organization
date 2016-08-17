from dal import autocomplete

import dal_queryset_sequence
import dal_select2_queryset_sequence

from organization.magazine.models import Article, Topic, Brief


class BriefForm(autocomplete.FutureModelForm):

    # selected_object = forms.ModelChoiceField(
    #     queryset=ContentType.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='object-autocomplete')
    # )

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            Topic.objects.all(),
            # ContentType.objects.all(),
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('object-autocomplete'),
    )

    class Meta:
        model = Brief
        fields = ('__all__')
