from myapp import db


class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eng = db.Column(db.String(100), unique=True, nullable=True)
    rus = db.Column(db.String(100), nullable=True)
    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'))

    def __init__(self, *args, **kwargs):
        super(Words, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<eng: {self.eng}, rus: {self.rus}>'
