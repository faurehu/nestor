from nestor.errors import InvalidAttribute, MissingAttribute
from nestor.helpers import is_valid_uri
from nestor.db import db

class Context(db.Model):

    __tablename__ = 'context'

    type = db.Column('type', db.String(10), primary_key=True)
    audio_id = db.Column('audio_id', db.Integer, db.ForeignKey('audio.id', ondelete='CASCADE'), primary_key=True)
    time_start = db.Column('time_start', db.Integer, db.CheckConstraint('time_start > 0'), primary_key=True)
    time_end = db.Column('time_end', db.Integer, nullable=False)
    link_uri = db.Column('link_uri', db.String(1000))
    img_uri = db.Column('img_uri', db.String(1000))
    text = db.Column('text', db.String(140))
    audio = db.relationship('Audio', backref=db.backref('contexts', cascade='save-update, merge, '
                                                                            'delete, delete-orphan'))

    def __init__(self, type, audio_id, time_start, time_end, link_uri=None, img_uri=None, text=None):
        self.type = type
        self.audio_id = audio_id
        self.time_start = time_start
        self.time_end = time_end

        if link_uri is not None:
            self.link_uri = link_uri

        if img_uri is not None:
            self.img_uri = img_uri

        if text is not None:
            self.text = text

        self.validate()

    def validate(self):

        if self.type not in ['quote', 'button', 'image']:
            raise InvalidAttribute('type is not valid')

        if self.type == 'image':
            if not self.img_uri:
                raise MissingAttribute('img_uri is missing')
            if len(self.img_uri) > 1000:
                raise InvalidAttribute('img_uri is too long')
            if not is_valid_uri(self.img_uri):
                raise InvalidAttribute('img_uri is not a valid uri')

        if self.type == 'quote':
            if not self.text:
                raise MissingAttribute('text is missing')
            if len(self.text) > 140:
                raise InvalidAttribute('text is too long')

        if self.type == 'button':
            if not self.link_uri:
                raise MissingAttribute('link_uri is missing')
            if len(self.link_uri) > 1000:
                raise InvalidAttribute('link_uri is too long')
            if not is_valid_uri(self.link_uri):
                raise InvalidAttribute('link_uri is not a valid uri')
            if not self.text:
                raise MissingAttribute('text is missing')
            if len(self.text) > 140:
                raise InvalidAttribute('text is too long')
