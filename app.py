from datetime import timedelta
from main import app
from sessions.session import generic_session_key
from handlers.routes import all_bp


app.register_blueprint(all_bp, url_prefix='path')


app.secret_key = generic_session_key()
app.permanent_session_lifetime = timedelta(days=1)