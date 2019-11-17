import csv
import sqlite3
import re

# commands = {
#     r'add [0-9] [0-9][0-9]*':add,
#     r'rm [0-9] [0-9][0-9]*':rm,
#     r'tex [0-9]':tex,
#     r'disp [0-9]':disp,
#     r'update':update,
# }

__qformat__ = '''
\\begin{center}
    \\textbf{{{TYPE}}} \\\\ By: {author}
\\end{center}
{num}) {SUBJECT} \\textit{{{form}}} {question}
\\\\{choices}
\\\\ANSWER: {answer}
'''

__choiceformat__ = '''
W) {W}
\\\\X) {X}
\\\\Y) {Y}
\\\\Z) {Z}
'''
__db__ = 'questions.db'
__qn__ = 'questions.csv'
c = sqlite3.connect(__db__)

count = lambda : [item for item in c.execute('select count(*) from qn_tossup;')][0][0]

def insert(pid):
    qnum = count()
    if (pid + 1 == qnum):
        return
    reader = csv.reader(open(__qn__))
    data = [item for item in reader][pid + 1]

    author, subject = data[2], data[3]
    thead = 4
    bhead = 13

    tform = data[thead]
    if tform == 'Multiple-choice':
        tcontent = data[thead + 1]
        tchoices = '///'.join(data[thead+2:thead+6])
        letter = data[thead + 6]
        content = data[thead + ord(data[thead + 6]) - ord('V')]
        tanswer = f'{letter}) {content}'
    elif tform == 'Short-answer':
        tcontent = data[thead + 7]
        tchoices = ''
        tanswer = data[thead + 8]
    
    bform = data[bhead]
    if bform == 'Multiple-choice':
        bcontent = data[bhead + 1]
        bchoices = '///'.join(data[bhead+2:bhead+6])
        letter = data[bhead + 6]
        content = data[bhead + ord(data[bhead + 6]) - ord('V')]
        banswer = f'{letter}) {content}'
    elif bform == 'Short-answer':
        bcontent = data[bhead + 7]
        bchoices = ''
        banswer = data[bhead + 8]
    

    c.execute('insert into qn_tossup values (?,?,?,?,?,?,?,?);', (qnum, 0, author, subject, tform, tcontent, tchoices, tanswer))
    c.execute('insert into qn_bonus values (?,?,?,?,?,?,?,?);', (qnum, 0, author, subject, bform, bcontent, bchoices, banswer))
    c.commit()
    c.close()

def update():
    reader = csv.reader(open(__qn__))
    data = [item for item in reader][1:]
    while (count() < len(data))
        insert(count())

# def cmd(arg: str):
#     for pattern, func in commands:
#         if re.search(pattern, arg):

        
# def add(set, pid)
#     return

# def tex(pid):
#     return

def disp(pid):
    return

# while True:
#     arg = input('>')
#     if arg == 'quit':
#         break
#     else:
#         print(cmd(arg).span())