import csv
import sqlite3
import re

commands = {
    r'add [0-9] [0-9][0-9]*':add,
    r'rm [0-9] [0-9][0-9]*':rm,
    r'tex [0-9]':tex,
    r'disp [0-9]':disp,
}

__db__ = 'questions.db'
c = sqlite3.connect(__db__)

def cmd(arg):
    for pattern, func in commands:

        
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