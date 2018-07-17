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

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic.base import View, RedirectView
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.apps import apps
from django.utils import six, timezone, formats
from django.utils.translation import ugettext_lazy as _
from django.http import QueryDict
from django.template.defaultfilters import capfirst
from django.core.urlresolvers import reverse
from mezzanine.conf import settings
from mezzanine.utils.views import paginate
from organization.core.models import *
from functools import reduce
from operator import ior, iand
from organization.media.models import Playlist
from mezzanine_agenda.models import Event
from organization.pages.models import CustomPage
from organization.projects.models import Project
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from organization.network.models import Person
from organization.magazine.models import Article
from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from organization.network.models import *
from django import http
from django.template import Context, Engine, TemplateDoesNotExist, loader
from django.utils import six
from django.utils.encoding import force_text
from django.views.decorators.csrf import requires_csrf_token
 

class SlugMixin(object):

    def get_object(self):
        objects = self.model.objects.all()
        return get_object_or_404(objects, slug=self.kwargs['slug'])


class PublishedMixin(object):
    
    def get_queryset(self, **kwargs):
        return self.model.objects.published()


class CustomSearchView(TemplateView):

    template_name='search_results.html'

    def get(self, request, *args, **kwargs):
        """
        Display search results. Takes an optional "contenttype" GET parameter
        in the form "app-name.ModelName" to limit search results to a single model.
        """
        context = super(CustomSearchView, self).get_context_data(**kwargs)
        query = request.GET.get("q", "")
        page = request.GET.get("page", 1)
        per_page = settings.SEARCH_PER_PAGE
        max_paging_links = settings.MAX_PAGING_LINKS
        is_searching_all = False
        try:
            parts = request.GET.get("type", "").split(".", 1)
            search_model = apps.get_model(*parts)
            search_model.objects.search  # Attribute check
        except (ValueError, TypeError, LookupError, AttributeError):
            search_model = Displayable
            search_type = _("Everything")
            is_searching_all = True
        else:
            search_type = search_model._meta.verbose_name_plural.capitalize()

        # @Todo : rewrite SearchableManager
        results = search_model.objects.search(query, for_user=request.user)
        results_media_count = len(Playlist.objects.search(query, for_user=request.user))
        results_page_count = len(CustomPage.objects.search(query, for_user=request.user))
        results_event_count = len(Event.objects.search(query, for_user=request.user))
        results_project_count = len(Project.objects.search(query, for_user=request.user))
        results_article_count = len(Article.objects.search(query, for_user=request.user))

        # count objects
        filter_dict = dict()

        for result in results:
            classname = result.__class__.__name__
            app_label = result._meta.app_label
            full_classname = app_label+"."+classname
            verbose_name = result._meta.verbose_name
            # aggregate all Page types : CustomPage, TeamPage, Topic etc...
            if result._meta.get_parent_list() :
                parent_class = result._meta.get_parent_list()[0]
                if full_classname in settings.PAGES_MODELS:
                    classname = "CustomPage"
                    verbose_name = "Page"
                    app_label = "organization-pages"
            elif classname == "Playlist":
                verbose_name = "Media"
            if classname in filter_dict:
                filter_dict[classname]['count'] += 1
            else:
                filter_dict[classname] = {'count' : 1}
                filter_dict[classname].update({'verbose_name' : verbose_name})
                filter_dict[classname].update({'app_label' : app_label})

        # temporarily overriding filter_dict to get all filters manually
        filter_dict = {
            'CustomPage': {
                'count' : results_page_count,
                'verbose_name' : _('Page'),
                'app_label' : 'organization-pages'
            },
            'Article': {
                'count' : results_article_count,
                'verbose_name' : _('Article'),
                'app_label' : 'organization-magazine'
            },
            'Playlist': {
                'count' : results_media_count,
                'verbose_name' : _('Media'),
                'app_label' : 'organization-media'
            },
            'Project': {
                'count' : results_project_count,
                'verbose_name' : _('Project'),
                'app_label' : 'organization-projects'
            },
            'Event': {
                'count' : results_event_count,
                'verbose_name' : _('Event'),
                'app_label' : 'mezzanine_agenda'
            },
        }

        # get url param
        current_query = QueryDict(mutable=True)
        current_query = request.GET.copy()

        # generate filter url
        for key, value in filter_dict.items():
            current_query['type'] = value['app_label']+'.'+ key
            filter_dict[key].update({'url' : request.path+"?"+current_query.urlencode(safe='/')})

        # pagination
        paginated = paginate(results, page, per_page, max_paging_links)

        # count all results
        all_results_count = results_media_count \
            + results_page_count \
            + results_event_count \
            + results_article_count \
            + results_project_count

        # context
        context = {"query": query, "results": paginated,
                   "search_type": search_type.__class__.__name__, "search_model": search_model.__name__,
                   "all_results_count" : all_results_count, 'is_searching_all': is_searching_all}

        # cancel filter url
        if request.GET.__contains__('type'):
            previous_query = QueryDict(mutable=True)
            previous_query = request.GET.copy()
            previous_query.pop('type')
            context['cancel_filter_url'] = '?'+previous_query.urlencode(safe='/')

        context['filter_dict'] = filter_dict
        # context.update(extra_context or {})
        return self.render_to_response(context)


def autocomplete_result_formatting(self, context):
    """
    Return a list of results usable by Select2.
    It will render as a list of one <optgroup> per different content type
    containing a list of one <option> per model.
    """
    groups = {}

    for result in context['object_list']:
        groups.setdefault(type(result), [])
        groups[type(result)].append(result)

    all_results = []
    for model, results in groups.items():
        children = []
        for result in results:
            text = six.text_type(result)
            if model.__name__ == "Event":
                event_date = timezone.localtime(result.start)
                is_parent = ""
                if not result.parent:
                    is_parent =  " ♦ -"
                text = "%s -%s%s" % (six.text_type(result), is_parent, formats.date_format(event_date, "d-m-y H:i"))

            children.append({
                'id': self.get_result_value(result),
                'text': text,
            })

        curr_model_result = {
             'id': None,
             'text': capfirst(model._meta.verbose_name),
             'children': children
        }
        all_results.append(curr_model_result)

    return all_results


class AccountProfilView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        redirect_url = reverse('home')
        try :
            person = Person.objects.get(email=self.request.user._wrapped.email)
            if person:
                person.user = self.request.user
                person.save()
                if person.register_id :
                    redirect_url = reverse("organization-network-person-detail", kwargs={"slug": person.slug})
        except :
            pass
        return redirect_url


class UserProjectsView(LoginRequiredMixin, ListView):

    model = Project
    template_name='accounts/account_projects_list.html'

    def get_queryset(self):
        user = self.request.user
        qs = Project.objects.filter(user=user).select_related().order_by('title')
        return qs


class UserProducerView(LoginRequiredMixin, ListView):

    model = Organization
    template_name='accounts/account_producer_list.html'

    def get_queryset(self):
        user = self.request.user
        qs = Organization.objects.filter(user=user).select_related().order_by('name')
        return qs


# This can be called when CsrfViewMiddleware.process_view has not run,
# therefore need @requires_csrf_token in case the template needs
# {% csrf_token %}.
@requires_csrf_token
def permission_denied(request, exception, template_name='errors/403.html'):
    """
    Permission denied (403) handler.
    Templates: :template:`403.html`
    Context: None
    If the template does not exist, an Http403 response containing the text
    "403 Forbidden" (as per RFC 2616) will be returned.
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return http.HttpResponseForbidden(
        template.render(request=request, context={'exception': force_text(exception)})
    )