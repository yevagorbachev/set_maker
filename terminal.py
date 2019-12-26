# update [filename]
# add [-lf] [[[round number] [space-separated number list]] [filename]]
# tex [[--all] [--column=value]] [filename]

import re

def parse(arg: str):
    result = []
    quote = False
    last = 0
    for index, char in enumerate(arg):
        if char == '\"':
            quote = not quote
        if (char == ' ') and (not quote):
            result.append(arg[last:index])
            last = index + 1
    result.append(arg[last:])
    return result
