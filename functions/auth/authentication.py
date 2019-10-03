from flask import render_template, redirect, session, flash
from db.temporary_db import users


def login(user, psw):
    if user in users and psw == users[user]:
        session['logged_in'] = True
        return render_template('home.html')
    else:
        msg = str(
            "The username and/or password you have introduced were " +
            "not correct."
        )
        flash(msg)
        return redirect('login')
