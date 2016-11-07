from django.conf import settings # import the settings file
from datetime import datetime, date

def static(request):
    date_now = datetime.now()
    CURRENT_SEASON = int(date_now.year) - 1 if datetime(date_now.year, 1,1) <= date_now and date_now <= datetime(date_now.year, 7, 31) else date_now.year
    CURRENT_SEASON_STYLED = str(CURRENT_SEASON)[-2:]+"."+str(CURRENT_SEASON+1)[-2:]

    return {'CURRENT_SEASON': CURRENT_SEASON,
            'CURRENT_SEASON_STYLED': CURRENT_SEASON_STYLED}
