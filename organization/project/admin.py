from django.contrib import admin
from mezzanine.blog.admin import BlogPostAdmin
from organization.magazine.models import Article
#from custom.admin import SubTitleAdmin
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

# class ArticleAdmin(BlogPostAdmin, SubTitleAdmin):
#
#     model = Article

#admin.site.register(Article, BlogPostAdmin)
class ArticleAdmin(admin.ModelAdmin):

    model = Article


class ArticleAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArticleAdmin.fieldsets)

admin.site.register(Article, ArticleAdminDisplayable)
