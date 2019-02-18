import MySQLdb

def connection():
	conn = MySQLdb.connect(host="classmysql.engr.oregonstate.edu",
			user="cs340_fisherj2",
			password="2260",
			database="cs340_fisherj2"
		)

	c = conn.cursor()

	return c, conn
