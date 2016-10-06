from nose.tools import assert_raises

from nestor.models.audio import Audio
from nestor.models.action import Action
from nestor.db import db
from nestor import create_app

from datetime import datetime

from nestor.errors import InvalidAttribute
from sqlalchemy.exc import IntegrityError

VALID_LINK = 'http://google.com'

class TestAction():

    def setUp(self):
        self.app = create_app(testing=True)

        audio = Audio(0, 'title', 'story', 'author', 'description', VALID_LINK, VALID_LINK)
        db.session.add(audio)
        db.session.commit()

    def tearDown(self):
        db.session.query(Action).delete()
        db.session.query(Audio).delete()
        db.session.commit()

    def test_is_saved(self):
        action = Action(0, 0, 0, 'start', 0, datetime.utcnow())
        db.session.add(action)
        db.session.commit()

        saved = Action.query.filter_by(id=action.id).first()
        assert(saved == action)

    def test_all_strings_have_info(self):
        with assert_raises(InvalidAttribute):
            action = Action(0, 0, 0, '', 0, datetime.utcnow())

    def test_type_exists(self):
        with assert_raises(InvalidAttribute):
            Action(0, 0, 0, 'other', 0, datetime.utcnow())

        Action(0, 0, 0, 'start', 0, datetime.utcnow())
        Action(0, 0, 0, 'finished', 0, datetime.utcnow())
        Action(0, 0, 0, 'queued', 0, datetime.utcnow())
        Action(0, 0, 0, 'shared', 0, datetime.utcnow())
        Action(0, 0, 0, 'context', 0, datetime.utcnow())
        Action(0, 0, 0, 'link', 0, datetime.utcnow())

    def test_id_is_unique(self):
        action = Action(0, 0, 0, 'link', 0, datetime.utcnow())
        copy = Action(0, 0, 0, 'link', 0, datetime.utcnow())

        db.session.add(action)
        db.session.add(copy)

        with assert_raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

    def test_audio_is_deleted(self):
        action = Action(0, 0, 0, 'link', 0, datetime.utcnow())
        db.session.add(action)
        db.session.commit()

        audio = Audio.query.filter_by(title='title').first()
        db.session.delete(audio)

        with assert_raises(IntegrityError):
            db.session.commit()

        db.session.rollback()
