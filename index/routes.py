from index import app
from flask import render_template

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template(
        'home.html',
        app_title='Dashboard'
    )
