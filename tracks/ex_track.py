import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
curs = conn.cursor()
ZERO = '0'

curs.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;                   

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
                   
CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);            

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

ofile = open('tracks.csv')
# fhand = ET.fromstring(ofile)
# tracks = fhand.findall('dict/dict/dict')
# print('Dict Count', len(ofile))

def lookup(track, key):
    found = False
    for element in track:
        if found is True: 
            return element.text
        if element.tag == 'key' and element.text == key:
            found = True
    return None

for track in ofile:
    # print(track)
    line = track.rstrip()
    spl = line.split(',')
    artist = spl[1]
    genre = spl[len(spl) - 1]
    album = spl[2]
    trackName = spl[0]

    if artist == ZERO or genre == ZERO or album == ZERO:
        continue

    # print('Artist',artist,': Genre', genre,': Album', album,': Track Name', trackName)
    print('---', trackName, '---')
    curs.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
    curs.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artistId = curs.fetchone()[0]
    print(artist, artistId)
        
    print(album)
    curs.execute('INSERT OR IGNORE INTO Album (artist_id, title) VALUES (?,?)', (artistId,album,))
    curs.execute('SELECT id FROM Album WHERE artist_id = ? AND title = ?', (artistId, album,))
    albumId = curs.fetchone()[0]
    print(album,albumId)
        
    curs.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
    curs.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genreId = curs.fetchone()[0]
    print(genre,genreId)

    curs.execute('INSERT OR IGNORE INTO Track (title, album_id, genre_id) VALUES (?,?,?)', (trackName,albumId,genreId,))
    conn.commit()

curs.close()