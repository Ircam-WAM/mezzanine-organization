from django.contrib import admin
from django import forms
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.magazine.models import *
from organization.magazine.forms import *


class ArticleImageInline(TabularDynamicInlineAdmin):

    model = ArticleImage


class ArticleAdmin(admin.ModelAdmin):

    model = Article


class ArticlePersonAutocompleteInlineAdmin(TabularDynamicInlineAdmin):

    model = ArticlePersonListBlockInline
    form = ArticlePersonListForm


class DynamicContentArticleInline(TabularDynamicInlineAdmin):

    model = DynamicContentArticle
    form = DynamicContentArticleForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class ArticleAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArticleAdmin.fieldsets)
    exclude = ('related_posts',)
    filter_horizontal = ['categories',]
    inlines = [ArticleImageInline,
              ArticlePersonAutocompleteInlineAdmin,
              DynamicContentArticleInline]


class BriefAdmin(admin.ModelAdmin): #OrderableTabularInline

    model = Brief


class BriefAdminDisplayable(BaseTranslationModelAdmin,): #, OrderableAdmin

    list_display = ('title', 'external_content', 'content_object', )
    form = BriefForm
    fieldsets = deepcopy(BriefAdmin.fieldsets)
    exclude = ("short_url", "keywords", "description", "slug", )


admin.site.register(Article, ArticleAdminDisplayable)
admin.site.register(Brief, BriefAdminDisplayable)
admin.site.register(Topic, PageAdmin)
