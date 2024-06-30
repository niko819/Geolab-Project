from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, length, Email
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=8, max=24)])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), length(min=8, max=24)])
    submit = SubmitField("Submit")

class ProductForm(FlaskForm):
    img = FileField("Product Photo")
    name = StringField("Product Name", validators=[DataRequired()])
    price = IntegerField("Product Price", validators=[DataRequired()])
    submit = SubmitField("Product Upload")

class ContactForm(FlaskForm):
    username = StringField("username")
    email = StringField("mmail", validators=[DataRequired()])
    message = TextAreaField("message")
    submit = SubmitField("Submit Text")
