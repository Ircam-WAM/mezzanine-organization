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


from organization.core.views import SlugMixin
from django.views.generic import DetailView
from cartridge.shop.models import Product


class CustomProductDetailView(SlugMixin, DetailView):

    model = Product
    template_name = 'shop/product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CustomProductDetailView, self).get_context_data(**kwargs)
        if hasattr(self.object, 'product_external_shop') and\
                self.object.product_external_shop.shop and\
                self.object.product_external_shop.shop.item_url:
            context['shop_url'] = self.object.product_external_shop.shop.item_url %\
                self.object.product_external_shop.external_id
        return context
