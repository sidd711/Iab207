from flask import Blueprint, render_template, url_for, flash, request, redirect, url_for
from . import db
import os
from werkzeug.utils import redirect, secure_filename
from .forms import CreateEvent
from .models import Event
from flask_login import login_required, current_user
from .models import Event

bp = Blueprint('main', __name__)

choices = ["Mixed Genre", "Pop", "Rock",
           "Country", "Blues", "Techno", "Hip hop"]


@bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events, choices=choices)


@bp.route('/search')
def search():
    if request.args["search"]:
        print(request.args['search'])
        event_search = "%" + request.args['search'] + '%'
        events = Event.query.filter(Event.title.like(event_search)).all()
        events += Event.query.filter(
            Event.description.like(event_search)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))


@bp.route('/genre')
def genre():
    if request.args["genredrop"] != 'all':
        print(request.args['genredrop'])
        event_search = request.args['genredrop']
        events = Event.query.filter(Event.type.like(event_search)).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
