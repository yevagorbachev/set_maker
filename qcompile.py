import csv
import sqlite3
import re

commands = {
    r'add [0-9] [0-9][0-9]*':add,
    r'rm [0-9] [0-9][0-9]*':rm,
    r'tex [0-9]':tex,
    r'disp [0-9]':disp,
}

qformat = '''
\\begin{center}
    \\textbf{{{TYPE}}} \\\\ By: {author}
\\end{center}
{num}) {SUBJECT} \\textit{{{form}}} {question}
\\\\{choices}
\\\\ANSWER: {answer}
'''

choiceformat = '''
W) {W}
\\\\X) {X}
\\\\Y) {Y}
\\\\Z) {Z}
'''
__db__ = 'questions.db'
c = sqlite3.connect(__db__)

def cmd(arg: str):
    for pattern, func in commands:
        if re.search(pattern, arg):

        
def add()

def tex(n):
    return

def disp(n):
    return

while True:
    arg = input('>')
    if arg == 'quit':
        break
    else:
        print(cmd(arg).span())