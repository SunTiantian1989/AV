# 初始化数据库
import sqlite3


def initial_database():
    conn = sqlite3.connect('AV.db')
    print("Opened database successfully")
    cursor = conn.cursor()
    cursor.execute('''create table videos (
    id  INTEGER PRIMARY KEY autoincrement,
    number TEXT NOT NULL,
    title TEXT DEFAULT NULL,
    date TEXT DEFAULT NULL,
    length INTEGER DEFAULT NULL,
    director TEXT DEFAULT NULL,
    maker TEXT DEFAULT NULL,
    label TEXT DEFAULT NULL,
    review_point INTEGER DEFAULT NULL,
    codec_tag TEXT DEFAULT NULL,
    height TEXT DEFAULT NULL,
    width TEXT DEFAULT NULL,
    bit_rate TEXT DEFAULT NULL,
    size TEXT DEFAULT NULL)''')
    cursor.execute('create table casts (id  INTEGER PRIMARY KEY autoincrement,cast_name TEXT NOT NULL UNIQUE )')
#    cursor.execute('create table director (id  INTEGER PRIMARY KEY autoincrement,director_name TEXT NOT NULL UNIQUE )')
#    cursor.execute('create table maker (id  INTEGER PRIMARY KEY autoincrement,maker_name TEXT NOT NULL UNIQUE )')
#    cursor.execute('create table label (id  INTEGER PRIMARY KEY autoincrement,label_name TEXT NOT NULL UNIQUE )')
    cursor.execute('create table genres (id  INTEGER PRIMARY KEY autoincrement,genre_name TEXT NOT NULL UNIQUE )')
    cursor.execute('''create table casts_in_videos (
    id  INTEGER PRIMARY KEY autoincrement,
    video_number TEXT NOT NULL,
    cast_name TEXT NOT NULL)''')
    cursor.execute('''create table genres_in_videos (
    id  INTEGER PRIMARY KEY autoincrement,
    video_number TEXT NOT NULL,
    genre_name  TEXT NOT NULL)''')
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initial_database()




