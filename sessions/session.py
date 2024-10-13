import os


def generic_session_key():
    key = os.urandom(20).hex()
    return key
