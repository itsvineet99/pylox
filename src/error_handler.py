import sys

# separate file for error handling cause the original method was causing 
# cirucular error import 

had_error = False

def error(line_no, message):
    report(line_no, "", message)

def report(line_no, where, message):
    global had_err 

    # using file=sys.stderr redirects our output to err stream rather than general output stream
    print(f"[line {line_no}] error{where}: {message}", file=sys.stderr)
    had_err = True

