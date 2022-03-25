from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField
)
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    lang = SelectField('Language', validators=[DataRequired()], choices=['en', 'et'])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
