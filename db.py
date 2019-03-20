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
        ident = c.fetchall()[0][0]

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
        ident = c.fetchall()[0][0]

    else:
        c.execute("INSERT INTO composer (name) VALUES ('{}')".format(composer))

        conn.commit()

        c.execute("SELECT (id) FROM composer WHERE name = '{}'".format(composer))

        ident = c.fetchall()[0][0]

    user_id = get_user_id(username)

    relations = c.execute(
        "SELECT * FROM user_composer WHERE user_id = '{}' AND composer_id = '{}'".format(user_id, ident))

    if relations == 0:
        c.execute(
            "INSERT INTO user_composer (user_id, composer_id) VALUES ('{}', '{}')".format(get_user_id(username), ident))
        conn.commit()

    c.close()
    conn.close()

    return ident


def create_album(username, artist, album):
    c, conn = connection()

    artist_id = create_artist(artist, username)
    albums = c.execute("SELECT (id) FROM album WHERE name = '{}'".format(album))
    print(album)
    print(albums)

    if albums != 0:
        album_id = c.fetchall()[0][0]
        relations = c.execute(
            "SELECT * FROM user_album WHERE user_id = '{}' AND album_id = '{}'".format(get_user_id(username), album_id))

        if relations == 0:
            c.execute("INSERT INTO user_album (user_id, album_id) VALUES ('{}', '{}')".format(get_user_id(username),
                                                                                              album_id))
            conn.commit()
    else:
        c.execute("INSERT INTO album (name) VALUES ('{}')".format(album))
        conn.commit()

        c.execute("SELECT (id) FROM album WHERE name = '{}'".format(album))
        album_id = c.fetchall()[0][0]

        c.execute("INSERT INTO artist_album (artist_id, album_id) VALUES ('{}', '{}')".format(artist_id, album_id))
        conn.commit()

        c.execute(
            "INSERT INTO user_album (user_id, album_id) VALUES ('{}', '{}')".format(get_user_id(username), album_id))
        conn.commit()

    return album_id


def create_song(username, artist, song, album, composer):
    c, conn = connection()

    artist_id = create_artist(artist, username)

    album_id = create_album(username, artist, album)
    print(composer)
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

    if composer_id is not None:
        c.execute("INSERT INTO composer_song (composer_id, song_id) VALUES ('{}', '{}')".format(composer_id, song_id))
        conn.commit()

    c.execute("INSERT INTO user_song (user_id, song_id) VALUES ('{}', '{}')".format(get_user_id(username), song_id))
    conn.commit()

    return song_id


def create_user(username, password, email):
    c, conn = connection()

    c.execute("INSERT INTO user (`username`, `password`, `email`) VALUES ('{}', '{}', '{}')".format(username, password,
                                                                                                    email))

    conn.commit()
    c.close()
    conn.close()


def display_artist(artistName, username):
    userId = get_user_id(username)
    c, conn = connection()

    c.execute(
        "SELECT album.name, album.release_date, album.url, a.name "
        "FROM album "
        "JOIN artist_album aa on album.id = aa.album_id "
        "JOIN artist a on aa.artist_id = a.id "
        "JOIN user_artist ua on a.id = ua.artist_id "
        "WHERE a.name = '{}'".format(artistName))
    album_data = c.fetchall()

    c.execute(
        "SELECT DISTINCT song.name, album.name, song.release_date, song.genre, song.url "
        "FROM song JOIN artist_song sa on song.id = sa.song_id "
        "JOIN artist a on sa.artist_id = a.id "
        "JOIN user_artist ua on a.id = ua.artist_id "
        "JOIN album on album.id = song.album_id "
        "WHERE a.name = '{}'".format(artistName))
    song_data = c.fetchall()
    print(song_data)

    c.execute(
        "SELECT composer.name "
        "FROM song JOIN artist_song sa on song.id = sa.song_id "
        "JOIN artist a on sa.artist_id = a.id "
        "JOIN user_artist ua on a.id = ua.artist_id "
        "JOIN album on album.id = song.album_id "
        "JOIN composer_song cs on cs.song_id = song.id "
        "JOIN composer on cs.composer_id = composer.id "
        "WHERE a.name = '{}'".format(artistName))

    composer_data = c.fetchall()

    if len(composer_data) > 0:
        composer_data = composer_data[0][0]
    else:
        composer_data = 'None'

    c.close()
    conn.close()
    return album_data, song_data, composer_data


def display_song(songName, username):
    userId = get_user_id(username)
    c, conn = connection()
    c.execute(
        "SELECT DISTINCT a.name, album.name, song.release_date, song.genre, song.url "
        "FROM song JOIN artist_song sa on song.id = sa.song_id "
        "JOIN artist a on sa.artist_id = a.id "
        "JOIN user_artist ua on a.id = ua.artist_id "
        "JOIN album on album.id = song.album_id "
        "WHERE user_id = '{}' AND song.name = '{}'".format(userId, songName))
    song_data = c.fetchall()
    print(song_data)
    c.execute(
        "SELECT composer.name from composer join composer_song cs on composer.id = cs.composer_id "
        "JOIN song on song.id = cs.song_id WHERE song.name = '{}'".format(songName)
    )
    composer_data = c.fetchall()
    if len(composer_data) > 0:
        composer_data = composer_data[0][0]
    else:
        composer_data = 'None'
    c.close()
    conn.close()
    return song_data, composer_data


def display_album(albumName, username):
    userId = get_user_id(username)
    c, conn = connection()
    c.execute(
        "SELECT DISTINCT song.name, composer.name, song.release_date, song.genre, song.url, a.name "
        "FROM song JOIN artist_song sa ON song.id = sa.song_id "
        "JOIN artist a ON sa.artist_id = a.id "
        "JOIN user_artist ua ON a.id = ua.artist_id "
        "JOIN album ON album.id = song.album_id "
        "JOIN composer_song cs ON cs.song_id = song.id "
        "JOIN composer ON cs.composer_id = composer.id "
        "WHERE album.name = '{}'".format(albumName))

    album_data = c.fetchall()
    print(album_data)
    c.execute(
        "SELECT artist.name "
        "FROM artist JOIN artist_album aa ON artist.id = aa.artist_id "
        "JOIN album ON album.id = aa.album_id "
        "WHERE album.name = '{}'".format(albumName)
    )
    artist_name = c.fetchall()
    print('artist name: ')
    print(artist_name)
    if len(artist_name) > 0:
        artist_name = artist_name[0][0]

    print(artist_name)
    c.close()
    conn.close()
    return album_data, artist_name


# *****************************************************************************
# song update
# *****************************************************************************


def song_update(username, song_name, u_release, u_url, u_genre):
    print("albumName")
    userId = get_user_id(username)
    c, conn = connection()
    c.execute(
        "UPDATE song "
        "SET release_date = '{}'"
        "WHERE name = '{}'".format(u_release, song_name)
    )
    conn.commit()
    c.execute(
        "UPDATE song "
        "SET url = '{}'"
        "WHERE name = '{}'".format(u_url, song_name)
    )
    conn.commit()

    c.execute(
        "UPDATE song "
        "SET genre = '{}'"
        "WHERE name = '{}'".format(u_genre, song_name)
    )
    conn.commit()

    c.close()
    conn.close()


def update_album(userName, artistName, albumName, songName, composerName, release, genre, link):
    c, conn = connection()
    album_id = c.execute("SELECT (id) FROM album WHERE name = '{}'".format(albumName))
    artist_id = c.execute("SELECT (id) FROM artist WHERE name = '{}'".format(artistName))

    if composerName == None or composerName == "":
        composer_id = None
    else:
        composer_id = c.execute("SELECT (id) FROM composer WHERE name = '{}'".format(composerName))

    print("Composer Id is {}".format(composer_id))
    # Insert song into
    c.execute("INSERT INTO song (name, album_id, release_date, genre, url) "
              "VALUES ('{}', '{}', '{}', '{}', '{}')".format(songName, album_id, release, genre, link))
    conn.commit()

    c.execute("SELECT (id) FROM song WHERE name = '{}' AND album_id = '{}'".format(songName, album_id))
    song_id = c.fetchall()[0][0]

    c.execute(
        "INSERT INTO artist_song (artist_id, song_id) "
        "VALUES ((SELECT artist.id FROM artist "
        "WHERE artist.name = '{}' LIMIT 1),"
        "(SELECT song.id FROM song WHERE song.name = '{}' LIMIT 1))".format(artistName, songName))

    conn.commit()

    if composer_id is not None:
        c.execute(
            "INSERT INTO composer_song (composer_id, song_id) VALUES ((SELECT composer.id FROM composer WHERE composer.name = '{}' LIMIT 1), (SELECT song.id FROM song WHERE song.name = '{}' LIMIT 1))".format(
                composerName, songName))
        conn.commit()

    c.execute("INSERT INTO user_song (user_id, song_id) VALUES ('{}', '{}')".format(get_user_id(userName), song_id))

    conn.commit()
    album_data = c.fetchall()
    c.close()
    conn.close()

    return album_data


def get_internal_data(table):
    c, conn = connection()
    c.execute(
        "SELECT name, id "
        "FROM {}".format(table))

    artist_data = c.fetchall()
    c.close()
    conn.close()
    return artist_data


def get_data():
    data = {}

    data["artists"] = get_internal_data("artist")
    data["composers"] = get_internal_data("composer")
    data["songs"] = get_internal_data("song")
    data["albums"] = get_internal_data("album")

    return data


def connect_data(table, data_id, username):
    userId = get_user_id(username)
    c, conn = connection()

    c.execute("INSERT INTO user_{} (user_id, {}_id) "
              "VALUES ('{}','{}')".format(table, table, userId, data_id))

    conn.commit()


def display_composer(composerName, username):
    userId = get_user_id(username)
    c, conn = connection()
    c.execute(
        "SELECT DISTINCT song.name, a.name, song.release_date, song.genre, song.url "
        "FROM song JOIN artist_song sa on song.id = sa.song_id "
        "JOIN artist a on sa.artist_id = a.id "
        "JOIN user_artist ua on a.id = ua.artist_id "
        "JOIN album on album.id = song.album_id "
        "JOIN composer_song cs on cs.song_id = song.id "
        "JOIN composer on cs.composer_id = composer.id "
        "WHERE user_id = '{}' AND composer.name = '{}'".format(userId, composerName))
    composer_data = c.fetchall()
    c.close()
    conn.close()
    return composer_data


def get_music_id(table, name):
    c, conn = connection()
    c.execute("SELECT id FROM {} WHERE name LIKE '%{}%'".format(table, name))
    data_id = c.fetchall()[0][0]
    c.close()
    conn.close()
    return data_id


def delete(username, table, value):
    userId = get_user_id(username)
    c, conn = connection()
    c.execute("DELETE FROM user_{} WHERE user_id = '{}' AND {}_id = '{}'".format(table, userId, table,
                                                                                 get_music_id(table, value)))

    conn.commit()
    c.close()
    conn.close
