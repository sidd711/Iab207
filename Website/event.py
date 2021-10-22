from . import db
import os
from werkzeug.utils import redirect, secure_filename
from .forms import CreateEvent, CommentForm, UpdateEvent
from .models import Event, Comment, User
from flask import Blueprint, render_template, flash, url_for, request
from flask_login import login_required, current_user

bp = Blueprint('event', __name__, url_prefix='/events')


@bp.route('/all', methods=["GET", "POST"])
def show_all():

    events = Event.query.all()
    return render_template('event/show_all.html', events=events)


@bp.route('/create', methods=["GET", "POST"])
@login_required
def create():
    # instantiate the from to access input information from page
    form = CreateEvent()
    db_file_path = check_upload_file(form)
    # db_file_path = check_upload_file(form)
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


@bp.route('/<id>', methods=["GET", "POST"])
def show(id):
    cform = CommentForm()
    # create an event item accociated with the event id which is collected from the link
    event = Event.query.filter_by(id=id).first()

    event_user = User.query.filter_by(id=event.user).first()
    event_owner = event_user.name
    # create a new variable that contains the event comments -is this a list? uncertain print it
    event_comments = event.comments

    return render_template('event/show.html', event=event, form=cform, event_owner=event_owner, comment_no=5)


@bp.route('/<event>/comment', methods=['GET', 'POST'])
def comment(event):
    form = CommentForm()
    # get a list of users to use for name retrieval
    Users = User.query.all()
    # get the destination object associated to the page and the comment
    event_obj = Event.query.filter_by(id=event).first()
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data,
                          event_id=event_obj.id,
                          user=current_user.name)
        # here the back-referencing works - comment.destination is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()
        # flashing a message which needs to be handled by the html
        # flash('Your comment has been added', 'success')
        print('Comment added sucessfully')
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=event))


@bp.route('/myevents')
@login_required
def myevents():
    print(current_user.id)
    events = Event.query.filter_by(user=current_user.id).all()
    return render_template('event/myevents.html', events=events)


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
    form.maxguests.data = event.maxguests
    # form.image.data = event.image
    form.type.data = event.type
    form.status.data = event.status
    form.description.data = event.description
    form.artist.data = event.artist
    form.description_header.data = event.description_header

    if form.validate_on_submit():
        event.title = form.title.data

        event.startdate = form.startdate.data
        event.enddate = form.enddate.data
        event.starttime = form.starttime.data
        event.endtime = form.endtime.data
        event.address = form.address.data
        event.city = form.city.data
        event.suburb = form.city.data
        event.maxguests = form.maxguests.data
        event.type = form.type.data
        event.status = form.status.data
        event.description = form.description.data
        event.artist = form.artist.data
        event.description_header = form.description_header.data
        db.session.commit()
        print('Event updated successfully')
        return redirect(url_for('event.myevents'))
    else:
        return render_template('forms.html', form=form, heading="Update", id=id)
