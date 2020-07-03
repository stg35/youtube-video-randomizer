from flask import Flask
from flask import render_template, request, redirect, url_for
from db import randomVideo

app = Flask(__name__)
app.config["SECRET_KEY"] = b'\x82-ZoQ$\xf2\xfb\xf1-\xa0(Q~U-'

@app.route('/')
def index():
    video = randomVideo()
    return render_template('index.html', videoID = video['videoID'], title = video['title'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)