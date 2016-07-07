from django.contrib import admin
from copy import deepcopy
from mezzanine.pages.models import Page
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
<<<<<<< HEAD:app/organization/core/admin.py
from organization.core.models import BasicPage
=======
from mezzanine.core.admin import DisplayableAdmin
from custom.models import BasicPage
>>>>>>> article:app/custom/admin.py


# class SubTitleAdmin(DisplayableAdmin):
# 	    """
# 	    Admin class for blog posts.
# 	        return False

#admin.site.register(SubTitle, DisplayableAdmin)


# class SubTitleAdmin(admin.ModelAdmin):
#
#     model = SubTitle



admin.site.register(BasicPage, PageAdmin)
