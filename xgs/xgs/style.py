import sys

class Format:
    end = '\033[0m'
    underline = '\033[4m'
    bold = '\033[1m'

    class Colors:
        red = '\u001b[31m'
        light_red = '\033[1;31m'
        green = '\u001b[32m'

def bold(msg) -> str:
    return f"{Format.bold}{msg}{Format.end}"

def underlined(msg) -> str:
    return Format.underline + msg + Format.end

def color(string, color) -> str:
    if (n:=getattr(Format.Colors, color)) is not None:
        return f"{n}{string}{Format.end}"
    else:
        return string

def info(string):
    print(underlined(bold(color("INFO:", "green"))), string)

def warn(*args):
    print(underlined(bold(color("WARNING:", "light_red"))), *args)

def error(*args, exit_code=1):
    print(underlined(bold(color("ERROR:", "red"))), *args)
    sys.exit(exit_code)
