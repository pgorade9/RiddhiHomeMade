import sqlalchemy
from pydantic import BaseModel
from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo
from config import engine, user


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
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        with engine.connect() as connection:
            query = sqlalchemy.delete(user).where(user.c.email == email)
            result = connection.execute(query).first()
            if result:
                raise ValidationError("That email is already taken. Please take a different one")
