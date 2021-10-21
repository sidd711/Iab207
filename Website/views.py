from flask import Blueprint, render_template, url_for, flash, request, redirect, url_for
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
    return render_template('index.html', events=events)


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
    return render_template('index.html')
