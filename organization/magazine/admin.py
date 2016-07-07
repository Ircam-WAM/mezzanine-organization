from django.contrib import admin
from django import forms
from copy import deepcopy
from mezzanine.core.admin import DisplayableAdmin
from organization.magazine.models import Brief
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import AutoCompleteSelectField
from organization.magazine.models import Brief


class BriefAdmin(AjaxSelectAdmin):

    model = Brief

class BriefAdminDisplayable(DisplayableAdmin):

    #make_ajax_form(Label, {'ville': 'ville'})
    #id_local_content = AutoCompleteSelectField('local_content', label="local_content")
    form = make_ajax_form(Brief, {'local_content': 'article'})
    fieldsets = deepcopy(BriefAdmin.fieldsets)

admin.site.register(Brief, BriefAdminDisplayable)
