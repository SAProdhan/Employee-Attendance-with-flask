from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from attendance.models import User, Employee, Shift
from wtforms_components import TimeField
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exits')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exits')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    update = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is not match with the email. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is not match with the username. Please choose a different one.')


class EmployeeForm(FlaskForm):
    id = IntegerField('Id:')
    name = StringField('Employee Name:')
    phone = IntegerField('Phone Number:')
    email = StringField('Email:')
    designation = StringField('Designation:')
    department = StringField('Department:')
    # shift = StringField('Select Shift:',
    #                        validators=[DataRequired()])
    cardno = StringField('Card No:')
    picture = FileField('Photo:', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    document = FileField('Add Documents:', validators=[FileAllowed(['jpg', 'png', 'jpeg','pdf', 'doc'])])
    Add = SubmitField('Add')
    Delete = SubmitField('Delete')
    Edit = SubmitField('Edit')
    Search = SubmitField('Search')
    def validate_id(self, id):
        user = Employee.query.filter_by(id=id.data).first()
        if user:
            raise ValidationError('Id already exits')
    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exits')
    def validate_cardno(self, cardno):
        user = Employee.query.filter_by(cardno=cardno.data).first()
        if user:
            raise ValidationError('Card already exits')
    def validate_phone(self, phone):
        user = Employee.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Phone number already exits')


class OrganizationForm(FlaskForm):
    designation = StringField('Designation:')
    department = StringField('Department name:')
    Add = SubmitField('Add')
    Delete = SubmitField('Delete')
    Edit = SubmitField('Edit')



class ShiftForm(FlaskForm):
    name = StringField('Shift name:', validators=[DataRequired()])
    start = TimeField('Start Time:', validators=[DataRequired()])
    end = TimeField('End Time', validators=[DataRequired()])
    holidays = StringField('Holidays')
    Add = SubmitField('Add')
    Delete = SubmitField('Delete')
    Edit = SubmitField('Edit')
 
