from running import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    mail = db.Column(db.String(),unique=True)
    password = db.Column(db.String())
    cash = db.Column(db.Integer)

    def __init__(self, name, mail,password,cash):
        self.name = name
        self.mail = mail
        self.password = password
        self.cash = cash

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'mail': self.mail,
            'cash': self.cash
        }