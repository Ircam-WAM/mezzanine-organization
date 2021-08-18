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


from django.apps import apps
from functools import reduce
from operator import ior
from django.core.exceptions import ImproperlyConfigured

from mezzanine.conf import settings
from mezzanine.pages.managers import PageManager


class CustomSearchableManager(PageManager):

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
                raise ImproperlyConfigured(
                    "Could not load the model(s) "
                    "%s defined in the 'SEARCH_MODEL_CHOICES' setting."
                    % ", ".join(errors)
                )

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
                raise ImproperlyConfigured(
                    "Could not load the model(s) "
                    "%s defined in the 'SEARCH_MODEL_CHOICES' setting."
                    % ", ".join(errors)
                )
        else:
            models = [self.model]
        all_results = []
        user = kwargs.pop("for_user", None)
        for model in models:
            try:
                queryset = model.objects.published(for_user=user)
            except AttributeError:
                queryset = model.objects.get_queryset()
            all_results.extend(queryset.search(*args, **kwargs).annotate_scores())
        return sorted(all_results, key=lambda r: r.result_count, reverse=True)
