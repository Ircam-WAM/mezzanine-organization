from django.contrib import admin
from django import forms
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
#from orderable.admin import OrderableTabularInline #OrderableAdmin,
from organization.magazine.models import Article, Brief, Topic, ArticleImage
from organization.magazine.forms import BriefForm


class ArticleImageInline(TabularDynamicInlineAdmin):

    model = ArticleImage


class ArticleAdmin(admin.ModelAdmin):

    model = Article


class ArticleAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArticleAdmin.fieldsets)
    exclude = ('related_posts',)
    filter_horizontal = ['categories', 'related_articles', ]
    inlines = [ArticleImageInline,]


class BriefAdmin(admin.ModelAdmin): #OrderableTabularInline

    model = Brief


class BriefAdminDisplayable(BaseTranslationModelAdmin,): #, OrderableAdmin

    #list_display = ('title', 'local_content', 'sort_order_display',)
    form = BriefForm
    fieldsets = deepcopy(BriefAdmin.fieldsets)

    # form = BriefForm
    # form = autocomplete_light.modelform_factory(Brief)


admin.site.register(Article, ArticleAdminDisplayable)
admin.site.register(Brief, BriefAdminDisplayable)
admin.site.register(Topic, PageAdmin)
