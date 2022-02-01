from datetime import datetime

from myapp import db


class Dictionaries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    words = db.relationship('Words', backref='dictionary')

    def __init__(self, *args, **kwargs):
        super(Dictionaries, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Dict id: {self.id}, date: {self.date}>'
