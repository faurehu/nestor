from nose.tools import assert_raises

from nestor.models.audio import Audio
from nestor.db import db
from nestor import create_app

from nestor.errors import InvalidAttribute
from sqlalchemy.exc import IntegrityError, DataError

VALID_LINK = 'http://google.com'

class TestAudio():

    def setUp(self):
        self.app = create_app(testing=True)

    def tearDown(self):
        db.session.rollback()
        db.session.query(Audio).delete()
        db.session.commit()

    def test_is_saved(self):
        audio = Audio(1, 'title', 'story', 'author', 'description', VALID_LINK, VALID_LINK)
        db.session.add(audio)
        db.session.commit()

        saved = Audio.query.filter_by(title='title').first()
        assert(saved == audio)

    def test_all_strings_have_info(self):
        with assert_raises(InvalidAttribute):
            audio = Audio(0, '', 'story', 'author', 'description', VALID_LINK, VALID_LINK)

        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', '', 'author', 'description', VALID_LINK, VALID_LINK)

        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', 'story', '', 'description', VALID_LINK, VALID_LINK)

        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', 'story', 'author', '', VALID_LINK, VALID_LINK)

        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', 'story', 'author', 'description', '', VALID_LINK)

        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', 'story', 'author', 'description', 'link', '')

    def test_audio_is_story_or_ad(self):
        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', 'type', 'author', 'description', VALID_LINK, VALID_LINK)

    def test_uri_are_valid(self):
        with assert_raises(InvalidAttribute):
            # Check it has a schema
            audio = Audio(0, 'title', 'story', 'author', 'description', 'google.com', 'audio')

        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', 'story', 'author', 'description', VALID_LINK, 'google.com')

            # Check it has domain
        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', 'story', 'author', 'description', 'http://google', VALID_LINK)

        with assert_raises(InvalidAttribute):
            audio = Audio(0, 'title', 'story', 'author', 'description', 'http://google', VALID_LINK)

    def test_audio_id_is_unique(self):
        audio = Audio(0, 'title', 'story', 'author', 'description', VALID_LINK, VALID_LINK)
        copy = Audio(0, 'diff_title', 'story', 'diff_author', 'description', VALID_LINK, VALID_LINK)

        db.session.add(audio)
        db.session.add(copy)

        with assert_raises(IntegrityError):
            db.session.commit()

    def test_strings_not_too_long(self):
       title = Audio(0, '*' * 141, 'story', 'author', 'description', VALID_LINK, VALID_LINK)
       db.session.add(title)
       with assert_raises(DataError):
           db.session.commit()
       db.session.rollback()

       author = Audio(0, 'title', 'story', '*' * 141, 'description', VALID_LINK, VALID_LINK)
       db.session.add(author)
       with assert_raises(DataError):
           db.session.commit()
       db.session.rollback()

       description = Audio(0, 'title', 'story', 'author', '*' * 141, VALID_LINK, VALID_LINK)
       db.session.add(description)
       with assert_raises(DataError):
           db.session.commit()
       db.session.rollback()

       link_uri = Audio(0, 'title', 'story', 'author', 'description', VALID_LINK + '/' + 'a' * (1001 - len(VALID_LINK)), VALID_LINK)
       db.session.add(link_uri)
       with assert_raises(DataError):
           db.session.commit()
       db.session.rollback()

       audio_uri = Audio(0, 'title', 'story', 'author', 'description', VALID_LINK, VALID_LINK + '/' + 'a' * (1000 - len(VALID_LINK)))
       db.session.add(audio_uri)
       with assert_raises(DataError):
           db.session.commit()
