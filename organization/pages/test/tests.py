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
from organization.pages.models import Page, PageBlock, PageImage, PagePlaylist,\
    PageRelatedTitle, DynamicContentPage, Home, HomeImage, DynamicContentHomeMedia,\
    DynamicContentHomeBody, DynamicContentHomeSlider


class URLTests(TestCase):
    def setUp(self):
        super(URLTests, self).setUp()
        self.page = Page.objects.create()

    def test_no_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_url(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_newsletter_url(self):
        response = self.client.get('/newsletter/')
        self.assertEqual(response.status_code, 200)


class PageTests(TestCase):

    def setUp(self):
        super(PageTests, self).setUp()
        self.page = Page.objects.create()

    def test_page_deletion(self):
        page_block = PageBlock.objects.create(page=self.page)
        page_image = PageImage.objects.create(page=self.page)
        page_playlist = PagePlaylist.objects.create(page=self.page)
        page_related_title = PageRelatedTitle.objects.create(page=self.page)
        dynamic_content_page = DynamicContentPage.objects.create(page=self.page)
        self.page.delete()
        self.assertFalse(self.page in Page.objects.all())
        self.assertTrue(page_block in PageBlock.objects.filter(page__isnull=True))
        self.assertTrue(page_image in PageImage.objects.filter(page__isnull=True))
        self.assertTrue(page_playlist in PagePlaylist.objects.filter(page__isnull=True))
        self.assertFalse(
            dynamic_content_page in DynamicContentPage.objects.filter(page__isnull=True)
        )
        self.assertTrue(
            page_related_title in PageRelatedTitle.objects.filter(page__isnull=True)
        )


class HomeTests(TestCase):

    def setUp(self):
        super(HomeTests, self).setUp()
        self.home = Home.objects.create()

    def test_home_deletion(self):
        home_image = HomeImage.objects.create(home=self.home)
        dynamic_content_home_media = DynamicContentHomeMedia.objects.create(
            home=self.home
        )
        dynamic_content_home_body = DynamicContentHomeBody.objects.create(
            home=self.home
        )
        dynamic_content_home_slider = DynamicContentHomeSlider.objects.create(
            home=self.home
        )
        self.home.delete()
        self.assertTrue(home_image in HomeImage.objects.filter(home__isnull=True))
        self.assertFalse(
            dynamic_content_home_slider in DynamicContentHomeSlider.objects.filter(
                home__isnull=True
            )
        )
        self.assertFalse(
            dynamic_content_home_body in DynamicContentHomeBody.objects.filter(
                home__isnull=True
            )
        )
        self.assertFalse(
            dynamic_content_home_media in DynamicContentHomeMedia.objects.filter(
                home__isnull=True
            )
        )
        self.assertFalse(self.home in Home.objects.all())
