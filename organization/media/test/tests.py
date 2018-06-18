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
from organization.media.models import *
from django.contrib.auth import get_user_model as User
from django.core import urlresolvers
from unittest import skip

class URLTests(TestCase):
    
    def setUp(self):
        super(URLTests, self).setUp()
        self.category = MediaCategory.objects.create(title="video")
        self.media = Media.objects.create(title="video", external_id = "A10", poster_url="www.ircam.fr", category = self.category)   
        self.playlist = Playlist.objects.create(type="audio",title="playlist django", description="playing django")
        self.stream = LiveStreaming.objects.create(title="live",type="html5")


    def test_playlist_slug_detail_url(self):
        response = self.client.get('/playlists/' + self.playlist.slug + "/detail/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"playing django")        
        self.assertTemplateUsed(response,'media/playlist_detail.html')

    def test_playlist_list_url(self):
        response = self.client.get('/playlists/list/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"playlist django")    
        self.assertTemplateUsed(response,'media/playlist_list.html')

    def test_playlist_list_type_url(self):
        response = self.client.get('/playlists/list/video/')
        self.assertEqual(response.status_code,200)
        self.assertNotContains(response,"playlist django")  
        response = self.client.get('/playlists/list/audio/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"playlist django")    
        self.assertTemplateUsed(response,'media/playlist_list.html')

    def test_playlist_overlay(self):
        response = self.client.get('/playlists/overlay/' + self.playlist.slug + "/")
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'media/playlist_overlay.html')

    def test_media_type_slug_detail_url(self):
        response = self.client.get('/medias/video/' + self.media.slug + "/detail/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"www.ircam.fr")    

    @skip('MediaOverlayView : self.object.type = None. Maybe use self.object only')
    def test_media_type_slug_overlay_url(self):
        response = self.client.get('/medias/video/' + self.media.slug + "/overlay/")
        self.assertEqual(response.status_code,200)

    def test_media_autocomplete(self):
        self.client.login(username="test",password="test")
        response = self.client.get('/playlist-media-autocomplete/')
        self.assertEqual(response.status_code,200)        

    def test_stream_slug_type_detail_url(self):
        response = self.client.get('/streams/live/html5/detail/')
        self.assertEqual(response.status_code,200)        
        self.assertTemplateUsed(response,'media/live_streaming/live_streaming_detail.html')

class MediaTests(TestCase):
    
    def setUp(self):
        super(MediaTests, self).setUp()
        self.category = MediaCategory.objects.create()
        self.media = Media.objects.create(external_id = "A10", poster_url="www.ircam.fr", category = self.category)

    def test_media_fk_deletion(self):
        self.category.delete()
        self.assertTrue(self.media in Media.objects.filter(category__isnull=True))

    def test_media_creation(self):
        self.assertTrue(isinstance(self.media, Media))
        self.assertEquals(self.media.external_id, "A10")
        self.assertEquals(self.media.poster_url,"www.ircam.fr")
        self.assertEquals(self.media.category,self.category)

    def test_media_retrieval(self):
        self.assertTrue(self.media in Media.objects.all())
        self.assertTrue(self.media in Media.objects.filter(external_id="A10"))
        self.assertTrue(self.media in Media.objects.filter(poster_url="www.ircam.fr"))
        self.assertTrue(self.media in Media.objects.filter(category=self.category))

    def test_media_update(self):
        self.media.external_id="A11"
        self.assertEqual(1,Media.objects.filter(external_id = "A10").count())
        self.assertEqual(0,Media.objects.filter(external_id="A11").count())
        self.media.save()
        self.assertEqual(0,Media.objects.filter(external_id ="A10").count())
        self.assertEqual(1,Media.objects.filter(external_id="A11").count())     

    def test_media_deletion(self):
        media_transcoded = MediaTranscoded.objects.create(media=self.media)
        media_image = MediaImage.objects.create(media=self.media)
        playlist_media = PlaylistMedia.objects.create(media=self.media)
        self.media.delete()
        self.assertFalse(self.media in Media.objects.all())
        self.assertFalse(media_transcoded in MediaTranscoded.objects.filter(media__isnull=True))
        self.assertTrue(media_image in MediaImage.objects.filter(media__isnull=True))
        self.assertTrue(playlist_media in PlaylistMedia.objects.filter(media__isnull=True))

class PlaylistTests(TestCase):
    
    def setUp(self):
        super(PlaylistTests,self).setUp()
        self.user = User().objects.create_user(username="user", password='test')
        self.playlist = Playlist.objects.create(type="audio")
        app = "organization-media"
        model = "playlist" 
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
    
    def test_playlist_creation(self):
        self.assertTrue(isinstance(self.playlist, Playlist))
        self.assertEqual(self.playlist.type, "audio")        

    def test_playlist_retrieval(self):
        self.assertTrue(self.playlist in Playlist.objects.all())
        self.assertTrue(self.playlist in Playlist.objects.filter(type="audio"))

    def test_playlist_update(self):
        self.playlist.type="video"
        self.assertEqual(1,Playlist.objects.filter(type = "audio").count())
        self.assertEqual(0,Playlist.objects.filter(type = "video").count())
        self.playlist.save()
        self.assertEqual(0,Playlist.objects.filter(type = "audio").count())
        self.assertEqual(1,Playlist.objects.filter(type = "video").count())        

    def test_playlist_deletion(self):
        playlist_media = PlaylistMedia.objects.create(playlist=self.playlist)
        playlist_related = PlaylistRelated.objects.create(playlist=self.playlist)
        self.playlist.delete()
        self.assertTrue(playlist_media in PlaylistMedia.objects.filter(playlist__isnull=True))
        self.assertTrue(playlist_related in PlaylistRelated.objects.filter(playlist__isnull=True))
        self.assertFalse(self.playlist in Playlist.objects.all())

    def test_playlist_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.playlist.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "media/playlist_detail.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.playlist.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "media/playlist_detail.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.playlist.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "media/playlist_detail.html")

    def test_playlist_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.playlist.get_absolute_url())
        self.assertNotContains(response,"editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.playlist.get_absolute_url())
        self.assertNotContains(response,"editable")
        self.client.login(username='editor', password='pass')
        response = self.client.get(self.playlist.get_absolute_url())
        self.assertNotContains(response,"editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.playlist.get_absolute_url())
        self.assertContains(response,"editable")

    def test_playlist_admin(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)   
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)    