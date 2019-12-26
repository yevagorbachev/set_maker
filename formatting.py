class scibowlset():
    subjects = [
        'Mathematics',
        'Physics',
        'Chemistry',
        'Biology',
        'Earth and Space',
        'Computer Science',
        'General Science'
    ]
    doc = '''\\documentclass{{scibowlset}}

    \\begin{{document}}
    \\newcounter{{qnumber}}\\stepcounter{{qnumber}}
    {content}
    \\end{{document}}'''
    pair = '''\\begin{{pair}} % {subject}
        \\ta{{
            {tossup}
        }}
        \\bn{{
            {bonus}
        }}
    \\end{{pair}}\n\n'''
    question = '''\\question{{\\theqnumber}}{{{subject}}}{{{format}}}
    {{{question}}}
    {{{answer}}}'''
    mc = '\\mc{{{W}}}{{{X}}}{{{Y}}}{{{Z}}}{{{ans}}}'
    sa = '\\sa{{{ans}}}'
