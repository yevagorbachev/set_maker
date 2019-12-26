# update [filename]
# add [-lf] [[[round number] [space-separated number list]] [filename]]
# tex [[--all] [--column=value]] [filename]

import re

def parse(arg: str):
    result = []
    quote = False
    for index, char in enumerate(arg):
        if char == '\"':
            quote = not quote
        if (char == ' ') and (not quote):
            result.append(arg[:index])
            arg = arg[index + 1:]
    return result

tests = [
    'tex --all all.tex',
    'tex --all \"all with space.tex\"',
    'tex --col=oneword oneword.tex'
    'tex --col=\"not oneword\" \"not oneword.tex\"'
]

for test in tests:
    print(parse(test))