from wtforms import Form, SelectField, TextAreaField
from wtforms.fields.core import StringField


class PostForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')
    