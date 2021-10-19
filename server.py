from flask import Flask
from flask import render_template, request, redirect, url_for, session
from db import randomVideo

app = Flask(__name__)
app.secret_key = b'\x82-ZoQ$\xf2\xfb\xf1-\xa0(Q~U-'

@app.route('/', methods=['GET', 'POST'])
def index():
    video = randomVideo()
    return render_template('index.html', videoID = video['videoID'], title = video['title'])

#@app.route('/likesCounter', methods=['POST'])
# def getLikes():
#     if request.form['submit_button'] == 'like':
#         if 'likes' in session:
#             session['likes'] += 1
#         else:
#             session['likes'] = 1
#     elif request.form['submit_button'] == 'dislike':
#         if 'dislikes' in session:
#             session['dislikes'] += 1
#         else:
#             session['dislikes'] = 1
#     print('likes: ', session['likes'], ' dislikes: ', session['dislikes'])
#     return '', 204

@app.route('/y', methods=['POST'])
def y():
    if request.form['isLike'] == 'yes':
        print('yes!')
    if request.form['isLike'] == 'no':
        print('no!')
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)