import csv
import sqlite3
import re

from formats import Set

schema = [
    '''CREATE TABLE qn_tossup 
        (id integer primary key, pset integer, author text, subject text, format text, content text, choices text, answer text);''',
    '''CREATE TABLE qn_bonus 
        (id integer primary key, pset integer, author text, subject text, format text, content text, choices text, answer text);'''
]

__db__ = 'questions.db'
__qn__ = 'questions.csv'
c = sqlite3.connect(__db__)

count = lambda : [item for item in c.execute('select count(*) from qn_tossup;')][0][0]
count_subject = lambda s : [item for item in c.execute('select count(*) from qn_tossup where subject=?;', (s,))][0][0]

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
    clear([])
    print('Reading from question file...')
    reader = csv.reader(open(__qn__))
    data = [item for item in reader][1:]
    print('Inserting into database...')
    while (count() < len(data)):
        insert(count())
        
def add(argv):
    pset = int(argv[0])
    pid = int(argv[1])
    c.execute('update qn_tossup set pset=? where id=?;', (pset, pid))
    c.execute('update qn_bonus set pset=? where id=?;', (pset, pid))

def tex(argv, number=-1):
    pid = int(argv[0])
    items = Set.std_order.items()
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
            dict['choices'] = Set.choiceformat.format(W = ch[0], X = ch[1], Y = ch[2], Z = ch[3],)
        return Set.qformat.format(
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
        return Set.pairfomat.format(
            tossup = onetex(dict_tossup, 'TOSS-UP'),
            bonus = onetex(dict_bonus, 'BONUS')
        )
    except Exception as ex:
        print(ex)

def disp(argv):
    print(tex(argv[0]))

def write(argv):
    def questions(condition):
        body = ''
        query = c.execute('select id from qn_tossup where %s;' % condition)
        results = [item[0] for item in query]
        print('%d questions found' % len(results))
        for i in results:
            body += tex([i], i)
        return body

    category = argv[0][2:]
    if category == 'all':
        for subject in Set.subjects:
            print('%s: %d' % (subject, count_subject(subject)))
        with open('all.tex','w') as texfile:
            body = questions('1=1')
            texfile.write(Set.setformat.format(
                set = "All questions",
                content = body
            ))
            return
    condition = argv[1]
    name = argv[2].strip('\"')

    
    body = questions('%s=%s' % (category, condition))
    if body == '':
        print('No questions matching %s=%s were found' % (category, condition))
    else:
        with open('%s.tex' % name.replace(' ',''), 'w') as texfile:
            texfile.write(Set.setformat.format(set=name, content=body).replace('    ', ''))
        
def rm(argv):
    return 

def clear(argv):
    print('Clearing tossup...')
    c.execute('delete from qn_tossup;')
    print('Clearing bonus...')
    c.execute('delete from qn_bonus;')

commands = {
    'add':add,
    'rm':rm,
    'tex':tex,
    'disp':disp,
    'write':write,
    'update':update,
}

def cmd(argv):
    for pattern, func in commands.items():
        if argv[0] == pattern:
            func(argv[1:])

def parse_cmd(command):
    cmdr = re.compile('(\".*?\"|([a-z\-]*))')
    match = [item[0] for item in re.findall(cmdr, command)]
    argv = list(filter(lambda token: token != '', match))
    
    return argv

while True:
    arg = input('>')
    if arg in ['quit', 'exit']:
        break
    else:
        argv = parse_cmd(arg)
        cmd(argv)