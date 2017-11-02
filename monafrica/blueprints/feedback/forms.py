from flask_wtf import Form
from wtforms import TextAreaField, TextField
from wtforms_components import EmailField
from wtforms.validators import DataRequired, Length


class FeedbackForm(Form):
    name = TextField("What's your name?",
                     [DataRequired(), Length(3, 254)])
    email = EmailField("What's your email address?",
                       [DataRequired(), Length(3, 254)])
    message = TextAreaField("What Feedback would you like to give?",
                            [DataRequired(), Length(1, 8192)])