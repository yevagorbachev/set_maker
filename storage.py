import sqlite3

class questiondb():
    dborder = {
        'qid':lambda s:int(s),
        'round':lambda s:int(s),
        'subject':lambda s:s,
        'tuformat':lambda s:s,
        'tucontent':lambda s:s,
        'tuanswer':lambda s:s,
        'bnformat':lambda s:s,
        'bncontent':lambda s:s,
        'bnanswer':lambda s:s,
        'author':lambda s:s,
        'difficulty':lambda s:int(s)
    }
    schema = '''CREATE TABLE questions (qid integer primary key, round integer,
    subject text,
    tuformat text, tucontent text, tuanswer text,
    bnformat text, bncontent text, bnanswer text,
    author text, diff integer);'''
