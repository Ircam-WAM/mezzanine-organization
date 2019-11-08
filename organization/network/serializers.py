from rest_framework import serializers
from django.contrib.auth.models import User
from organization.network.models import Person, Organization
from organization.core.serializers import UserPublicSerializer


# You may want to have a look at
# organization.core.serializers.UserPublicSerializer
class PersonPublicSerializer(serializers.ModelSerializer):
    # Instead of UserSerializer, we use a MethodField to avoid
    # making another object in response (= flatten the response payload)
    username = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            "first_name",
            "last_name",
            "profile_image",
            "background_image",
            "username",
            "occupation"
        )

    def get_username(self, obj):
        if not obj.user:
            return None
        return obj.user.username


class OrganizationPublicSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='organization')

    class Meta:
        model = Organization
        fields = ("name", "images", "type")


class PersonFollowSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    is_followed_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            "following",
            "followers",
            "is_followed_by_me"
        )

    def get_is_followed_by_me(self, obj):
        current_person = self.context['request'].user.person
        return obj.user \
                  .followers_users \
                  .filter(pk=current_person.pk) \
                  .exists()

    def get_followers(self, obj):
        users = UserPublicSerializer(
                User.objects.filter(person__in=obj.user.followers_users.all()),
                read_only=True,
                many=True
        )
        # As of this commit's date, organization
        # do not have a following_list attributes
        # So, organizations cannot follow.
        # So, no organization in the followers list
        return users.data

    def get_following(self, obj):
        users = UserPublicSerializer(
                obj.following_users.all(),
                read_only=True,
                many=True
        )
        orgs = OrganizationPublicSerializer(
                obj.following_organizations.all(),
                read_only=True,
                many=True
        )
        return users.data + orgs.data
