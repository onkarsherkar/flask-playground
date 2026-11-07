from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", page_name="Index", page_num=1)


@app.route("/home", methods=["GET"])
def home():
    return "<h1>Home</h1>"


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
