from flask import Flask,request, render_template, session, flash, redirect
import re
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, "login_reg")
app.secret_key = "very secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
    is_good = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email")
        is_good = False
 
    if len(request.form["first_name"]) and len(request.form["last_name"]) < 0:
        flash("First and Last Name are Required")
        is_good = False
    elif not request.form["first_name"].isalpha() and not request.form["last_name"].isalpha():
        flash("Invalid First Name")
        is_good = False
    
    if len(request.form["pword"]) < 8:
        flash("Password Must Be At Least 8 Characters")
        is_good = False
    elif request.form["pword"] != request.form["confpword"]:
        flash("Password Entries Do Not Match")
        is_good = False

    if is_good:
        user = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:firstn, :lastn, :email, :pword, NOW(), NOW())"
        data = {    
                'firstn': request.form["first_name"],
                'lastn': request.form["last_name"],
                'email': request.form["email"],
                'pword': request.form["pword"]
                }
        user_id = mysql.query_db(user,data)
        session["name"] = request.form["first_name"]
        session["user_id"] = user_id
        return redirect('/success')
    return redirect('/')
@app.route('/login', methods=["POST"])
def login():
    
    find_the_user = "SELECT * FROM users WHERE email = :email"
    data = { 'email': request.form["email"]}
    return_user = mysql.query_db(find_the_user, data)

    if len(return_user) == 0:
        flash("User Entered Is Not Registered")
    else:
        if return_user[0]["password"] != request.form["pword"]:
            flash("Password Is Incorrect")
        else:
            session["name"] = return_user[0]["first_name"]
            return redirect('/success')
    return redirect('/success')
@app.route('/success')
def success():
    return render_template('success.html')




app.run(debug=True)