
from flask import Flask , render_template , url_for , redirect , flash , request


from flask_wtf import FlaskForm

from wtforms import StringField , PasswordField , SelectField , SubmitField
from wtforms.validators import DataRequired , Email , ValidationError
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager, login_manager , login_required , logout_user , login_user , UserMixin

app = Flask(__name__,template_folder='template')
app.config['SECRET_KEY'] = 'asff'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

Migrate(app,db)

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(user_id)

class user(db.Model , UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    hash_password = db.Column(db.String)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.hash_password = generate_password_hash(password)
    
    def check_pass(self,password):
        return check_password_hash(self.hash_password,password)
    
    def __repr__(self):
        return f"For {self.username} , Email is {self.email} , Password is {self.hash_password}"

class forms(FlaskForm):

    Username = StringField('Username',validators=[DataRequired()])
    Email = StringField('Email',validators=[DataRequired(),Email(message='Email not correct')])
    Password = PasswordField('Password')
    select = SelectField('So you Agree with terms',choices=[('yes','yes'),('no','no')])
    Submit = SubmitField('Submit')

    def check_email(self,field):
        if user.query.filter_by(email = field.data).first():
            return ValidationError(message='Email already exits')

class loginform(FlaskForm):

    Email = StringField('Email')
    Password = PasswordField('Password')
    Submit = SubmitField('Login')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out")

    return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
    form = forms()
    if form.validate_on_submit():
        db.create_all()

        u1 = user(form.Username.data,form.Email.data,form.Password.data)

        db.session.add(u1)
        db.session.commit()
        flash('Thanks for registration')
        return redirect(url_for('login'))

    return render_template('register.html',form = form)

@app.route('/thanku')
def thanku():
    users = user.query.all()
    return render_template('thanku.html',users = users)

@app.route('/login',methods=['GET','POST'])
def login():
    form = loginform()

    if form.validate_on_submit():

        User = user.query.filter_by(email = form.Email.data).first()

        if User.check_pass(form.Password.data) and User is not None:
            
            login_user(User)

            flash('You are successfully logged in')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')
            
            return redirect(next)

    return render_template ('login.html',form=form)



if __name__ == '__main__':
    app.run(debug=True)