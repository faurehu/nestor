from nestor.models.story import Story
from nestor.db import db
from nestor import create_app

class TestStory():

    def setUp(self):
        self.app = create_app(testing=True)

    def tearDown(self):
        with self.app.app_context():
            db.session.query(Story).delete()
            db.session.commit()

    def test_is_saved(self):
        story = Story(1, 'title', 'author', 'description', 'text', 'audio')

        with self.app.app_context():
            db.session.add(story)
            db.session.commit()
            saved = Story.query.filter_by(title='title').first()

        assert(saved == story)
