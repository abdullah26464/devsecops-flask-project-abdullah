#!/usr/bin/env python3
import os
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect

from db_seed import setup_db
from routes import init

app = Flask(__name__)

# ✅ Enforce environment variable for secret key
secret_key = os.environ.get("FLASK_SECRET_KEY")
if not secret_key:
    raise RuntimeError("FLASK_SECRET_KEY environment variable is not set!")
app.config["SECRET_KEY"] = secret_key

# ✅ Enable CSRF protection
app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("WTF_CSRF_SECRET_KEY", secret_key)
csrf = CSRFProtect(app)

# ✅ Local assets (safer than remote CDN)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
app.config["CKEDITOR_SERVE_LOCAL"] = True

bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)
ckeditor = CKEditor(app)

# ✅ Pass app into init & setup_db (safer practice)
init(app)
setup_db(app)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(error):
    # ✅ No f-strings, Jinja auto-escapes output
    detailed_message = f"{error}. Requested URL was {request.path}"
    return render_template("404.html", detailed_message=detailed_message), 404

if __name__ == "__main__":
    # ✅ Never use debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=False)
