# update [filename]
# add [-lf] [[[round number] [space-separated number list]] [filename]]
# tex [[--all] [--column=value]] [filename]

import re
from cmds import *

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

cmds = {

}

while True:
    cmd = input()
    if cmd == 'exit':
        break
    argv = parse(cmd)
    try:
        cmds[argv[0]](argv[1:])
    except KeyError as kerr:
        print('Command \"%s\" not found' % argv[0])
    except InvalidArgument as argerr:
        print('Invalid argument for \"%s\": %s' % (argv[0], argerr))