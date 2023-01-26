from flask_wtf import FlaskForm,RecaptchaField
from flask_wtf.file import  FileAllowed
from wtforms import StringField,PasswordField,BooleanField,SubmitField,DateField,DateTimeField,FileField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_login import current_user



class Regestration(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Password',validators=[DataRequired()])
    Confirm_Password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign in',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    Datefield_entry=DateField('Enter your date',format='%Y-%m-%d')






class Log_in_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in', validators=[DataRequired()])


class Account_form(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture_file = FileField('choose a profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update', validators=[DataRequired()])

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first
            if user:
                raise ValidationError('this Name is already taken please chose another name!','danger')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first
            if user:
                raise ValidationError('this Email is already taken please chose another name!','danger')

class Post_form(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])

    submit = SubmitField('Post', validators=[DataRequired()])

class Request_Reset(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('reset Password', validators=[DataRequired()])

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first
        if user is None:
            raise ValidationError('this Email is already taken please chose another name!', 'danger')

class Reset_password(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    Confirm_Password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset', validators=[DataRequired()])

    def validate_password(self, password):
        user = User.query.filter_by(email=password.data).first
        if user :
            raise ValidationError('this password is already taken choose another password!', 'danger')


from flaskblog.models import User
