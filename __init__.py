from flask import Flask, render_template, redirect, flash, session, request
from functions.auth.authentication import login
from functions.models.pdf import generatePdf
import os
import sys

app = Flask(__name__)
app.secret_key = os.urandom(33)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "GET":
        if not session.get('logged_in'):
            try:
                return redirect('/login')
            except Exception as ex:
                return str(ex)
        else:
            return render_template('home.html')
    else:
        return login(request.form['id'], request.form['psw'])


@app.route('/login')
def loginPage():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash("You have successfully logged out.")
    return redirect('/login')


@app.route('/pdf', methods=["POST"])
def createPdf():
    values = [
        request.form['name'],  # 0
        request.form['dateOfBirth'],  # 1
        request.form['passport'],  # 2
        request.form['startDate'],  # 3
        request.form['endDate'],  # 4
        request.form['country'],  # 5
        request.form.get('exclusive'),  # 6
        request.form['remunaration'],  # 7
        request.form.get('lump'),  # 8
        request.form.get('byClub'),  # 9
        request.form['signCity'],  # 10
        request.form['date']  # 11
    ]

    generatePdf("FVerbeeren", values)
    flash("The document has been created and saved in your Downloads folder.")
    return redirect('/')


@app.errorhandler(404)
def pageNotFound(e):
    try:
        return "Sorry, Page Not Found"
    except Exception as ex:
        return str(ex)


if __name__ == "__main__":
    app.run(debug=True)
