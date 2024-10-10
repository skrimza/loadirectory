from datetime import timedelta
from flask import Flask
from sessions.session import generic_session_key
from settings import settings


app = Flask(__name__)

app.config['DATABASE_URL'] = settings.DATABASE_URL.get_secret_value()


app.secret_key = generic_session_key()
app.permanent_session_lifetime = timedelta(days=1)


    