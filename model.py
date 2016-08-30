from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()

DB_URI = 'postgresql:///speeches'

## TODO: FIGURE OUT AUTOINCREMENT RESET


class President(db.Model):
    """docstring for President"""

    __tablename__ = 'presidents'

    prez_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    speech = db.relationship('Speech')

    def __repr__(self):
        return '<ID={}, Name={}>'.format(self.prez_id, self.name)

    # POST MVP:
    # start_yr = db.Column(db.Integer, nullable=False)
    # end_yr = db.Column(db.Integer, nullable=False)


class Speech(db.Model):
    """docstring for Speech"""

    __tablename__ = 'speeches'

    speech_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))       # db.ForeignKey('speech_types.speech_type')
    speaker = db.Column(db.Integer, db.ForeignKey('presidents.prez_id'))
    link = db.Column(db.String(100), nullable=True)
    sentiment = db.Column(db.String(5))

    prez = db.relationship('President')

    # speechtype = db.relationship('SpeechTypes')

    speech_phrases = db.relationship('SpeechCollocation')

    def __repr__(self):
        return '<ID={}, Title: {}, President: {}, Sentiment: {}>'.format(self.speech_id,
                                                                         self.title, self.speaker, self.sentiment)


class Collocation(db.Model):
    """docstring for Collocations"""

    __tablename__ = 'collocations'

    phrase_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phrase = db.Column(db.String(75), nullable=False)
    sentiment_score = db.Column(db.String(5))

    connect = db.relationship('SpeechCollocation')

    def __repr__(self):
        return '<ID={}, Phrase={}>'.format(self.phrase_id, self.phrase)


class SpeechCollocation(db.Model):
    """docstring for SpeechCollocation"""

    __tablename__ = 'SpeechCollocations'

    connect_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    speech_id = db.Column(db.Integer, db.ForeignKey('speeches.speech_id'))
    phrase_id = db.Column(db.Integer, db.ForeignKey('collocations.phrase_id'))

    speech = db.relationship('Speech')
    phrase = db.relationship('Collocation')

    def __repr__(self):
        return '<ID={}, Speech ID={}, Phrase ID={}>'.format(self.connect_id, self.speech_id, self.phrase_id)


def connect_to_db(app):
    """Connect database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///speeches'
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    print 'Connected to DB!'
