#!/usr/bin/env python3
import os
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask import Flask, render_template, render_template_string, request, redirect

from db_seed import setup_db
from routes import init

app = Flask(__name__)

# Use environment variable for secret key to avoid hardcoding secrets
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'change_this_to_a_strong_secret')

app.config["BOOTSTRAP_SERVE_LOCAL"] = True
app.config["CKEDITOR_SERVE_LOCAL"] = True

bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

ckeditor = CKEditor()
ckeditor.init_app(app)

init()
setup_db()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")

@app.errorhandler(404)
def page_not_found(error):
    detailed_message = render_template_string(f"{error}. Requested URL was {request.path}")
    return render_template("404.html", detailed_message=detailed_message), 404

if __name__ == "__main__":
    # Turn off debug mode for production
    app.run(host="0.0.0.0", port=5000, debug=False)
