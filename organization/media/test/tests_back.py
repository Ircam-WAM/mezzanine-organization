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

    def test_article_deletion(self):
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
        self.playlist = Playlist.objects.create(type="audio")
    
    def test_playlist_creation(self):
        self.assertTrue(isinstance(self.playlist, Playlist))
        self.assertEqual(self.playlist.type, "audio")        

    def test_playlist_retrieval(self):
        self.assertTrue(self.playlist in Playlist.objects.all())
        self.assertTrue(self.playlist in Playlist.objects.filter(type="audio"))

    def test_article_update(self):
        self.playlist.type="video"
        self.assertEqual(1,Playlist.objects.filter(type = "audio").count())
        self.assertEqual(0,Playlist.objects.filter(type = "video").count())
        self.playlist.save()
        self.assertEqual(0,Playlist.objects.filter(type = "audio").count())
        self.assertEqual(1,Playlist.objects.filter(type = "video").count())        

    def test_article_deletion(self):
        playlist_media = PlaylistMedia.objects.create(playlist=self.playlist)
        playlist_related = PlaylistRelated.objects.create(playlist=self.playlist)
        self.playlist.delete()
        self.assertTrue(playlist_media in PlaylistMedia.objects.filter(playlist__isnull=True))
        self.assertTrue(playlist_related in PlaylistRelated.objects.filter(playlist__isnull=True))
        self.assertFalse(self.playlist in Playlist.objects.all())
