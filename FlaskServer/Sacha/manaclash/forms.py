from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf
from wtforms.validators import ValidationError
from manaclash.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                           Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
                       'Confirm Password',
                       validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account is assiociated with this email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already used.')


class CardForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = StringField(
                'Category',
                validators=[DataRequired(), AnyOf('Creature', 'Enchantment')])
    creature_type = StringField(
                        'Type (creature)',
                        validators=[AnyOf('Humanoid', 'Beast', 'Spirit')])
    enchantment_type = StringField(
                        'Type (enchantment)',
                        validators=[AnyOf('Ephemeral', 'Ongoing')])
    effect = TextAreaField('Effect', validators=[DataRequired()])
    mana_cost = IntegerField('Cost', validators=[DataRequired()])
    attack = IntegerField('Attack', validators=[DataRequired()])
    defense = IntegerField('Defense', validators=[DataRequired()])
    submit = SubmitField('Card')
