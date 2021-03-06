from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, FileField, SelectField, RadioField
from wtforms.fields.core import IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo,NumberRange
from flask_wtf.file import FileRequired, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}

# Code containing form fields with types and requirements

class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])
    contact_no = IntegerField("Contact No", validators=[InputRequired(),NumberRange(min=400000000, max=499999999,message='Please use national moblie format (4XXXXXXXX) ')])
    address = StringField(" Address", validators=[InputRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),Length(min=4, max=20),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    image = FileField('Profile Picture', validators=[
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    # submit button
    submit = SubmitField("Register")


class CreateEvent(FlaskForm):
    title = StringField("Title",
                        validators=[InputRequired()]
                        )
    startdate = DateField("Date",
                          validators=[InputRequired()])
    enddate = DateField("Date",
                        validators=[InputRequired()])
    starttime = TimeField("Start Time", validators=[InputRequired()])
    endtime = TimeField("End Time", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    suburb = StringField("Suburb", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    artist = StringField("City", validators=[InputRequired()])
    maxguests = IntegerField("Max Guests", validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    type = SelectField("Genre", choices=[("Mixed Genre","Mixed Genre"), ("Pop", "Pop"),
                       ("Rock", "Rock"), ("Country", "Country"), ("Blues", "Blues"), ("Techno", "Techno"), ("Hip hop", "Hip hop")])
    description = TextAreaField("Description", validators=[InputRequired()])
    description_header = StringField(
        "Description Header", validators=[InputRequired()])

    submit = SubmitField("Create Event")


class CommentForm(FlaskForm):
    text = TextAreaField('Leave a Review', [InputRequired()])
    submit = SubmitField('Post')


class UpdateEvent(FlaskForm):
    title = StringField("Title",
                        validators=[InputRequired()]
                        )
    startdate = DateField("Date",
                          validators=[InputRequired()])
    enddate = DateField("Date",
                        validators=[InputRequired()])
    starttime = TimeField("Start Time", validators=[InputRequired()])
    endtime = TimeField("End Time", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    suburb = StringField("Suburb", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    artist = StringField("City", validators=[InputRequired()])
    # image = FileField('Event Image', validators=[
    #     FileRequired(message='Image cannot be empty'),
    #     FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    type = SelectField(choices= [('Mixed Genre','Mixed Genre'),('Pop','Pop'),('Rock','Rock'),('Country','Country'),('Blues','Blues'),('Techno','Techno'),('Hip hop','Hip hop')])
    status = SelectField(
        choices=[("Upcoming", "Upcoming"), ("Cancelled", "Cancelled"), ("Inactive", "Inactive"), ("Booked Out", "Booked Out")])
    description = TextAreaField("Description", validators=[InputRequired()])
    description_header = StringField(
        "Description Header", validators=[InputRequired()])

    submit = SubmitField("Update Event")

class BookEvent(FlaskForm):
    attending = IntegerField("How many bookings", validators=[InputRequired()])
    submit = SubmitField("Create Booking")
