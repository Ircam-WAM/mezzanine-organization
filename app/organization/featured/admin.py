from django.contrib import admin

from organization.featured.models import *


class FeaturedAdmin(admin.ModelAdmin):

    model = Featured
    list_display = ('__unicode__',)
    filter_horizontal = ['events', 'videos', 'articles', 'pages', 'playlists', 'briefs']


admin.site.register(Featured, FeaturedAdmin)
