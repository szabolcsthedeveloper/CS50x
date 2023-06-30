import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Create users table if it doesn't exist
db.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC DEFAULT 10000.00)"
)

# Create history table if it doesn't exist
db.execute(
    "CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, symbol TEXT NOT NULL, amount INTEGER NOT NULL, price NUMERIC NOT NULL, time DATETIME NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))"
)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    temp = db.execute(
        "SELECT symbol, SUM(amount) AS amount FROM history GROUP BY symbol, user_id HAVING user_id = ?", session["user_id"])
    user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    user[0]["total"] = user[0]["cash"]
    stocks = []

    for stock in temp:
        company = lookup(stock["symbol"])

        stock["price"] = company["price"]
        stock["name"] = company["name"]
        stock["total"] = company["price"] * stock["amount"]
        user[0]["total"] += stock["total"]

        if stock["amount"] != 0:
            stocks.append(stock)

    return render_template("index.html", stocks=stocks, user=user[0])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        company = lookup(request.form.get("symbol"))
        temp = request.form.get("shares")
        amount = float(temp) if temp and temp.isnumeric() else 0

        if not company:
            return apology("invalid symbol", 400)
        if amount < 1 or not amount.is_integer():
            return apology("amount must be a whole number greater than zero", 400)

        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if company["price"] * amount > user[0]["cash"]:
            return apology("not enough cash balance", 400)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", user[0]["cash"] - company["price"] * amount, user[0]["id"])
        db.execute("INSERT INTO history (user_id, symbol, amount, price, time) VALUES (?, ?, ?, ?, datetime('now', 'localtime'))",
                    user[0]["id"], company["symbol"], amount, company["price"])

        return redirect("/")

    else:
        return render_template("buy.html", sym=request.args.get("sym"))


@app.route("/history")
@login_required
def history():
    history = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY time DESC", session["user_id"])

    for row in history:
        row["type"] = 'BOUGHT' if row["amount"] > 0 else 'SOLD'
        row["amount"] = abs(row["amount"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        info = lookup(request.form.get("symbol"))
        if not info:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", info=info)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        check = db.execute("SELECT * FROM users WHERE username = ?", username)

        if check or not username:
            return apology("invalid username", 400)
        if not password:
            return apology("password cannot be empty", 400)
        if password != confirm:
            return apology("password and confirm password doesn't match", 400)


        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        company = lookup(request.form.get("symbol"))
        temp = request.form.get("shares")
        amount = float(temp) if temp and temp.isnumeric() else 0

        user = db.execute("SELECT user_id, symbol, SUM(amount) AS amount FROM history GROUP BY symbol, user_id HAVING user_id = ? AND symbol = ?",
                           session["user_id"], company["symbol"])

        if not company or not user:
            return apology("invalid symbol", 403)
        user[0]["cash"] = db.execute("SELECT cash FROM users WHERE id = ?", user[0]["user_id"])[0]["cash"]

        if amount < 1 or not amount.is_integer():
            return apology("amount must be a whole number greater than zero", 400)
        if amount > user[0]["amount"]:
            return apology("you don't own enough shares", 400)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", user[0]["cash"] + company["price"] * amount, user[0]["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, amount, price, time) VALUES (?, ?, ?, ?, datetime('now', 'localtime'))",
                    user[0]["user_id"], company["symbol"], -amount, company["price"])

        return redirect("/")

    else:
        temp = db.execute("SELECT symbol, SUM(amount) as amount FROM history GROUP BY symbol, user_id HAVING user_id = ?", session["user_id"])
        symbols = []
        sym = request.args.get("sym")

        for stock in temp:
            if stock["amount"] != 0 and stock["symbol"] != sym:
                symbols.append(stock)

        return render_template("sell.html", symbols=symbols, sym=sym)


@app.route("/change", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old = request.form.get("oldpassword")
        new = request.form.get("newpassword")
        confirm = request.form.get("confirm")

        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if not check_password_hash(user[0]["hash"], old):
            return apology("old password doesn't match", 400)
        if not new:
            return apology("password cannot be empty", 400)
        if new != confirm:
            return apology("new password and confirm password doesn't match", 400)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new), session["user_id"])
        return redirect("/")

    else:
        return render_template("password.html")
