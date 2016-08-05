from django.contrib import admin
from django import forms
from copy import deepcopy
from mezzanine.core.admin import DisplayableAdmin
from mezzanine.pages.admin import PageAdmin
from orderable.admin import OrderableAdmin, OrderableTabularInline
from organization.magazine.models import Article, Brief ,Topic


class ArticleAdmin(admin.ModelAdmin):
    model = Article

class ArticleAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArticleAdmin.fieldsets)
    exclude = ('related_posts',)

class BriefAdmin(OrderableTabularInline):

    model = Brief

class BriefAdminDisplayable(OrderableAdmin):

    list_display = ('title', 'local_content', 'sort_order_display',)
    fieldsets = deepcopy(BriefAdmin.fieldsets)


admin.site.register(Article, ArticleAdminDisplayable)
admin.site.register(Brief, BriefAdminDisplayable)
admin.site.register(Topic, PageAdmin)
