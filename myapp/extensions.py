import random
from myapp.models.dictionaries import Dictionaries  # noqa
from myapp.models.words import Words  # noqa
from myapp import db


class SQLAlchemyDataBase:
    def __init__(self, db):
        self.db = db

    def check_existence(self, value):
        if value.isdecimal():
            value = self.db.session.query(Dictionaries).filter_by(id=value).first()
        else:
            value = self.db.session.query(Words).filter_by(eng=value).first()

        if value:
            return True
        else:
            return False

    def check_limit(self, num):
        amount = self.db.session.query(Words).filter_by(dictionary_id=num).count()
        if amount >= 30:
            return True
        else:
            return False

    def create_dict(self, num):
        d = Dictionaries(id=num)
        self.db.session.add(d)
        self.db.session.commit()

    def add_word(self, num, eng, rus):
        w = Words(eng=eng, rus=rus, dictionary_id=num)
        self.db.session.add(w)
        self.db.session.commit()

    def get_words(self, num):
        hash_words = self.db.session.query(Words).filter_by(dictionary_id=num).all()
        words = [[w.eng, w.rus] for w in hash_words]
        random.shuffle(words)
        return words
