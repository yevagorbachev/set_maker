class Set():
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
    # format for a single question
    qformat = '''\\begin{{center}}
        \\textbf{{{TYPE}}} \\\\ By: {author}
    \\end{{center}}
    {num}) {SUBJECT} \\textit{{{form}}} {question}{choices}
    \\\\\\\\ANSWER: {answer}
    \\\\'''
    # format for choices
    choiceformat = '''\\\\
    \\\\W) {W}
    \\\\X) {X}
    \\\\Y) {Y}
    \\\\Z) {Z}'''
    # format for question pairs
    pairfomat = '''
    \\begin{{minipage}}{{\\textwidth}}
    {tossup}
    {bonus}
    \\underline{{\\hspace{{6.5in}}}}
    \\\\
    \\end{{minipage}}
    '''
    # LaTeX file template
    setformat = '''
    \\documentclass{{article}}
    \\usepackage[utf8]{{inputenc}}
    \\usepackage[letterpaper, portrait, margin=1in]{{geometry}}
    \\usepackage{{siunitx, amsmath, amssymb, setspace}}
    \\title{{{set}}}
    \\author{{}}
    \\date{{}}
    \\begin{{document}}
    \\maketitle
    \\noindent
    {content}
    \\end{{document}}'''.replace('    ','')