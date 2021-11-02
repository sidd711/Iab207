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
    # Uncomment this and comment out below to play with code locally through sqlite database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicdb.sqlite'
    # db.init_app(app)

    # Code here is for use when code it deployed via heroku
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bmgauhwbvbidsp:28c10ab1f4b6e8c76bc8ae149690cff1b58bca740e359f13d9cb720df6ecf25f@ec2-54-159-176-167.compute-1.amazonaws.com:5432/d6bivuubs5bp3j'
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
