import optparse
import fileinput
import os
import sys


def takeEntriesFromStdin():
    """
    Request matches from user by stdin
    """
    print("Please enter game entries in format 'team name points",
          "team name points' (Example: Lions 3, Snakes 3)")
    print("Write done, to finish game input")

    input = []
    for line in sys.stdin:
        inputLine = line.rstrip()
        if inputLine != "done":
            input.append(inputLine)
        else:
            break
    return input


def parse_parameters():
    """
    Aux function to get the input
    If the parameter "-f" or "--file is in arguments,
    then read input from that file.
    if there are parameters in the program,
    take them as input.
    Else, let usser add entries by stdin.
    """
    param_parser = optparse.OptionParser()
    param_parser.add_option('-f', '--file')
    param_parser.add_option('-m', '--match', action="append")
    options, argv = param_parser.parse_args()

    # if file is defined, check if it exists and return file input
    if options.file:
        if os.path.isfile(options.file):
            return fileinput.input(options.file)
        else:
            print(options.file, " doesn't exists :(")
            exit(1)
    elif options.match:
        # if match is specified, then return those values
        return options.match
    elif len(argv):
        # if there are parameters, then return them and try to parse them later
        return argv
    else:
        return takeEntriesFromStdin()
