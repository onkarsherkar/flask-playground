from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_joined = db.Column(db.DateTime)

    orders = db.relationship("Order", back_populates="user")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    user_id = db.Column(db.ForeignKey("user.id"))

    user = db.relationship("User", back_populates="orders")


@app.route("/")
def index():
    return render_template("index.html", page_name="Index", page_num=1)


@app.route("/home", methods=["GET"])
def home():
    return render_template(
        "home.html",
        number=9,
        data=[{"key": "value1"}, {"key": "value2"}, {"key": "value3"}],
    )


@app.route("/json")
def json():
    return {"mykey": "Json value", "mylist": [1, 2, 3, 4, 5]}


@app.route("/dynamic", defaults={"user_input": "default"})
@app.route("/dynamic/<user_input>")
def dynamic(user_input):
    return f"<h1> User input text: {user_input}</h1>"


@app.route("/query")
def query():
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    return f"<h1>The query string contains:{first_name} {last_name}</h1>"


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        user_input = request.form["user_input"]
        print("user_input", user_input)
        return redirect(url_for("home"))
    return (
        '<form method="POST"> <input type="text" name="user_input" /> '
        '<input type="submit" /> </form>'
    )


@app.route("/acceptjson")
def acceptjson():
    json_data = request.get_json()
    api_input = json_data["mylist"]
    hello = json_data["hello"]

    return {"api_input": api_input, "hello": hello}


@app.route("/error")
def error():
    1 / 0
    return "error"


def insert_data():
    from datetime import datetime

    python_user = User(name="Python User", date_joined=datetime.now())
    flask_user = User(name="Flask User", date_joined=datetime.now())
    javascript_user = User(name="Javascript User", date_joined=datetime.now())

    db.session.add_all([python_user, flask_user, javascript_user])

    first_order = Order(total=99, user=python_user)
    second_order = Order(total=20, user=python_user)
    third_order = Order(total=35, user=flask_user)

    db.session.add_all([first_order, second_order, third_order])
    db.session.commit()


def update_first_user():
    first_user = User.query.first()
    first_user.name = "Flask Tom"
    db.session.commit()


def delete_first_user():
    first_user = User.query.first()
    db.session.delete(first_user)
    db.session.commit()
