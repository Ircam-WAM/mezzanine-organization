from rest_framework import serializers
from django.contrib.auth.models import User

class UserPublicSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "profile_image", "username")

    def get_profile_image(self, obj):
        if not obj.person or not obj.person.profile_image:
            return None
        return obj.person.profile_image

class UserPrivateSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "profile_image",
                  "username", "email")

    def get_profile_image(self, obj):
        if not obj.person or not obj.person.profile_image:
            return None
        return obj.person.profile_image
