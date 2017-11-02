from datetime import datetime

from lib.util_sqlalchemy import ResourceMixin
from monafrica.extensions import db


class Post(ResourceMixin, db.Model):
    """
        Create Department Table
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                          nullable=False)

    def __repr__(self):
        return '<Post: {}>'.format(self.title)