import os

from flask import Flask, render_template, request
from dotenv import load_dotenv

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("team") or not request.form.get("name"):
        return render_template("failure.html")
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=8080)
