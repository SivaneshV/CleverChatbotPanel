# %% Import(s)
from flask_cors import CORS
from flask import Flask, render_template


application = Flask(__name__, template_folder='template')
application.secret_key = 'POC1'
CORS(application)


@application.route('/home')
def home():
    return render_template('login.html')
