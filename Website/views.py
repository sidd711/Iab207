from flask import Blueprint, render_template, url_for, flash
from . import db
import os
from werkzeug.utils import redirect, secure_filename
from .forms import CreateEvent
from .models import Event
from flask_login import login_required, current_user
from .models import Event

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events = events)


@bp.route('/create', methods=["GET", "POST"])
@login_required
def create():
    # instantiate the from to access input information from page
    form = CreateEvent()
    db_file_path = check_upload_file(form)
    # db_file_path = check_upload_file(form)
    if form.validate_on_submit():
        new_event = Event(title=form.title.data,
                          date=form.date.data,
                          starttime=form.starttime.data,
                          endtime=form.endtime.data,
                          address=form.address.data,
                          suburb=form.suburb.data,
                          city=form.city.data,
                          maxguests=form.maxguests.data,
                          image=db_file_path,
                          type=form.type.data,
                          description=form.description.data,
                          user=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created sucessfully.')
        return redirect(url_for('main.create'))
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
