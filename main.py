from datetime import timedelta
from flask import Flask
from sessions.session import generic_session_key


app = Flask(__name__)




app.secret_key = generic_session_key()
app.permanent_session_lifetime = timedelta(days=1)

