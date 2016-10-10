from nestor.errors import InvalidAttribute
from nestor.db import db

from sqlalchemy import func

ACTION_TYPES = ['start', 'finished', 'queued', 'shared', 'context', 'link']

class Action(db.Model):

    __tablename__ = 'action'

    id = db.Column('id', db.Integer, primary_key=True)
    client_id = db.Column('client_id', db.Integer, nullable=False)
    audio_id = db.Column('audio_id', db.Integer, db.ForeignKey('audio.id'), nullable=False)
    type = db.Column('type', db.String(10), nullable=False)
    audio_point = db.Column('audio_point', db.Integer, nullable=False)
    timestamp = db.Column('timestamp', db.Date, nullable=False)

    def __init__(self, id, client_id, audio_id, type, audio_point, timestamp):
        if id is None:
            id = Action.get_new_id()

        self.id = id
        self.client_id = client_id
        self.audio_id = audio_id
        self.type = type
        self.audio_point = audio_point
        self.timestamp = timestamp

        self.validate()

    def validate(self):
        if len(getattr(self, 'type')) < 1:
           raise InvalidAttribute('type is missing')

        if getattr(self, 'type', '') not in ACTION_TYPES:
            raise InvalidAttribute('type is not valid')

    @staticmethod
    def get_new_id():
        # TODO: Potential race condition
        query = db.session.query(func.max(Action.id).label('max_id')).one()
        max_id = query.max_id

        if max_id is None:
            max_id = 0

        return max_id + 1
