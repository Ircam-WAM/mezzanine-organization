from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from versatileimagefield.serializers import VersatileImageFieldSerializer
from organization.core.serializers import UserPublicSerializer
from organization.network.serializers import PersonPublicSerializer
from organization.projects.models import (Article, Project,
                                          ProjectResidency,
                                          ProjectResidencyArticle)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "external_id")


class ProjectResidencySerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    artist = PersonPublicSerializer()

    class Meta:
        model = ProjectResidency
        fields = ("id", "title", "project", "artist")


class ArticleSerializer(serializers.ModelSerializer):
    # Do NOT validate user because it will be set by ORM
    user = UserPublicSerializer(required=False)

    class Meta:
        model = Article
        fields = ("title", "content", "user")

    # Empty user field to avoid bad insert
    def validate_user(self, user):
        return None


class Base64VersatileImageFieldSerializer(
        Base64ImageField,
        VersatileImageFieldSerializer
):
    """
    .to_representation returns URL of different sizes from VersatileImageField
    .to_internal_value decode base64 string
    """
    pass


class ResidencyBlogPublicSerializer(serializers.ModelSerializer):
    residency = serializers.PrimaryKeyRelatedField(
        queryset=ProjectResidency.objects.all(),
        required=False
    )
    article = ArticleSerializer(required=True)
    image = Base64VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__1100x600'),
            # ('cropped', 'crop__400x400')
            # Other resize available:
            # https://django-versatileimagefield.readthedocs.io/en/latest/using_sizers_and_filters.html
        ],
        represent_in_base64=False,  # Allow to represent with VersatileImage
        required=False
    )

    class Meta:
        model = ProjectResidencyArticle
        fields = ("id", "residency", "article", "image")

    def validate_residency(self, residency):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            raise serializers.ValidationError("no user")

        if residency.artist.id != user.person.id:
            raise serializers.ValidationError(
                "the residency does not belongs to request.user"
            )

        return residency

    def create(self, validated_data):
        request = self.context['request']
        article = Article.objects.create(
            **validated_data['article'],
            site_id=get_current_site(request).id,
            user=request.user,
        )
        instance = ProjectResidencyArticle.objects.create(
            residency=validated_data.get('residency'),
            image=validated_data.get('image'),
            article=article,
        )
        return instance

    def update(self, instance, validated_data):
        # Article nested model update
        updated_article = validated_data.get('article', None)
        if updated_article is not None:
            instance.article.title = (
                    updated_article.get('title', instance.article.title)
            )
            instance.article.content = (
                    updated_article.get('content', instance.article.content)
            )
            instance.article.save()

        instance.residency = validated_data.get('residency',
                                                instance.residency)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance
