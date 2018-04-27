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
from organization.magazine.models import *
from organization.network.models import Organization
from django.contrib.auth import get_user_model as User


class ArticleTests(TestCase):

    def setUp(self):
        super(ArticleTests, self).setUp()
        organization = Organization.objects.create()
        self.department = Department.objects.create(organization = organization)
        self.user = User().objects.create()
        self.article = Article.objects.create(department = self.department,user = self.user)

    def test_article_many_to_many_fields(self):
        topic = Topic.objects.create()
        self.article.topics.add(topic)
        self.assertEqual(1,self.article.topics.all().count())
        topic = Topic.objects.create()
        self.article.topics.add(topic)
        self.assertEqual(2,self.article.topics.all().count())
        topic = Topic.objects.create()
        self.article.topics.add(topic)
        self.assertEqual(3,self.article.topics.all().count())

    def test_article_fk_deletion(self):
        self.department.delete()
        self.user.delete()
        self.assertFalse(self.article in Article.objects.all())

    def test_article_creation(self):
        self.assertTrue(isinstance(self.article,Article))
        self.assertEquals(self.article.department,self.department)
        self.assertEquals(self.article.user,self.user)

    def test_article_retrieval(self):
        self.assertTrue(self.article in Article.objects.filter(department=self.department))
        self.assertTrue(self.article in Article.objects.filter(user=self.user))
        self.assertTrue(self.article in Article.objects.all())

    def test_article_update(self):
        self.article.department=None
        self.assertEqual(1,Article.objects.filter(department = self.department).count())
        self.assertEqual(0,Article.objects.filter(department__isnull=True).count())
        self.article.save()
        self.assertEqual(0,Article.objects.filter(department = self.department).count())
        self.assertEqual(1,Article.objects.filter(department__isnull=True).count())        

    def test_article_deletion(self):
        article_image = ArticleImage.objects.create(article=self.article)
        article_related_title = ArticleRelatedTitle.objects.create(article=self.article)
        article_playslist = ArticlePlaylist.objects.create(article=self.article)
        article_person_list_block_inline = ArticlePersonListBlockInline.objects.create(article=self.article)
        dynamic_content_article = DynamicContentArticle.objects.create(article=self.article)
        self.article.delete()
        self.assertTrue(article_image in ArticleImage.objects.filter(article__isnull=True))
        self.assertTrue(article_related_title in ArticleRelatedTitle.objects.filter(article__isnull=True))
        self.assertTrue(article_playslist in ArticlePlaylist.objects.filter(article__isnull=True))
        self.assertTrue(article_person_list_block_inline in ArticlePersonListBlockInline.objects.filter(article__isnull=True))
        self.assertFalse(dynamic_content_article in DynamicContentArticle.objects.filter(article__isnull=True))
        self.assertFalse(self.article in Article.objects.all())
