from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField
)
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    ValidationError
)


class ActorInnerJoinForm(FlaskForm):
    actor1 = StringField('First Actor', validators=[DataRequired(), Length(min=2)])
    actor2 = StringField('Second Actor', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('InnerJoin!')
