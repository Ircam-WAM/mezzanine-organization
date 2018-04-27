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

from mezzanine.utils.tests import TestCase
from organization.shop.models import *
from cartridge.shop.models import Product

class ProductTests(TestCase):
    
    def setUp(self):
        super(ProductTests, self).setUp()
        self.product = Product.objects.create()

    def test_product_deletion(self):
        product_list_product = ProductListProduct.objects.create(product = self.product)
        link_type = LinkType.objects.create(name = "test link")
        product_link = ProductLink.objects.create(product = self.product, link_type = link_type)
        product_prestashop_product = ProductPrestashopProduct.objects.create(product = self.product)
        self.product.delete()
        self.assertTrue(product_list_product in ProductListProduct.objects.filter(product__isnull=True))
        self.assertTrue(product_link in ProductLink.objects.filter(product__isnull=True))
        self.assertFalse(product_prestashop_product in ProductPrestashopProduct.objects.all())
        self.assertFalse(self.product in Product.objects.all())

class ProductListTests(TestCase):
    
    def setUp(self):
        super(ProductListTests, self).setUp()
        self.list = ProductList.objects.create(style="square")    

    def test_product_list_creation(self):
        self.assertTrue(isinstance(self.list,ProductList))
        self.assertEquals(self.list.style,"square")

    def test_product_list_retrieval(self):
        self.assertTrue(self.list in ProductList.objects.filter(style="square"))
        self.assertTrue(self.list in ProductList.objects.all())

    def test_product_list_update(self):
        self.list.style="circle"
        self.assertEqual(1,ProductList.objects.filter(style="square").count())
        self.assertEqual(0,ProductList.objects.filter(style="circle").count())
        self.list.save()
        self.assertEqual(0,ProductList.objects.filter(style="square").count())
        self.assertEqual(1,ProductList.objects.filter(style="circle").count())        

    def test_product_list_deletion(self):
        product_list_product = ProductListProduct.objects.create(list = self.list)
        page_product_list = PageProductList.objects.create(list = self.list)
        self.list.delete()
        self.assertTrue(product_list_product in ProductListProduct.objects.filter(list__isnull=True))
        self.assertTrue(page_product_list in PageProductList.objects.filter(list__isnull=True))
        self.assertFalse(self.list in ProductList.objects.all())