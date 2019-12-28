import sqlite3
import csv

class questioncsv():
	qfile: str

	def __init__(self, file):
		qfile = file

	def read(self, qid: int):
		with open(self.qfile, 'r') as csvfile:
			reader = csv.reader(csvfile)
			qlist = reader[qid]
		qdict = {
			'qid':qid,
			'round':0,
			'subject':qlist[3],
			'tuformat':qlist[4],
			'tucontent':qlist[5],
			'bnformat':qlist[12],
			'bncontent':qlist[13],
			'author':qlist[2],
			'difficulty':int(qlist[20])
		}
		if qdict['tuformat'] == 'Multiple Choice':
			qdict['tucontent'] = '///'.join(qlist[7:12])
		else:
			qdict['tucontent'] = qlist[6]

		if qdict['bnformat'] == 'Multiple Choice':
			qdict['bncontent'] = '///'.join(qlist[15:20])
		else:
			qdict['bncontent'] = qlist[14]

class questiondb():
	dbfile:str

	dborder = {
		'qid':lambda s: int(s),
		'round':lambda s: int(s),
		'subject':lambda s: s,
		'tuformat':lambda s: s,
		'tucontent':lambda s: s,
		'tuanswer':lambda s: s,
		'bnformat':lambda s: s,
		'bncontent':lambda s: s,
		'bnanswer':lambda s: s,
		'author':lambda s: s,
		'difficulty':lambda s:int(s)
	}

	schema = '''CREATE TABLE IF NOT EXISTS questions (qid integer primary key, round integer,
	subject text,
	tuformat text, tucontent text, tuanswer text,
	bnformat text, bncontent text, bnanswer text,
	author text, diff integer);'''

	def __init__(self, file: str):
		self.dbfile = file
		db = sqlite3.connect(self.dbfile)
		db.execute(schema)
		db.commit()
		db.close()

	def store(self, question: dict):
		return

	def read(self, columns, condition: str =''):
		return

	def count(self, condition: str =''):
		db = sqlite3.connect(self.dbfile)
		return read('count(*)')[0][0]



