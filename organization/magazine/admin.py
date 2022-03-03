# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from copy import deepcopy
from mezzanine.utils.static import static_lazy as static
from modeltranslation.admin import TranslationTabularInline
from mezzanine.core.admin import TabularDynamicInlineAdmin, TeamOwnableAdmin,\
    DisplayableAdmin, OwnableAdmin, BaseTranslationModelAdmin
from mezzanine.pages.admin import PageAdmin
from organization.magazine.models import ArticleImage, ArticlePlaylist, Article,\
    ArticlePersonListBlockInline, DynamicContentArticle, DynamicMultimediaArticle,\
    ArticleRelatedTitle, Brief, DynamicContentMagazineContent, Magazine, Topic
from organization.magazine.forms import ArticlePersonListForm,\
    DynamicContentArticleForm, DynamicMultimediaArticleForm, BriefForm,\
    DynamicContentMagazineContentForm


class ArticleImageInline(TabularDynamicInlineAdmin):

    model = ArticleImage


class ArticlePlaylistInline(TabularDynamicInlineAdmin):

    model = ArticlePlaylist


class ArticleAdmin(TeamOwnableAdmin):

    model = Article


class ArticlePersonAutocompleteInlineAdmin(TabularDynamicInlineAdmin):

    model = ArticlePersonListBlockInline
    exclude = ("title", "description")
    form = ArticlePersonListForm


class DynamicContentArticleInline(TabularDynamicInlineAdmin):

    model = DynamicContentArticle
    form = DynamicContentArticleForm


class DynamicMultimediaArticleInline(TabularDynamicInlineAdmin):

    model = DynamicMultimediaArticle
    form = DynamicMultimediaArticleForm


class ArticleRelatedTitleAdmin(TranslationTabularInline):

    model = ArticleRelatedTitle


class ArticleAdminDisplayable(TeamOwnableAdmin, DisplayableAdmin):

    fieldsets = deepcopy(ArticleAdmin.fieldsets)
    list_display = ('title', 'department', 'publish_date', 'status', 'user')
    exclude = ('related_posts', 'short_url')

    filter_horizontal = ['categories', ]
    inlines = [
        ArticleImageInline,
        ArticlePersonAutocompleteInlineAdmin,
        DynamicMultimediaArticleInline,
        ArticleRelatedTitleAdmin,
        DynamicContentArticleInline,
        ArticlePlaylistInline
    ]
    list_filter = ['status', 'department', ]  # 'keywords'

    # actions = actions_to_duplicate()

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = super(
            ArticleAdminDisplayable,
            self
        ).get_readonly_fields(request, obj=None)
        if not request.user.is_superuser and 'user' not in self.readonly_fields:
            self.readonly_fields += ('user',)
        return self.readonly_fields

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class BriefAdmin(admin.ModelAdmin):

    model = Brief


class BriefAdminDisplayable(TeamOwnableAdmin, BaseTranslationModelAdmin):

    list_display = ('title', 'ext_content', 'content_object', 'publish_date', 'status')
    form = BriefForm
    fieldsets = deepcopy(BriefAdmin.fieldsets)
    exclude = ("short_url", "keywords", "description", "slug", )
    search_fields = ['title', ]

    def ext_content(self, instance):
        return instance.external_content[:100] + "..."


class DynamicContentHomeSliderInline(TabularDynamicInlineAdmin):

    model = DynamicContentMagazineContent
    form = DynamicContentMagazineContentForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class MagazineAdmin(BaseTranslationModelAdmin):

    model = Magazine
    inlines = [DynamicContentHomeSliderInline, ]


admin.site.register(Article, ArticleAdminDisplayable)
admin.site.register(Brief, BriefAdminDisplayable)
admin.site.register(Topic, PageAdmin)
admin.site.register(Magazine, MagazineAdmin)
