from flask import session
import os
from datetime import timedelta


def generic_session_key():
    key = os.urandom(20).hex()
    return key
