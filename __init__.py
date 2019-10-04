import os
import datetime
# VANILA FLASK
from flask import Flask, render_template, redirect, flash, request

# LOGIN Manager
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, login_required, current_user

# DATABASE Manager
from flask_sqlalchemy import SQLAlchemy

# PROJECT FUNCTIONS
from functions.pdf import generatePdf
from functions.save import getDownloadPath
from db.encryption import encryptPsw


# --- INITIATE THE APP, THE DATABASE & THE LOGIN MANAGER ---
# Create the APP object & assign it a secret key
app = Flask(__name__)
app.secret_key = os.urandom(33)

# Link the database and create the DB object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/users.db'
db = SQLAlchemy(app)

# Create the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginPage'


# --- DEFINE THE DATABASE CLASSES THAT WILL BE USED BY THE APP ---
# Create the User Class that is linked to our DB & our User Manager
class User(UserMixin, db.Model):
    # Define the table in which it should be placed
    __tablename__ = "users"

    # Define the columns of a user (and thus of the table)
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String, unique=True)
    password = db.Column("password", db.String)


class Company(db.Model):
    # Define the tablename in which it should be placed
    __tablename__ = "companies"

    # Define the columns present in the Company class (and thus the table)
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("userid", db.String, db.ForeignKey("users.id"))
    name = db.Column("name", db.String)
    vat_nr = db.Column("vat_nr", db.String)
    street = db.Column("street", db.String)
    city = db.Column("city", db.String)
    country = db.Column("country", db.String)
    agent_name = db.Column("agent_name", db.String)
    agent_nr = db.Column("agent_nr", db.String)
    agent_country = db.Column("agent_country", db.String)

# Define the route to the User login
@login_manager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))


# --- DEFINE THE ROUTES OF THE APP ---
# Main page
@app.route('/')
@login_required
def home():
    try:
        return render_template('home.html')
    except Exception as ex:
        return str(ex)


# Create PDF page (transition page to redirect)
@app.route('/pdf', methods=["POST"])
def createPdf():
    user_id = current_user.id
    company = Company.query.filter_by(user_id=user_id).first()
    dob = str(datetime.datetime.strptime(
        request.form['dateOfBirth'], "%Y-%m-%d").strftime('%d/%m/%Y'))
    start = str(datetime.datetime.strptime(
        request.form['startDate'], "%Y-%m-%d").strftime('%d/%m/%Y'))
    end = str(datetime.datetime.strptime(
        request.form['endDate'], "%Y-%m-%d").strftime('%d/%m/%Y'))
    sign_date = str(datetime.datetime.strptime(
        request.form['date'], "%Y-%m-%d").strftime('%d/%m/%Y'))

    values = [
        request.form['name'], dob, request.form['passport'], start, end,
        request.form['country'], request.form.get('exclusive'),
        request.form['remunaration'], request.form.get('lump'),
        request.form.get('byClub'), request.form['signCity'], sign_date
    ]
    dest_path = getDownloadPath()
    generatePdf(company, values, dest_path)
    flash(
        "The document has been created and saved in your Downloads folder."
    )
    return redirect('/')


@app.route('/login', methods=["POST", "GET"])
def loginPage():
    # User entered credentials
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form['id']).first()

        # The entered username exists in the DataBase
        if user:
            hashed = encryptPsw(request.form['psw'])
            if user.password == hashed:  # Check password
                login_user(user, remember=True)
                name = Company.query.filter_by(user_id=user.id).first()
                name = name.agent_name
                flash("Welcome ! You are now logged in as %s." % (name))
                return redirect('/')
            else:
                flash("Your password was incorrect.")
                return redirect('login')
        else:
            flash("The given User Name does not exist")
            return redirect('login')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out.")
    return redirect('/login')


@app.errorhandler(404)
def pageNotFound(e):
    try:
        return "Sorry, Page Not Found"
    except Exception as ex:
        return str(ex)


if __name__ == "__main__":
    app.run(debug=True)
