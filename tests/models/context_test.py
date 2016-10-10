from nose.tools import assert_raises

from nestor.models.context import Context
from nestor.models.audio import Audio
from nestor.db import db
from nestor import create_app

from sqlalchemy.exc import IntegrityError
from nestor.errors import InvalidAttribute, MissingAttribute

VALID_LINK = 'http://google.com'
VALID_TEXT = 'valid text'

class TestContext():

    def setUp(self):
        self.app = create_app(testing=True)

        audio = Audio(0, 'title', 'story', 'author', 'description', VALID_LINK, VALID_LINK)
        db.session.add(audio)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        db.session.query(Audio).delete()
        db.session.query(Context).delete()
        db.session.commit()

    def test_is_saved(self):
        context = Context('quote', 0, 1, 10, text=VALID_TEXT)
        db.session.add(context)
        db.session.commit()

        saved = Context.query.filter_by(type='quote', audio_id=0, time_start=1).first()
        assert(saved == context)

    def test_keys_are_unique(self):
        new_audio = Audio(1, 'title', 'story', 'author', 'description', VALID_LINK, VALID_LINK)
        db.session.add(new_audio)
        db.session.commit()

        original = Context('quote', 0, 1, 10, text=VALID_TEXT)
        copy = Context('quote', 0, 1, 10, text=VALID_TEXT)

        db.session.add(original)
        db.session.add(copy)

        with assert_raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        diff_time_start = Context('quote', 0, 2, 10, text=VALID_TEXT)
        diff_type = Context('image', 0, 1, 10, img_uri=VALID_LINK)
        diff_audio_id = Context('quote', 1, 1, 10, text=VALID_TEXT)

        db.session.add(original)
        db.session.add(diff_time_start)
        db.session.add(diff_type)
        db.session.add(diff_audio_id)
        db.session.commit()

    def test_time_start_less_than_zero(self):
        context = Context('quote', 0, -1, 10, text=VALID_TEXT)
        db.session.add(context)

        with assert_raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

        context = Context('quote', 0, 0, 10, text=VALID_TEXT)
        db.session.add(context)
        db.session.commit()

    def test_type_exists(self):
        with assert_raises(InvalidAttribute):
            Context('other', 0, 0, 10)

    def test_image_has_uri(self):
        with assert_raises(MissingAttribute):
            Context('image', 0, 0, 10)

    def test_quote_has_text(self):
        with assert_raises(MissingAttribute):
            Context('quote', 0, 0, 10)

    def test_button_has_uri_and_text(self):
        with assert_raises(MissingAttribute):
            Context('button', 0, 0, 10)

    def test_strings_not_too_long(self):
        INVALID_LINK = VALID_LINK + '/' + 'a' * (1001 - len(VALID_LINK))
        INVALID_TEXT = '*' * 141

        with assert_raises(InvalidAttribute):
            Context('image', 0, 0, 10, img_uri=INVALID_LINK)

        with assert_raises(InvalidAttribute):
            Context('quote', 0, 0, 10, text=INVALID_TEXT)

        with assert_raises(InvalidAttribute):
            Context('button', 0, 0, 10, text=INVALID_TEXT, link_uri=VALID_LINK)

        with assert_raises(InvalidAttribute):
            Context('button', 0, 0, 10, text='text', link_uri=INVALID_LINK)

    def test_uri_are_valid(self):
        # 'google.com' 'http://google'
        with assert_raises(InvalidAttribute):
            Context('image', 0, 0, 10, img_uri='google.com')

        with assert_raises(InvalidAttribute):
            Context('image', 0, 0, 10, img_uri='http://google')

        with assert_raises(InvalidAttribute):
            Context('button', 0, 0, 10, text=VALID_TEXT, link_uri='http://google')

        with assert_raises(InvalidAttribute):
            Context('button', 0, 0, 10, text=VALID_TEXT, link_uri='google.com')

    def test_context_is_deleted(self):
        context = Context('quote', 0, 1, 10, text=VALID_TEXT)
        db.session.add(context)
        db.session.commit()

        audio = Audio.query.filter_by(title='title').first()
        db.session.delete(audio)
        db.session.commit()

        deleted = Context.query.filter_by(type='quote', audio_id=0, time_start=1).first()
        assert(deleted is None)

    def test_get_context_from_audio(self):
        context = Context('quote', 0, 1, 10, text=VALID_TEXT)
        db.session.add(context)
        db.session.commit()

        audio = Audio.query.filter_by(title='title').first()
        assert(context in audio.contexts)

    def test_no_same_type_and_audio_share_time(self):
        context = Context('quote', 0, 10, 20, text=VALID_TEXT)
        db.session.add(context)
        db.session.commit()

        with assert_raises(InvalidAttribute):
            overlap = Context('quote', 0, 9, 11, text=VALID_TEXT)

        with assert_raises(InvalidAttribute):
            overlap = Context('quote', 0, 19, 21, text=VALID_TEXT)

    def test_is_serialized(self):
        context = Context('quote', 0, 9, 11, text=VALID_TEXT)

        expected_object = {
            'type': 'quote',
            'time_start': 9,
            'audio_id': 0,
            'time_end': 11,
            'text': VALID_TEXT
        }

        assert(context.serialize() == expected_object)
