from flask import Flask
from flask import flash




app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = '2sdad28bc4a13ce0c676dfde28031115'


from web import routes
from web import models
