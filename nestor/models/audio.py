from nestor.db import db
from nestor.errors import InvalidAttribute

from sqlalchemy import func

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
        # TODO: fix clashing ids
        if id is None:
            id = Audio.get_new_id()

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

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'author': self.author,
            'description': self.description,
            'link_uri': self.link_uri,
            'audio_uri': self.audio_uri,
            'contexts': [x.serialize() for x in self.contexts]
        }

    @staticmethod
    def get_story(id):
        audio = Audio.query.filter_by(id=id).first()

        if audio.type != 'story':
            audio = None

        return audio

    @staticmethod
    def get_stories():
        return Audio.query.all()

    @staticmethod
    def get_ad():
        pass

    @staticmethod
    def get_new_id():
        # TODO: Potential race condition
        query = db.session.query(func.max(Audio.id).label('max_id')).one()
        max_id = query.max_id

        if max_id is None:
            max_id = 0

        return max_id + 1
