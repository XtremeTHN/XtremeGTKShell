import sys
import traceback

from pystyle import Colorate, Colors

class Format:
    end = '\033[0m'
    underline = '\033[4m'
    bold = '\033[1m'

def bold(msg) -> str:
    return f"{Format.bold}{msg}{Format.end}"

def underlined(msg) -> str:
    return Format.underline + msg + Format.end

def color(string, color) -> str:
    return Colorate.Horizontal(color, string)

def info(*args):
    func = traceback.extract_stack()[-2]
    print(underlined(bold(color(f"{func.name} > INFO:", Colors.green_to_yellow))), *args)

def debug(*args):
    func = traceback.extract_stack()[-2]
    if "--debug" in sys.argv:
        print(underlined(bold(color(f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > DEBUG:", Colors.blue_to_cyan))), *args)

def warn(*args):
    func = traceback.extract_stack()[-2]
    print(underlined(bold(color(f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > WARNING:", Colors.red_to_yellow))), *args)

def error(*args, exit_code=1):
    func = traceback.extract_stack()[-2]
    print(underlined(bold(color(f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > ERROR:", Colors.red_to_blue))), *args)
    sys.exit(exit_code)
