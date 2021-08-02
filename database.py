from flask_sqlalchemy import SQLAlchemy
import os
from index import app
from werkzeug.security import generate_password_hash , check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class user(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f"For {self.username} , Email is {self.email} , Passwoed is {self.password}"