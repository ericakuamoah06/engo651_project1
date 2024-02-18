import os
import csv
from flask import Flask, session, request, render_template, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
   raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('postgresql://postgres:hideurs06@localhost:5432/postgres')
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    # Check if user is logged in and redirect accordingly
    if 'username' in session:
        return render_template('search.html', username=session['username'])         
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    # Process login form data
    username = request.form.get("username")
    password = request.form.get("password")
    # Validate form input
    if not username or not password:
        flash("Error: Username or password cannot be empty.")
        return render_template("index.html")
    # Verify username and password against database
    # user = db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    user = db.execute(text("SELECT * FROM users WHERE (username=:username)"),{"username": username}).fetchone()
    match = db.execute(text("SELECT * FROM users WHERE username=:username AND password=:password"),{"username":username, "password":password}).fetchone()
    # if user and user["password"] == password:
    #     session['username'] = username
    #     flash("Logged in successfully.")
    #     return render_template("search.html", username=username)
    # else:
    #     flash("Error: Invalid username or password.")
    #     return render_template("index.html")

    if user is not None:
        if match is not None:
            session['username'] = username
            flash("Logged in successfully.")
            return render_template("search.html", username=username)
        else:
            flash("Error: Invalid Username")
            return render_template("index.html")
    else:
        flash("Error: Invalid username or password.")
        return render_template("index.html")
    
@app.route("/register_form", methods=['GET'])
def register_form():
    # Display the registration form
    return render_template("register.html")

@app.route("/register", methods=['POST'])
def register():
    # Process registration form data
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    # Check if username or email already exists
    if db.execute(text("SELECT * FROM users WHERE username = :username OR email = :email"), {"username": username, "email": email}).rowcount > 0:
        flash("Username or email already exists.")
        return render_template("register.html")
    # Insert new user into the database
    db.execute(text("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)"), {"username": username, "password": password, "email": email})
    db.commit()
    session['username'] = username
    flash("Registration successful.")
    return render_template("search.html", username=username)

@app.route("/logout", methods=['GET'])
def logout():
    # Clear the user session to log out
    session.pop('username', None)
    flash("Logged out successfully.")
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def search():
    # Process search form data
    query = "%" + request.form.get("content") + "%"
    books = db.execute(text("SELECT * FROM books WHERE title LIKE :query OR author LIKE :query OR isbn LIKE :query"), {"query": query}).fetchall()
    return render_template('search.html', results=books, username=session.get('username'))

@app.route("/book/<isbn>", methods=['GET', 'POST'])
def book(isbn):
    # Display book details and process new reviews
    book_details = db.execute(text("SELECT * FROM books WHERE isbn = :isbn"), {"isbn": isbn}).fetchone()
    reviews = db.execute(text("SELECT username, comment, rating FROM reviews WHERE isbn = :isbn"), {"isbn": isbn}).fetchall()
    if request.method == "POST":
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        db.execute(text("INSERT INTO reviews (username, isbn, comment, rating) VALUES (:username, :isbn, :comment, :rating)"), {"username": session['username'], "isbn": isbn, "comment": comment, "rating": rating})
        db.commit()
        flash('Review submitted!')
        reviews = db.execute(text("SELECT username, comment, rating FROM reviews WHERE isbn = :isbn"), {"isbn": isbn}).fetchall()
        return render_template("book.html", book=book_details, reviews=reviews, username=session['username'])
    return render_template("book.html", book=book_details, reviews=reviews, username=session['username'])