from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask_session import Session

from factory import create_app
import db

app = create_app()
app.config.from_object(__name__)
Session(app)

@app.route('/')
def homepage():
    return render_template('base.html')

@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	try:
		session["loggedIn"]
	except:
		if db.try_signon(request.form["email"], request.form["password"]):
			session["loggedIn"] = True
			session["username"] = db.get_username(request.form["email"])

			return render_template('loggedIn.html', username=session["username"])

		else:
			return render_template('badLogin.html')
	else:
		return render_template('base.html')


@app.route('/find-artist', methods=["POST"])
def findArtist():
	try:
		session["loggedIn"]
	except:
		return render_template('login.html')
	else:
		artist_list, song_list = db.display_artist(request.form["artist"], session["username"])

		return render_template('display_by_artist.html', album_data=artist_list, song_data=song_list,
							   artist=request.form["artist"])


@app.route('/new-artist', methods=["POST"])
def newArtist():
	try:
		session["loggedIn"]
	except:
		return render_template('login.html')
	else:
		db.create_artist(request.form["artist"], session["username"])

		return render_template('dataAdded.html', data=request.form["artist"])

@app.route('/new-composer', methods=["POST"])
def newComposer():
	try:
		session["loggedIn"]
	except:
		return render_template('login.html')
	else:
		db.create_composer(request.form["composer"], session["username"])

		return render_template('dataAdded.html', data=request.form["composer"])

@app.route('/new-album', methods=["post"])
def newAlbum():
	try:
		session["loggedIn"]
	except:
		return render_template('login.html')
	else:
		db.create_album(session["username"], request.form["artist"], request.form["album"])
		return render_template('dataAdded.html', data=request.form["album"]);

@app.route('/new-song', methods=["post"])
def newSong():
	try:
		session["loggedIn"]
	except:
		return render_template('login.html')
	else:
		db.create_song(session["username"], request.form["artist"], request.form["song"], request.form["album"], request.form["composer"])

		return render_template('dataAdded.html', data=request.form["song"])

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/display_data')
def display_data():
    return render_template('displayData.html')

@app.route('/new-user', methods=["POST"])
def new_user():
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']

	if db.check_for_user(username, email):
		return render_template('userExists.html')

	if len(password) <= 20:
		db.create_user(username, password, email)
		
		session['username'] = username
		session['loggedIn'] = True

		return render_template('newUser.html', username = username)
	else:
		return render_template('invalidPassword.html')
	
@app.route('/db-test/', methods=["GET","POST"])
def dbTest():
	try:
		c, conn = connection()
		return "good"
	except Exception as e:
		return(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=56565)
