from django.contrib.contenttypes.models import ContentType
from .models import CustomPage, PageAction
from rest_framework import serializers, viewsets


class PageActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageAction
        fields = ("__all__")


class CustomPageSerializer(serializers.ModelSerializer):

    actions = PageActionSerializer(many=True, read_only=True)

    class Meta:
        model = CustomPage
        fields = ("__all__")


