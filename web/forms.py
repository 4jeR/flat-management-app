from wtforms import Form
from wtforms import BooleanField 
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

class RegistrationForm(Form):
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasła muszą być identyczne.')
    ])
    confirm_password = PasswordField('Powtórz hasło')


class LoginForm(Form):
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
    ])




class RoomForm(Form):
    price = StringField('E-mail', [validators.Length(min=6, max=35)])
    flat_id = PasswordField('Hasło', [
        validators.DataRequired(),
    ])