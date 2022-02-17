from flask import Flask, redirect, render_template, request

# Configure app
app = Flask(__name__)

# Registrants
teams = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registrants")
def registrants():
    return render_template("registrants.html", teams=teams)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    team = request.form.get("team")
    if not name or not team:
        return render_template("failure.html")
    teams.append("{} в команді {}".format(name, team))
    return redirect("/registrants")


if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=8080)
