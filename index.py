from flask import Flask , render_template , url_for , redirect
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SelectField , SubmitField
from wtforms.validators import DataRequired , Email
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash , check_password_hash

app = Flask(__name__,template_folder='template')
app.config['SECRET_KEY'] = 'asff'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

Migrate(app,db)

class user(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def __repr__(self):
        return f"For {self.username} , Email is {self.email} , Password is {self.password}"

class forms(FlaskForm):

    Username = StringField('Username',validators=[DataRequired()])
    Email = StringField('Email',validators=[DataRequired(),Email()])
    Password = PasswordField('Password')
    select = SelectField('So you Agree with terms',choices=[('yes','yes'),('no','no')])
    Submit = SubmitField('Submit')

class loginform(FlaskForm):

    Email = StringField('Email')
    Password = PasswordField('Password')
    Submit = SubmitField('Login')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def register():
    form = forms()
    if form.validate_on_submit():
        db.create_all()

        u1 = user(form.Username.data,form.Email.data,form.Password.data)

        db.session.add(u1)
        db.session.commit()
        return redirect(url_for('thanku'))

    return render_template('register.html',form = form)

@app.route('/thanku')
def thanku():
    users = user.query.all()
    return render_template('thanku.html',users = users)

@app.route('/login')
def login():
    form = loginform()
    return render_template ('login.html',form=form)



if __name__ == '__main__':
    app.run(debug=True)