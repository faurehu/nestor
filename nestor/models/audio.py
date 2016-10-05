from nestor.db import db

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

    def __repr__(self):
        return '< title {} - type {} >'.format(self.title, self.type)
