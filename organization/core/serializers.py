from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.reverse import reverse

class UserPublicSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    occupation = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "profile_image",
            "username",
            "occupation",
            "url",
            "location"
        )

    def get_location(self, obj):
        if not hasattr(obj, "person"):
            return None
        person = obj.person
        if person.city and person.country:
            return "{city} {country}".format(
                city=person.city,
                country=person.country.name
            )
        if person.city:
            return person.city
        if person.country:
            return person.country.name
        return None

    def get_url(self, obj):
        if not hasattr(obj, "person"):
            return None
        request = self.context.get("request")
        return reverse(
            'organization-network-profile-about',
            kwargs={'slug': obj.person.slug},
            request=request,
        )

    def get_profile_image(self, obj):
        if (not hasattr(obj, "person") or
                not hasattr(obj.person, "profile_image") or
                not obj.person.profile_image):
            return None
        return obj.person.profile_image.url

    def get_occupation(self, obj):
        if not hasattr(obj, "person"):
            return None
        return obj.person.occupation


class UserPrivateSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "profile_image",
            "username",
            "email"
        )

    def get_profile_image(self, obj):
        if (not hasattr(obj, "person") or
                not hasattr(obj.person, "profile_image") or
                not obj.person.profile_image):
            return None
        return obj.person.profile_image.url
