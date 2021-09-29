from flask import Blueprint,render_template,url_for

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    # print(url_for('index.html'))
    return render_template('n10867384_Demecillo/index.html')