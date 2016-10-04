from nestor.db import db

class Story(db.Model):

    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    author = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    text_uri = db.Column(db.String(1000), nullable=False)
    audio_uri = db.Column(db.String(1000), nullable=False)

    def __init__(self, id, title, author, description, text_uri, audio_uri):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.text_uri = text_uri
        self.audio_uri = audio_uri

    def __repr__(self):
        return '<title {}>'.format(self.title)
