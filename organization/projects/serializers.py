from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from organization.projects.models import (Article, Person, Project,
                                          ProjectResidency,
                                          ProjectResidencyArticle)


class PersonPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("first_name", "last_name", "profile_image")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "external_id")


class ArticleSerializer(serializers.ModelSerializer):
    # Do NOT validate user because it will be set by DB / ORM
    user = PersonPublicSerializer(required=False)

    class Meta:
        model = Article
        fields = ("title", "content", "user")

    # Empty user field to avoid bad insert
    def validate_user(self, user):
        return None

class ProjectResidencySerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    artist = PersonPublicSerializer()

    class Meta:
        model = ProjectResidency
        fields = ("id", "title", "project", "artist")


class ResidencyBlogPublicSerializer(serializers.ModelSerializer):
    residency = serializers.PrimaryKeyRelatedField(
        queryset=ProjectResidency.objects.all()
    )
    article = ArticleSerializer()

    class Meta:
        model = ProjectResidencyArticle
        fields = ("residency", "article")

    def create(self, validated_data):
        request = self.context['request']
        article = Article.objects.create(
            **validated_data['article'],
            site_id=get_current_site(request).id,
            user=request.user,
        )
        instance = ProjectResidencyArticle.objects.create(
            residency=validated_data['residency'],
            article=article
        )
        return instance

    def update(self, instance, validated_data):
        raise NotImplementedError
