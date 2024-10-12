from flask import Flask, render_template
from  utils.database import DataBaseRegister
from settings import settings

app = Flask(__name__)
app.config['DATABASE_URL'] = settings.DATABASE_URL.get_secret_value()


