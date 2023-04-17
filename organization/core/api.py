from rest_framework import serializers, viewsets
from organization.core.models import MetaCategory


class MetaCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MetaCategory
        fields = (
            "id",
            "name",
        )
