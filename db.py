import MySQLdb
from MySQLdb import escape_string

def connection():
	conn = MySQLdb.connect(host="classmysql.engr.oregonstate.edu",
			user="cs340_fisherj2",
			password="2260",
			database="cs340_fisherj2"
		)

	c = conn.cursor()

	return c, conn

def check_for_user(username, email):
	c, conn = connection()

	ret = c.execute("SELECT * FROM user WHERE username = '{}'".format(username))

	if int(ret) > 0:
		c.close()
		conn.close()
		return True

	ret = c.execute("SELECT * FROM user WHERE email = '{}'".format(email))

	if int(ret) > 0:
		c.close()
		conn.close()
		return True

	c.close()
	conn.close()

	return False

def try_signon(email, password):
	c, conn = connection()

	ret = c.execute("SELECT * FROM user Where email = '{}' AND password = '{}'".format(email, password))

	signon = False

	if int(ret) > 0:
		signon = True

	c.close()
	conn.close()

	return signon

def get_username(email):
	c, conn = connection()
	c.execute("SELECT (username) FROM user Where email = '{}'".format(email))

	ret = c.fetchall()

	c.close()
	conn.close()

	return ret[0][0]

def get_user_id(username):
	c, conn = connection()

	c.execute("SELECT (id) FROM user WHERE username = '{}'".format(username))

	ident = c.fetchall()[0][0]

	c.close()
	conn.close()

	return ident

def create_artist(artist, username):
	c, conn = connection()

	artists = c.execute("SELECT (id) FROM artist WHERE name = '{}'".format(artist))

	ident = None

	if artists != 0:
		ident =  c.fetchall()[0][0]

	else:
		c.execute("INSERT INTO artist (name) VALUES ('{}')".format(artist))

		conn.commit()

		c.execute("SELECT (id) FROM artist WHERE name = '{}'".format(artist))

		ident = c.fetchall()[0][0]

	user_id = get_user_id(username)

	relations = c.execute("SELECT * FROM user_artist WHERE user_id = '{}' AND artist_id = '{}'".format(user_id, ident))

	if relations == 0:
		c.execute("INSERT INTO user_artist (user_id, artist_id) VALUES ('{}', '{}')".format(user_id, ident))
		conn.commit()

	c.close()
	conn.close()

	return ident

def create_composer(composer, username):
	c, conn = connection()

	artists = c.execute("SELECT (id) FROM composer WHERE name = '{}'".format(composer))

	ident = None

	if artists != 0:
		ident =  c.fetchall()[0][0]

	else:
		c.execute("INSERT INTO composer (name) VALUES ('{}')".format(composer))

		conn.commit()

		c.execute("SELECT (id) FROM composer WHERE name = '{}'".format(composer))

		ident = c.fetchall()[0][0]

	user_id = get_user_id(username)

	relations = c.execute("SELECT * FROM user_composer WHERE user_id = '{}' AND composer_id = '{}'".format(user_id, ident))

	if relations == 0:
		c.execute("INSERT INTO user_composer (user_id, composer_id) VALUES ('{}', '{}')".format(get_user_id(username), ident))
		conn.commit()

	c.close()
	conn.close()

	return ident

def create_album(username, artist, album):
	c, conn = connection()

	artist_id = create_artist(artist, username)

	albums = c.execute("SELECT (id) FROM album WHERE name = '{}'".format(album))

	if albums != 0:
		album_id = c.fetchall()[0][0]
		relations = c.execute("SELECT * FROM user_album WHERE user_id = '{}' AND album_id = '{}'".format(get_user_id(username), album_id))
	
		if relations == 0:
			c.execute("INSERT INTO user_album (user_id, album_id) VALUES ('{}', '{}')".format(get_user_id(username), album_id))
			conn.commit()
	else:
		c.execute("INSERT INTO album (name) VALUES ('{}')".format(album))
		conn.commit()

		c.execute("SELECT (id) FROM album WHERE name = '{}'".format(album))
		album_id = c.fetchall()[0][0]
		
		c.execute("INSERT INTO artist_album (artist_id, album_id) VALUES ('{}', '{}')".format(artist_id, album_id))
		conn.commit()
		
		c.execute("INSERT INTO user_album (user_id, album_id) VALUES ('{}', '{}')".format(get_user_id(username), album_id))
		conn.commit()
		
		
	return album_id

def create_song(username, artist, song, album, composer=None):
	c, conn = connection()

	artist_id = create_artist(artist, username)
	
	album_id = create_album(username, artist, album)

	if composer == None or composer == "":
		composer_id = None
	else:
		composer_id = create_composer(composer, username)

	c.execute("INSERT INTO song (name, album_id) VALUES ('{}', '{}')".format(song, album_id))
	conn.commit()

	c.execute("SELECT (id) FROM song WHERE name = '{}' AND album_id = '{}'".format(song, album_id))
	song_id = c.fetchall()[0][0]

	c.execute("INSERT INTO artist_song (artist_id, song_id) VALUES ('{}', '{}')".format(artist_id, song_id))
	conn.commit()

	if composer_id != None:
		c.execute("INSERT INTO composer_song (composer_id, song_id) VALUES ('{}', '{}')".format(composer_id, song_id))
		conn.commit()

	c.execute("INSERT INTO user_song (user_id, song_id) VALUES ('{}', '{}')".format(get_user_id(username), song_id))
	conn.commit()

	return song_id

def create_user(username, password, email):
	c, conn = connection()

	c.execute("INSERT INTO user (`username`, `password`, `email`) VALUES ('{}', '{}', '{}')".format(username, password, email))

	conn.commit()
	c.close()
	conn.close()

