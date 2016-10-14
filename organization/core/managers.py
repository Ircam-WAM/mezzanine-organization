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
from mezzanine.core.managers import search_fields_to_dict, SearchableQuerySet

class CustomSearchableManager(Manager):

    """
    Manager providing a chainable queryset.
    Adapted from http://www.djangosnippets.org/snippets/562/
    search method supports spanning across models that subclass the
    model being used to search.
    """

    def __init__(self, *args, **kwargs):
        self._search_fields = kwargs.pop("search_fields", {})
        super(CustomSearchableManager, self).__init__(*args, **kwargs)

    def get_search_fields(self):
        """
        Returns the search field names mapped to weights as a dict.s
        Used in ``get_queryset`` below to tell ``SearchableQuerySet``
        which search fields to use. Also used by ``DisplayableAdmin``
        to populate Django admin's ``search_fields`` attribute.
        Search fields can be populated via
        ``SearchableManager.__init__``, which then get stored in
        ``SearchableManager._search_fields``, which serves as an
        approach for defining an explicit set of fields to be used.
        Alternatively and more commonly, ``search_fields`` can be
        defined on models themselves. In this case, we look at the
        model and all its base classes, and build up the search
        fields from all of those, so the search fields are implicitly
        built up from the inheritence chain.
        Finally if no search fields have been defined at all, we
        fall back to any fields that are ``CharField`` or ``TextField``
        instances.
        """
        search_fields = self._search_fields.copy()
        if not search_fields:
            for cls in reversed(self.model.__mro__):
                super_fields = getattr(cls, "search_fields", {})
                search_fields.update(search_fields_to_dict(super_fields))
        if not search_fields:
            search_fields = []
            for f in self.model._meta.fields:
                if isinstance(f, (CharField, TextField)):
                    search_fields.append(f.name)
            search_fields = search_fields_to_dict(search_fields)
        return search_fields

    def get_queryset(self):
        search_fields = self.get_search_fields()
        return SearchableQuerySet(self.model, search_fields=search_fields)

    def contribute_to_class(self, model, name):
        """
        Newer versions of Django explicitly prevent managers being
        accessed from abstract classes, which is behaviour the search
        API has always relied on. Here we reinstate it.
        """
        super(CustomSearchableManager, self).contribute_to_class(model, name)
        setattr(model, name, ManagerDescriptor(self))

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
