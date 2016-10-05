from nestor.models.audio import Audio
from nestor.db import db
from nestor import create_app

class TestAudio():

    def setUp(self):
        self.app = create_app(testing=True)

    def tearDown(self):
        with self.app.app_context():
            db.session.query(Audio).delete()
            db.session.commit()

    def test_is_saved(self):
        audio = Audio(1, 'title', 'type', 'author', 'description', 'link', 'audio')

        with self.app.app_context():
            db.session.add(audio)
            db.session.commit()
            saved = Audio.query.filter_by(title='title').first()

        assert(saved == audio)
