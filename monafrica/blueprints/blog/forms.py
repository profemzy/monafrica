from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(Form):
    """
        Form for admin to add or edit posts
    """
    title = StringField('Name', [DataRequired(), Length(3, 254)])
    content = TextAreaField('Content', [DataRequired(), Length(1, 8192)])
    submit = SubmitField('Submit')
