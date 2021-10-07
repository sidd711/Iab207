from . import db
import os
from werkzeug.utils import redirect, secure_filename
from .forms import CreateEvent, CommentForm
from .models import Event, Comment, User
from flask import Blueprint, render_template, flash, url_for, request
from flask_login import login_required, current_user

bp = Blueprint('event', __name__, url_prefix='/events')


@bp.route('/<id>', methods=["GET", "POST"])
def show(id):
    cform = CommentForm()
    # create an event item accociated with the event id which is collected from the link
    event = Event.query.filter_by(id=id).first()

    event_user = User.query.filter_by(id=event.user).first()
    event_owner = event_user.name

    return render_template('event/show.html', event=event, form=cform, event_owner=event_owner)


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
