from nestor.db import db
from nestor.errors import InvalidAttribute

from nestor.helpers import is_valid_uri

class Audio(db.Model):

    __tablename__ = 'audio'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    author = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    link_uri = db.Column(db.String(1000), nullable=False)
    audio_uri = db.Column(db.String(1000), nullable=False)

    def __init__(self, id, title, type, author, description, link_uri, audio_uri):
        self.id = id
        self.title = title
        self.type = type
        self.author = author
        self.description = description
        self.link_uri = link_uri
        self.audio_uri = audio_uri

        self.validate()

    def __repr__(self):
        return '< title {} - type {} >'.format(self.title, self.type)

    def validate(self):

        if not is_valid_uri(getattr(self, 'link_uri', '')):
            raise InvalidAttribute('link_uri is not a valid URL')

        if not is_valid_uri(getattr(self, 'audio_uri', '')):
            raise InvalidAttribute('audio_uri is not a valid URL')

        if getattr(self, 'type', '') not in ['story', 'ad']:
            raise InvalidAttribute('type should be one of story or ad')

        for attr in ['title', 'type', 'author', 'description', 'link_uri', 'audio_uri']:
            if len(getattr(self, attr, '')) < 1:
                raise InvalidAttribute('{} is empty'.format(attr))
