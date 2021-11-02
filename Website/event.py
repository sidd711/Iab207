from . import db
import os
from werkzeug.utils import redirect, secure_filename
from .forms import BookEvent, CreateEvent, CommentForm, UpdateEvent, BookEvent
from .models import Booking, Event, Comment, User
from flask import Blueprint, render_template, flash, url_for, request
from flask_login import login_required, current_user
from datetime import date, time


bp = Blueprint('event', __name__, url_prefix='/events')

# Route for event creation
@bp.route('/create', methods=["GET", "POST"])
@login_required
def create():
    # instantiate the from to access input information from page
    form = CreateEvent()
    db_file_path = check_upload_file(form)
    if form.validate_on_submit():
        new_event = Event(title=form.title.data,
                          startdate=form.startdate.data,
                          enddate=form.enddate.data,
                          starttime=form.starttime.data,
                          endtime=form.endtime.data,
                          address=form.address.data,
                          city=form.city.data,
                          suburb=form.suburb.data,
                          maxguests=form.maxguests.data,
                          image=db_file_path,
                          type=form.type.data,
                          status="Upcoming",
                          description=form.description.data,
                          description_header=form.description_header.data,
                          user=current_user.id,
                          artist=form.artist.data
                          )
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully.')
        return redirect(url_for('event.create'))
    return render_template('forms.html', form=form, heading="Create an Event")


# Funtion to ensure correct formatting and deposition if image files
def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    if fp:
        filename = fp.filename
        # get the current path of the module file… store image file relative to this path
        BASE_PATH = os.path.dirname(__file__)
        # upload file location – directory of this file/static/image
        upload_path = os.path.join(
            BASE_PATH, 'static/images/event_imgs/', secure_filename(filename))
        # store relative path in DB as image location in HTML is relative
        db_upload_path = 'static/images/event_imgs/' + \
            secure_filename(filename)
        # save the file and return the db upload path
        fp.save(upload_path)
        return db_upload_path

# Route to show event details
@bp.route('/<id>', methods=["GET", "POST"])
def show(id):
    cform = CommentForm()
    bform = BookEvent()
    # create an event item accociated with the event id which is collected from the link
    event = Event.query.filter_by(id=id).first()
    event_user = User.query.filter_by(id=event.user).first()
    event_owner = event_user.name
    return render_template('event/show.html', event=event, form=cform, bform=bform, event_owner=event_owner)


# Route for users to leave comments
@bp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    
    # get the destination object associated to the page and the comment
    event_obj = Event.query.filter_by(id=id).first()
    if form.validate_on_submit():
        # read the comment from the form
        if len(form.text.data) > 250:
            flash("Comment too long.")
        else:
            comment = Comment(text=form.text.data,
                            event_id=event_obj.id,
                            user=current_user.id)
            # here the back-referencing works - comment.destination is set
            # and the link is created

            db.session.add(comment)
            db.session.commit()
            # flashing a message which needs to be handled by the html
            flash('Your review has been added')
            print('Comment added sucessfully')
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))


# Route to provide booking functionality
@bp.route('/<id>/book', methods=['GET', 'POST'])
@login_required
def book(id):
    form = BookEvent()
    # get the destination object associated to the page and the booking
    event_obj = Event.query.filter_by(id=id).first()
    if form.validate_on_submit():
        # add funtionality here to update event max_guests number based on form number input
        # if the form number is greated then the number avaiable flash() message and redirect
        remaining_bookings = event_obj.maxguests
        new_bookings = form.attending.data
        if new_bookings > remaining_bookings:
            flash("Not enough spots.")
            return redirect(url_for('event.show', id=id))
        else:
        # read the booking from the form (only info it needs really should be user and number for booking, rest is foreign keys)
            booking = Booking(event_id=event_obj.id,
                              user=current_user.id,
                              attending = new_bookings)
            
            db.session.add(booking)
            event_obj.maxguests -= new_bookings
            if event_obj.maxguests == 0:
                event_obj.status = "Booked Out"
            db.session.commit()
            # flashing a message which needs to be handled by the html
            # flash('Your comment has been added', 'success')
            print('Booking added sucessfully')
            print(event_obj.maxguests)
            flash("Booking successfull. Booking ID: " +str(booking.id) + ". View in NavBar > Events > Booked Events.")
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))


# Route to view users owned events
@bp.route('/myevents')
@login_required
def myevents():
    events = Event.query.filter_by(user=current_user.id).all()
    if not events:
        flash("You currently do not have any events", 'error')
        return redirect(url_for('event.create'))

    return render_template('event/myevents.html', events=events)


# Route to view users event bookings
@bp.route('/mybookings')
@login_required
def bookings():
    bookings = Booking.query.filter_by(user=current_user.id).all()
    return render_template('event/bookedevents.html', bookings=bookings)


# Route to provide update event functionality
@bp.route('/<id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    event = Event.query.filter_by(id=id).first()
    form = UpdateEvent()

    form.title.data = event.title
    form.startdate.data = event.startdate
    form.enddate.data = event.enddate
    form.starttime.data = event.starttime
    form.endtime.data = event.endtime
    form.address.data = event.address
    form.city.data = event.city
    form.suburb.data = event.suburb
    form.type.data = event.type
    form.status.data = event.status
    form.description.data = event.description
    form.artist.data = event.artist
    form.description_header.data = event.description_header

    if form.validate_on_submit():
        # create two new date and time object from the old date strings
        newstartdate = create_date(request.form["startdate"])
        newenddate = create_date(request.form["enddate"])
        newstarttime = create_time(request.form["starttime"])
        newendtime = create_time(request.form["endtime"])
        print("newstart" + str(newstartdate))
        print("newend" + str(newenddate))
        # If start date is after end date flash message to user
        if newstartdate > newenddate:
            flash("End Date cannot be prior to start date")
            return redirect(url_for('event.update', id=id))
        else:
            event.startdate = newstartdate
            event.enddate = newenddate
            event.title = request.form["title"]
            event.starttime = newstarttime
            event.endtime = newendtime
            event.address = request.form["address"]
            event.city = request.form["city"]
            event.suburb = request.form["city"]
            event.type = request.form["type"]
            event.status = request.form["status"]
            event.description = request.form["description"]
            event.artist = request.form["artist"]
            event.description_header = request.form["description_header"]
            db.session.commit()
            print('Event updated successfully')
            flash("Event updated successfully")
            return redirect(url_for('event.myevents'))
    else:
        return render_template('forms.html', form=form, heading="Update", id=id)


# method that takes a string of a date and converts it into new date object (needed for the database to re-accept them)
def create_date(date_string):
    yearint = int(date_string[0:4])
    monthint = int(date_string[5:7])
    dayint = int(date_string[8:10])
    print(f"Year:" + str(yearint) + ", month:" +
          str(monthint) + ", day:" + str(dayint))
    newdate = date(yearint, monthint, dayint)
    print(newdate)
    return newdate

# method that takes a string of a time and converts it into new time object (needed for the database to re-accept them)
def create_time(time_string):
    hourint = int(time_string[0:2])
    minuteint = int(time_string[3:5])
    print(f"Hour:" + str(hourint) + ", minutes:" + str(minuteint))
    newtime = time(hourint, minuteint)
    print(newtime)
    return newtime


# Route to provide event deletion functionality
@bp.route('/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    # delete the bookings accociated with the event or we get key problems
    bookings = Booking.query.filter_by(event_id=id).all()
    for booking in bookings:
        db.session.delete(booking)
    event = Event.query.filter_by(id=id).first()
    db.session.delete(event)
    db.session.commit()
    print('Event deleted successfully')
    flash("Event deleted successfully")
    return redirect(url_for('event.myevents'))

