from app import db


class UserFacebook(db.Model):
    __tablename__ = 'userfacebook'
    user_id = db.Column(db.String(100), primary_key=True)
    subject = db.Column(db.String(20))

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<User %r>' % self.user_id
