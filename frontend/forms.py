from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Optional

class IRForm(FlaskForm):
    keywords = StringField('Keywords', validators=[DataRequired()])
    attributes = StringField('Attributes')
    length = DecimalField('Length', places=3, validators = [Optional()])
    merge = BooleanField('Merge all attributes')
    submit = SubmitField('Start query')

class ResForm(FlaskForm):
    data = []
