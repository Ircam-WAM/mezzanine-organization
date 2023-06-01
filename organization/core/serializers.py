from django.contrib.contenttypes.models import ContentType
from .models import MetaCategory
from rest_framework import serializers, viewsets


class MetaCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MetaCategory
        fields = (
            "id",
            "name",
        )


class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = ("__all__")

