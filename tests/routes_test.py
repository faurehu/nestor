from nestor.models.audio import Audio
from nestor.models.context import Context
from nestor import create_app
from nestor.db import db

import unittest
import json

VALID_LINK = 'http://google.com'
VALID_TEXT = 'valid text'

class TestRoutes():

    expected_story = {
        'id': 0,
        'title': 'title',
        'type': 'story',
        'author': 'author',
        'description': 'description',
        'link_uri': VALID_LINK,
        'audio_uri': VALID_LINK,
        'contexts': [{
            'type': 'quote',
            'audio_id': 0,
            'time_start': 1,
            'time_end': 10,
            'text' : VALID_TEXT
        }]
    }

    audio_form = {
        'title': 'title',
        'type': 'story',
        'author': 'author',
        'description': 'description',
        'audio_uri': VALID_LINK,
        'link_uri': VALID_LINK,
    }

    def setUp(self):
        app = create_app(testing=True)
        self.app = app.test_client()
        self.story = Audio(0, 'title', 'story', 'author', 'description', VALID_LINK, VALID_LINK)
        self.story.contexts = [Context('quote', 0, 1, 10, text=VALID_TEXT)]
        db.session.add(self.story)
        db.session.commit()

    def tearDown(self):
        db.session.query(Context).delete()
        db.session.query(Audio).delete()
        db.session.commit()

    def test_ping(self):
        r = self.app.get('/ping')
        payload = json.loads(r.get_data(as_text=True))
        assert(payload['ping'])

    def test_get_story(self):
        r = self.app.get('/story/0?json=true')
        json_response = json.loads(r.get_data(as_text=True))
        story = json_response['data']['story']
        assert(story == self.expected_story)

    @unittest.skip
    def test_get_ad(self):
        pass

    def test_get_stories(self):
        r = self.app.get('/stories?json=true')
        json_response = json.loads(r.get_data(as_text=True))
        stories = json_response['data']['stories']
        assert(stories == [self.expected_story])

    @unittest.skip
    def test_post_action(self):
        action = {
            'client_id': 0,
            'audio_id': 0,
            'type': 'start',
            'audio_point': 0,
            'timestamp': date.now(),
        }
        pass

    @unittest.skip
    def test_post_action_with_wrong_client_id(self):
        pass

    @unittest.skip
    def test_post_action_audio_dont_exist(self):
        pass

    def test_post_audio(self):
        audio_form = dict(self.audio_form)
        audio_form['token'] = 'secret_token'

        r = self.app.post('/audio',
                          content_type='application/json',
                          data=json.dumps(audio_form))
        json_response = json.loads(r.get_data(as_text=True))
        assert(json_response['ok'])
        assert(json_response['audio_id'])

    @unittest.skip
    def test_post_action_without_credentials(self):
        pass

    def test_post_audio_without_token(self):
        r = self.app.post('/audio',
                          content_type='application/json',
                          data=json.dumps(self.audio_form))
        json_response = json.loads(r.get_data(as_text=True))
        assert(not json_response['ok'])
