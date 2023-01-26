from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,TextAreaField,SubmitField



class Post_form(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])

    submit = SubmitField('Post', validators=[DataRequired()])