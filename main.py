from Website import create_app
from flask import render_template
if __name__=='__main__':
    n_app=create_app()
    n_app.run(debug=True)