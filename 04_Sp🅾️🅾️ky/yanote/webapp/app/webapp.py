from flask import redirect, Flask, render_template, request, abort
from flask import url_for, send_from_directory, make_response, Response
import zlib
import os
import mysql.connector
import logging as log
import pickle

import secret

app = Flask(__name__)


class User:
    pass


def MAC(pickled_user):
    """
    Add message authentication code to user.
    Since nobody knows the key, nobody can change it!
    """
    return pickled_user.hex() + "-" + hex(zlib.crc32(secret.KEY + pickled_user))[2:]


def verify_mac(mac):
    user, crc_value = mac.split("-")
    crc_value = int(crc_value, 16)
    user_b = bytes.fromhex(user)
    valid_mac = zlib.crc32(secret.KEY + user_b)
    if crc_value == valid_mac:
        return pickle.loads(user_b)
    raise ValueError("Bad CRC-HMAC!")


def mac_user(username):
    user_obj = User()
    user_obj.username = username
    user_obj.permission = False

    user_pickle = pickle.dumps(user_obj)
    return MAC(user_pickle)


def check_user():
    user_mac = request.cookies.get('user')
    if user_mac is None:
        return None
    try:
        user = verify_mac(user_mac)
    except ValueError:
        abort(Response("Bad CRC-HMAC!"))
    return user
        


def connect_to_db():
    conn = mysql.connector.connect(host="db", user='dbuser', password='123456', database='users')
    cursor = conn.cursor()
    return conn, cursor

def do_query(stmt, args, insert=False):
    conn, cur = connect_to_db()
    cur.execute(stmt, args)
    if insert:
        conn.commit()
        res = None
    else:
        res = cur.fetchall()
    cur.close()
    conn.close()
    return res


def do_insert(stmt, args):
    do_query(stmt, args, True)



@app.route('/register', methods=["GET", "POST"])
def register():
    user = check_user()
    if user is not None:
        return redirect(url_for('notes'))

    msg = ""

    if request.method == "POST":
        try:
            _, cursor = connect_to_db()
            do_insert("INSERT INTO users (username, password) VALUES (%s, %s)", (request.form['username'], request.form['password']))
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:
            msg = "User with that name already exists"
            

    return render_template("register.html", msg=msg)


@app.route('/notes', methods=["GET", "POST"])
def notes():
    user = check_user()
    if user is None:
        return redirect(url_for("register"))

    if request.method == "POST":
        try:
            do_insert("INSERT INTO notes (content, username) VALUES (%s, %s)", (request.form['content'], user.username))
        except mysql.connector.Error as ex:
            log.error("Exception in notes: %s", str(ex))
    res = do_query("SELECT content FROM notes WHERE username=%s", (user.username,))
    notes = [x[0] for x in res]

    
    return render_template("notes.html", notes=notes, dance=user.permission)


@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        try:
            res = do_query("SELECT username, password FROM users WHERE username=%s AND password=%s", (request.form['username'], request.form['password']))
            print(res)
            if res is not None:
                resp = make_response(redirect(url_for("notes")))
                resp.set_cookie('user', mac_user(request.form['username']))
                return resp
        except mysql.connector.Error as ex:
            msg = "Ooops. Something went wrong."
            log.error("Exception in login: %s", str(ex))
        else:
            msg = "Invalid credentials!"

    return render_template("login.html", msg=msg)


@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/static/<path:p>')
def wtf(p):
    return send_from_directory("static", p)


if __name__ == '__main__':
    app.run()

