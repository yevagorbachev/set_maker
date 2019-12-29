import sqlite3
import csv

class questioncsv():
	qfile: str

	def __init__(self, file):
		self.qfile = file

	def read(self):
		with open(self.qfile, 'r') as csvfile:
			reader = csv.reader(csvfile)
			qlist = [item for item in reader][1:]
		for index, question in enumerate(qlist):
			qdict = {
				'qid':index + 1,
				'round':0,
				'subject':question[3],
				'tuformat':question[4],
				'tucontent':question[5],
				'bnformat':question[12],
				'bncontent':question[13],
				'author':question[2],
				'difficulty':int(question[20])
			}
			if qdict['tuformat'] == 'Multiple Choice':
				qdict['tuanswer'] = '///'.join(question[7:12])
				# Stores MC choices as Choice W///Choice X///Choice Y///Choice Z///Correct choice letter
				# permits the use of the same "tuanswer" column for MC and SA questions
			else:
				qdict['tuanswer'] = question[6]

			if qdict['bnformat'] == 'Multiple Choice':
				qdict['bnanswer'] = '///'.join(question[15:20])
			else:
				qdict['bnanswer'] = question[14]
			qlist[index] = qdict.copy()
		return qlist

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

	schema = '''create table questions (qid integer primary key, 
	round integer, subject text,
	tuformat text, tucontent text, tuanswer text,
	bnformat text, bncontent text, bnanswer text,
	author text, difficulty integer);'''

	def __init__(self, file: str):
		"""Initializes database with given filename and schema specified in class constant"""
		self.dbfile = file
		db = sqlite3.connect(self.dbfile)
		try:
			db.execute('drop table questions;')
		db.execute(self.schema)
		db.commit()

	def write(self, question: dict):
		"""Inserts an item into a database using a dictionary, with keys as columns"""
		keys = question.keys()
		values = question.values()
		cmd = 'insert into questions (%s) values (%s);' % (','.join(keys), ','.join(['?' for item in values]))

		db = sqlite3.connect(self.dbfile)
		try:
			db.execute(cmd, tuple(values))
		except sqlite3.Error as dberr:
			print('Insertion failed: %s' % dberr)
		db.commit()

	def read(self, columns, condition: str =''):
		"""Selects specified columns from a database, under optional conditions"""
		return

	def count(self, condition: str =''):
		"""Returns a count of the number of questions satisfying the optional conditions"""
		db = sqlite3.connect(self.dbfile)
		return read('count(*)')[0][0]


csvf = questioncsv('questions.csv')
questions = csvf.read()
db = questiondb('questions.db')
db.write(questions[0])