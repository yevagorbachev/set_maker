import csv
import sqlite3
import re



std_order = {
    'id':lambda n:int(n),
    'pset':lambda n:int(n),
    'author':lambda s:s,
    'subject':lambda s:s,
    'format':lambda s:s,
    'content':lambda s:s,
    'choices':lambda s:s,
    'answer':lambda s:s
}

subjects = [
    'Mathematics',
    'Physics',
    'Chemistry',
    'Biology',
    'Earth and Space Science',
    'Computer Science',
    'General Science'
]

__qformat__ = '''\\begin{{center}}
    \\textbf{{{TYPE}}} \\\\ By: {author}
\\end{{center}}
{num}) {SUBJECT} \\textit{{{form}}} {question}{choices}
\\\\\\\\ANSWER: {answer}
\\\\'''

__choiceformat__ = '''\\\\
\\\\W) {W}
\\\\X) {X}
\\\\Y) {Y}
\\\\Z) {Z}'''

__pairformat__ = '''
\\begin{{minipage}}{{\\textwidth}}
{tossup}
{bonus}
\\underline{{\\hspace{{6.5in}}}}
\\\\
\\end{{minipage}}
'''

__db__ = 'questions.db'
__qn__ = 'questions.csv'
c = sqlite3.connect(__db__)

count = lambda : [item for item in c.execute('select count(*) from qn_tossup;')][0][0]
count_subject = lambda s : [item for item in c.execute('select count(*) from qn_tossup where subject=?;', s)][0][0]

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
        content = data[thead + ord(data[thead + 6]) - ord('U')]
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
        content = data[bhead + ord(data[bhead + 6]) - ord('U')]
        banswer = f'{letter}) {content}'
        
    elif bform == 'Short-answer':
        bcontent = data[bhead + 7]
        bchoices = ''
        banswer = data[bhead + 8]
    

    c.execute('insert into qn_tossup values (?,?,?,?,?,?,?,?);', (qnum, 0, author, subject, tform, tcontent, tchoices, tanswer))
    c.execute('insert into qn_bonus values (?,?,?,?,?,?,?,?);', (qnum, 0, author, subject, bform, bcontent, bchoices, banswer))
    c.commit()
    

def update(argv):
    reader = csv.reader(open(__qn__))
    data = [item for item in reader][1:]
    while (count() < len(data)):
        insert(count())
        
def add(argv):
    pset = int(argv[0])
    pid = int(argv[1])
    c.execute('update qn_tossup set pset=? where id=?;', (pset, pid))
    c.execute('update qn_bonus set pset=? where id=?;', (pset, pid))

def tex(argv, number=-1):
    pid = int(argv[0])
    items = std_order.items()
    cols = ', '.join([item[0] for item in items])
    
    reducts = [item[1] for item in items]

    def select(table):
        query = c.execute('select %s from %s where id=?' % (cols, table), (pid,))
        result = [item for item in query]
        if result:
            result = list(result[0])
        else:
            raise Exception('question dne')
        for i, value in enumerate(result):
            result[i] = reducts[i](value)
        return dict(zip([item[0] for item in items], result))
    
    def onetex(dict, qtype):
        if dict['choices']:
            dict['choices'] = dict['choices'].split('///')
            ch = dict['choices']
            dict['choices'] = __choiceformat__.format(W = ch[0], X = ch[1], Y = ch[2], Z = ch[3],)
        return __qformat__.format(
            TYPE = qtype,
            author = dict['author'],
            num = number,
            SUBJECT = dict['subject'].upper(),
            form = dict['format'],
            question = dict['content'],
            choices = dict['choices'],
            answer = dict['answer']

        )
    
    try:
        dict_tossup = select('qn_tossup')
        dict_bonus = select('qn_bonus')
        return __pairformat__.format(
            tossup = onetex(dict_tossup, 'TOSS-UP'),
            bonus = onetex(dict_bonus, 'BONUS')
        )
    except Exception as ex:
        print(ex)
        

    
def disp(argv):
    print(tex(argv[0]))

def write_all(argv):
    with open('all.tex','w') as texfile:
        for i in range(count()):
            # print(tex([i]))
            texfile.write(tex([i], i + 1))

def rm(argv):
    return 

def clear(argv):
    c.execute('delete from qn_tossup;')
    c.execute('delete from qn_bonus;')

commands = {
    'add':add,
    'rm':rm,
    'tex':tex,
    'disp':disp,
    'write':write_all,
    'update':update,
    'cleardb':clear
}

def cmd(argv):
    for pattern, func in commands.items():
        if argv[0] == pattern:
            func(argv[1:])


while True:
    arg = input('>')
    if arg in ['quit', 'exit']:
        break
    else:
        argv = arg.split(' ')
        cmd(argv)