from flask import render_template, Flask, request, flash
import web_app
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
load_dotenv()


@app.route('/')
def get_username():
    return render_template('index.html')

@app.route('/username', methods=["POST"])
def render_map():
    web_app.main(request.form.get('username'))
    return render_template('{}.html'.format(request.form.get('username')))
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8080)