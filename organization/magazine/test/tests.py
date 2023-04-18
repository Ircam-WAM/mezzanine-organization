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
from organization.magazine.models import Article, Topic, Department,\
    ArticleImage, ArticleRelatedTitle, ArticlePlaylist, ArticlePersonListBlockInline,\
    DynamicContentArticle
from organization.network.models import Organization
from django.contrib.auth import get_user_model as User
from django.core import urlresolvers
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from unittest import skip


class URLTests(TestCase):

    def setUp(self):
        super(URLTests, self).setUp()
        self.article = Article.objects.create(
            title="django article",
            user=self._user, content="django tricks",
            status=CONTENT_STATUS_PUBLISHED
        )
        self.topic = Topic.objects.create(title="title", content="django topic")

    @skip("No translation")
    def test_article_detail_url(self):
        response = self.client.get('/article/detail/' + self.article.slug + "/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "django tricks")

    @skip("No translation")
    def test_basic_article_url(self):
        response = self.client.get('/article/list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "django article")

    @skip("No translation")
    def test_article_type_url(self):
        response = self.client.get('/article/list/article/')
        self.assertEqual(response.status_code, 200)

    def test_dynamic_content_article_url(self):
        response = self.client.get('/dynamic-content-article/')
        self.assertEqual(response.status_code, 200)

    def test_object_autocomplete_url(self):
        response = self.client.get('/object-autocomplete/')
        self.assertEqual(response.status_code, 200)

    @skip("No translation")
    def test_topic_detail_url(self):
        response = self.client.get('/topic/detail/' + self.topic.slug + "/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "django topic")


class ArticleTests(TestCase):

    def setUp(self):
        super(ArticleTests, self).setUp()
        app = "organization_magazine"
        model = "article"
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
        organization = Organization.objects.create()
        User().objects.create_user(username="user", password='test')
        self.department = Department.objects.create(organization=organization)
        self.user = User().objects.create_user(username="editor", password="pass")
        self.article = Article.objects.create(
            department=self.department,
            user=self.user
        )

    def test_article_many_to_many_fields(self):
        topic = Topic.objects.create()
        self.article.topics.add(topic)
        self.assertEqual(1, self.article.topics.all().count())
        topic = Topic.objects.create()
        self.article.topics.add(topic)
        self.assertEqual(2, self.article.topics.all().count())
        topic = Topic.objects.create()
        self.article.topics.add(topic)
        self.assertEqual(3, self.article.topics.all().count())

    def test_article_fk_deletion(self):
        self.department.delete()
        self.user.delete()
        self.assertFalse(self.article in Article.objects.all())

    def test_article_creation(self):
        self.assertTrue(isinstance(self.article, Article))
        self.assertEquals(self.article.department, self.department)
        self.assertEquals(self.article.user, self.user)

    def test_article_retrieval(self):
        self.assertTrue(
            self.article in Article.objects.filter(department=self.department)
        )
        self.assertTrue(self.article in Article.objects.filter(user=self.user))
        self.assertTrue(self.article in Article.objects.all())

    def test_article_update(self):
        self.article.department = None
        self.assertEqual(
            1,
            Article.objects.filter(department=self.department).count()
        )
        self.assertEqual(
            0,
            Article.objects.filter(department__isnull=True).count()
        )
        self.article.save()
        self.assertEqual(
            0,
            Article.objects.filter(department=self.department).count()
        )
        self.assertEqual(1, Article.objects.filter(department__isnull=True).count())

    def test_article_deletion(self):
        article_image = ArticleImage.objects.create(article=self.article)
        article_related_title = ArticleRelatedTitle.objects.create(article=self.article)
        article_playslist = ArticlePlaylist.objects.create(article=self.article)
        article_person_list_block_inline = ArticlePersonListBlockInline.objects.create(
            article=self.article
        )
        dynamic_content_article = DynamicContentArticle.objects.create(
            article=self.article
        )
        self.article.delete()
        self.assertTrue(
            article_image in ArticleImage.objects.filter(
                article__isnull=True
            )
        )
        self.assertTrue(
            article_related_title in ArticleRelatedTitle.objects.filter(
                article__isnull=True
            )
        )
        self.assertTrue(
            article_playslist in ArticlePlaylist.objects.filter(
                article__isnull=True
            )
        )
        self.assertTrue(
            article_person_list_block_inline in ArticlePersonListBlockInline.objects
            .filter(article__isnull=True)
        )
        self.assertFalse(
            dynamic_content_article in DynamicContentArticle.objects
            .filter(article__isnull=True)
        )
        self.assertFalse(self.article in Article.objects.all())

    def test_article_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "magazine/article/article_detail.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "magazine/article/article_detail.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "magazine/article/article_detail.html")

    def test_article_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.article.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.article.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='editor', password='pass')
        response = self.client.get(self.article.get_absolute_url())
        self.assertContains(response, "editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.article.get_absolute_url())
        self.assertContains(response, "editable")

    def test_article_admin_creation(self):
        nmb = Article.objects.count()
        self.client.login(username='test', password='test')
        response = self.client.post(
            self.url,
            {
                "title": 'titre',
                "status": 2,
                "user": self.user.id,
                'article_person_list_block_inlines-INITIAL_FORMS': '0',
                'article_person_list_block_inlines-TOTAL_FORMS': '1',
                'dynamic_content_articles-INITIAL_FORMS': '0',
                'dynamic_content_articles-TOTAL_FORMS': '1',
                'images-INITIAL_FORMS': '0',
                'images-TOTAL_FORMS': '1',
                'playlists-INITIAL_FORMS': '0',
                'playlists-TOTAL_FORMS': '1',
                'related_title-INITIAL_FORMS': '0',
                'related_title-TOTAL_FORMS': '1',
                'allow_comments': 'on',
                'gen_description': 'on',
                'in_sitemap': 'on',
                'content': 'yes',
                'csrfmiddlewaretoken': 'ahGmaJGV8YSLUM8Vuvlzt9DOE8Bz9IxD'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(nmb + 1, Article.objects.count())
