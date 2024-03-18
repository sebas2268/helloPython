import json
import sqlite3

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

##sebas
##sebas dev_task1_1

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);
                  
CREATE TABLE Course (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE
);
                  
CREATE TABLE Member (
    id INTEGER PRIMARY KEY,
    role INTEGER,
    user_id INTEGER,
    course_id INTEGER
);
''')

fhand = open('roster_data.json').read()
js = json.loads(fhand)

for elemnt in js:
    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)',(elemnt[0],))
    cur.execute('SELECT id FROM User WHERE name = ?',(elemnt[0],))
    userId = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)',(elemnt[1],))
    cur.execute('SELECT id FROM Course WHERE title = ?',(elemnt[1],))
    courseId = cur.fetchone()[0]
    cur.execute('INSERT INTO Member (role, user_id, course_id) VALUES (?,?,?)',(elemnt[2],userId,courseId,))
    conn.commit()

cur.close()