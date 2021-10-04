from flask import Blueprint, render_template, url_for

from .forms import LoginForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')
