from flask import Flask
from datetime import timedelta
from sessions.session import generic_session_key
from handlers import bp, base_bp

app = Flask(__name__)

app.secret_key = generic_session_key()
app.permanent_session_lifetime = timedelta(days=1)

app.register_blueprint(bp, url_prefix='/router')
app.register_blueprint(base_bp, url_prefix='/base')

app.static_folder = 'static'
app.template_folder = 'templates'