from unittest import TestCase
import os
import json
import unittest

from api.app import create_app, db


class SongTestCase(TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.songlist = {'name_of_song': 'Dance to the music', 'duration': 6}

        with self.app.app_context():
            db.create_all()

    def test_songlist_creation(self):
        """Test API can create a songlist (POST request)."""
        response = self.client().post('/song/1', data=self.songlist)
        self.assertEqual(response.status_code, 201)
        self.assertIn('to the music', str(response.data))

    def test_songlist_creation_already_exist_with_id(self):
        """Test API can not create songlist with the same id"""
        response = self.client().post('/song/1', data=self.songlist)
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/song/1', data=self.songlist)
        self.assertEqual(response.status_code, 409)

    def test_songlist_creation_with_negative_duration(self):
        """Test API for negative duration (POST request)"""
        response = self.client().post(
            '/song/1', data={'name_of_song': 'Party Up', 'duration': -5})
        self.assertEqual(response.status_code, 400)

    def test_api_can_get_all_songlist(self):
        """Test API can get all the songlist (GET request)."""
        response = self.client().post('/song/1', data=self.songlist)
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/song')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dance to', str(response.data))

    def test_api_can_get_songlist_by_id(self):
        """Test API can get a single songlist by using it's id."""
        res = self.client().post('/song/1', data=self.songlist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(
            res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/song/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Dance to the music', str(result.data))

    def test_songlist_can_be_edited(self):
        """Test API can edit an existing songlist (PATCH request)"""
        res = self.client().post(
            '/song/1', data={'name_of_song': 'Feel me', 'duration': 4})
        self.assertEqual(res.status_code, 201)
        res = self.client().patch(
            '/song/1', data={'name_of_song': 'Feel me to the music on top', 'duration': 2})
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/song/1')
        self.assertIn('to the music on top', str(result.data))

    def test_songlist_can_not_be_edited_with_negative_duration(self):
        """Test API can not be edited with a negative duration  on an existing songlist (PATCH request)"""
        res = self.client().post(
            '/song/1', data={'name_of_song': 'Feel me', 'duration': 4})
        self.assertEqual(res.status_code, 201)
        res = self.client().patch(
            '/song/1', data={'name_of_song': 'Feel me', 'duration': -3})
        self.assertEqual(res.status_code, 400)

    def test_songlist_deletion(self):
        """Test API can delete an existing songlist (DELETE request)"""
        res = self.client().post(
            '/song/1', data={'name_of_song': 'Take me off', 'duration': 3})
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/song/1')
        self.assertEqual(res.status_code, 200)
        """Test if it exist, responds should be 404"""
        result = self.client().get('/song/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """Tear down all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class AudiobookTestCase(TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.audiobooklist = {'title_of_audiobook': 'Passion feel',
                              'author_of_title': 'James Peter', 'narrator': 'Hart', 'duration': 5}

        with self.app.app_context():
            db.create_all()

    def test_audiobooklist_creation(self):
        """Test API can create a audiobooklist (POST request)."""
        response = self.client().post('/audiobook/1', data=self.audiobooklist)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Passion feel', str(response.data))

    def test_audiobooklist_creation_already_exist_with_id(self):
        """Test API can not create audiobooklist with the same id"""
        response = self.client().post('/audiobook/1', data=self.audiobooklist)
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/audiobook/1', data=self.audiobooklist)
        self.assertEqual(response.status_code, 409)

    def test_audiobooklist_creation_with_negative_duration(self):
        """Test API for negative duration (POST request)"""
        response = self.client().post(
            '/audiobook/1', data={'title_of_audiobook': 'Cammon It', 'author_of_title': 'Kane J.', 'narrator': 'Jennie', 'duration': -5})
        self.assertEqual(response.status_code, 400)

    def test_api_can_get_all_audiobook(self):
        """Test API can get all the audiobooklist (GET request)."""
        response = self.client().post('/audiobook/1', data=self.audiobooklist)
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/audiobook')
        self.assertEqual(response.status_code, 200)
        self.assertIn('James Peter', str(response.data))

    def test_api_can_get_audiobooklist_by_id(self):
        """Test API can get a single audiobooklist by using it's id."""
        res = self.client().post('/audiobook/1', data=self.audiobooklist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(
            res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/audiobook/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Hart', str(result.data))

    def test_audiobooklist_can_be_edited(self):
        """Test API can edit an existing audiobooklist (PATCH request)"""
        res = self.client().post(
            '/audiobook/1', data={'title_of_audiobook': 'Take care', 'author_of_title': 'Drake', 'narrator': 'Jennie', 'duration': 5})
        self.assertEqual(res.status_code, 201)
        res = self.client().patch(
            '/audiobook/1', data={'title_of_audiobook': 'Take care guys!', 'author_of_title': 'Drake', 'narrator': 'Simeon', 'duration': 7})
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/audiobook/1')
        self.assertIn('care guys', str(result.data))

    def test_audiobooklist_can_not_be_edited_with_negative_duration(self):
        """Test API can not be edited with a negative duration  on an existing audiobooklist (PATCH request)"""
        res = self.client().post(
            '/audiobook/1', data={'title_of_audiobook': 'Take care', 'author_of_title': 'Drake', 'narrator': 'Jennie', 'duration': 5})
        self.assertEqual(res.status_code, 201)
        res = self.client().patch(
            '/audiobook/1', data={'title_of_audiobook': 'Take care', 'author_of_title': 'Drake', 'narrator': 'Jennie', 'duration': -7})
        self.assertEqual(res.status_code, 400)

    def test_audiobooklist_deletion(self):
        """Test API can delete an existing audiobooklist (DELETE request)"""
        res = self.client().post(
            '/audiobook/1', data={'title_of_audiobook': 'Take care', 'author_of_title': 'Drake', 'narrator': 'Jennie', 'duration': 7})
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/audiobook/1')
        self.assertEqual(res.status_code, 200)
        """Test if it exist, responds should be 404"""
        result = self.client().get('/audiobook/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """Tear down all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
