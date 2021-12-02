from app import db


class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.column(db.String(50))
    password = db.Column(db.String(20))

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
