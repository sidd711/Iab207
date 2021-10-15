from . import db
import os
from werkzeug.utils import redirect, secure_filename
from .forms import CreateEvent, CommentForm
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
    print(current_user.id)
    if form.validate_on_submit():

        new_event = Event(title=form.title.data,
                          date=form.date.data,
                          starttime=form.starttime.data,
                          endtime=form.endtime.data,
                          address=form.address.data,
                          city=form.city.data,
                          suburb=form.suburb.data,
                          maxguests=form.maxguests.data,
                          image=db_file_path,
                          type=form.type.data,
                          description=form.description.data,
                          description_header=form.description_header.data,
                          user=current_user.id
                          )
        db.session.add(new_event)
        db.session.commit()
        flash('Event created sucessfully.')
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
            BASE_PATH, 'static/images', secure_filename(filename))
        # store relative path in DB as image location in HTML is relative
        db_upload_path = '/static/images/' + secure_filename(filename)
        # save the file and return the db upload path
        fp.save(upload_path)
        return db_upload_path


@bp.route('/<id>', methods=["GET", "POST"])
def show(id):
    cform = CommentForm()
    # create an event item accociated with the event id which is collected from the link
    event = Event.query.filter_by(id=id).first()

    event_user = User.query.filter_by(id=event.users).first()
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
