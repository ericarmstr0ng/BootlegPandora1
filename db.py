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

def create_user(username, password, email):
	c, conn = connection()

	c.execute("INSERT INTO user (`username`, `password`, `email`) VALUES ('{}', '{}', '{}')".format(username, password, email))

	conn.commit()
	c.close()
	conn.close()

