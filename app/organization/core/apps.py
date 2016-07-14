from django.apps import AppConfig

from django.core.checks import register


class CoreConfig(AppConfig):

    name = 'organization.core'
    label = 'organization-core'
