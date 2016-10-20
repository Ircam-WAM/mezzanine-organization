from django.conf import settings # import the settings file


def static(request):

    return {'CURRENT_SEASON': settings.CURRENT_SEASON,
            'CURRENT_SEASON_STYLED': settings.CURRENT_SEASON_STYLED}
