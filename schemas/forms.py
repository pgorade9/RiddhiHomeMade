import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Session
from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo

# from config import engine, user
import models


class LoginForm(Form):
    email = StringField('User Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Submit")


class RegistrationForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # image = FileField('Picture')
    submit = SubmitField('Sign Up')

    def validate_email(self, db: Session, email):
        result = db.query(models.User).filter(models.User.email == email).first()
        if result:
            raise ValidationError("That email is already taken. Please take a different one")
