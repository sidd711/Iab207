from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # use for quick forms
    bootstrap = Bootstrap(app)

    # initialise login manager
    login_manager = LoginManager()
    # set the view route for logging in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Create a user loader function takes userid and returns User
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.secret_key = 'secret_key'

    # Create database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicdb.sqlite'
    # db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://usvtpyfbrbmyzy:dd529f4bd126712b4875283705f61733dae88e4a970f34c74bd072b1133af688@ec2-34-228-154-153.compute-1.amazonaws.com:5432/d3cp5i1vhbds1p'
    db.init_app(app)

    # config upload folder
    UPLOAD_FOLDER = 'static/images/event_imgs/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # import main bp from views
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import event
    app.register_blueprint(event.bp)

    @app.errorhandler(404)
    def handle_404(err):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def handle_500(err):
        return render_template('500.html'), 500
    return app
