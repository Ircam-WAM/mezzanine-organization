from __future__ import unicode_literals

import django
from future.builtins import int, zip

from functools import reduce
from operator import ior, iand
from string import punctuation

from django.apps import apps, AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Manager, Q, CharField, TextField
from django.db.models.manager import ManagerDescriptor
from django.db.models.query import QuerySet
from django.contrib.sites.managers import CurrentSiteManager as DjangoCSM
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.utils.sites import current_site_id
from mezzanine.utils.urls import home_slug
from mezzanine.core.managers import search_fields_to_dict, SearchableQuerySet, SearchableManager

class CustomSearchableManager(SearchableManager):

    def search(self, *args, **kwargs):
        """
        Proxy to queryset's search method for the manager's model and
        any models that subclass from this manager's model if the
        model is abstract.
        """
        if not settings.SEARCH_MODEL_CHOICES:
            # No choices defined - build a list of leaf models (those
            # without subclasses) that inherit from Displayable.
            models = [m for m in apps.get_models()
                      if issubclass(m, self.model)]
            parents = reduce(ior, [set(m._meta.get_parent_list())
                                   for m in models])
            models = [m for m in models if m not in parents]
        elif getattr(self.model._meta, "abstract", False):
            # When we're combining model subclasses for an abstract
            # model (eg Displayable), we only want to use models that
            # are represented by the ``SEARCH_MODEL_CHOICES`` setting.
            # Now this setting won't contain an exact list of models
            # we should use, since it can define superclass models such
            # as ``Page``, so we check the parent class list of each
            # model when determining whether a model falls within the
            # ``SEARCH_MODEL_CHOICES`` setting.
            search_choices = set()
            models = set()
            parents = set()
            errors = []
            for name in settings.SEARCH_MODEL_CHOICES:
                try:
                    model = apps.get_model(*name.split(".", 1))
                except LookupError:
                    errors.append(name)
                else:
                    search_choices.add(model)
            if errors:
                raise ImproperlyConfigured("Could not load the model(s) "
                        "%s defined in the 'SEARCH_MODEL_CHOICES' setting."
                        % ", ".join(errors))

            for model in apps.get_models():
                # Model is actually a subclasses of what we're
                # searching (eg Displayabale)
                is_subclass = issubclass(model, self.model)
                # Model satisfies the search choices list - either
                # there are no search choices, model is directly in
                # search choices, or its parent is.
                this_parents = set(model._meta.get_parent_list())
                in_choices = not search_choices or model in search_choices
                in_choices = in_choices or this_parents & search_choices
                if is_subclass and (in_choices or not search_choices):
                    # Add to models we'll seach. Also maintain a parent
                    # set, used below for further refinement of models
                    # list to search.
                    models.add(model)
                    parents.update(this_parents)
            # Strip out any models that are superclasses of models,
            # specifically the Page model which will generally be the
            # superclass for all custom content types, since if we
            # query the Page model as well, we will get duplicate
            # results.
            models -= parents
        elif self.model.__name__ == "CustomPage":
            # gather all pages defined in PAGES_MODELS settings
            models = set()
            errors = []
            for name in settings.PAGES_MODELS:
                try:
                    models.add(apps.get_model(name))
                except LookupError:
                    errors.append(name)
            if errors:
                raise ImproperlyConfigured("Could not load the model(s) "
                        "%s defined in the 'SEARCH_MODEL_CHOICES' setting."
                        % ", ".join(errors))
        else:
            models = [self.model]
        all_results = []
        user = kwargs.pop("for_user", None)
        for model in models:
            try:
                queryset = model.objects.published(for_user=user)
            except AttributeError:
                queryset = model.objects.get_queryset()
            all_results.extend(queryset.search(*args, **kwargs))
        return sorted(all_results, key=lambda r: r.result_count, reverse=True)
