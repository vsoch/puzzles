#!/usr/bin/env python

'''

Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import puzzles
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="Python Puzzles Solver")

    # Global Variables
    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    parser.add_argument('--quiet', dest="quiet", 
                        help="suppress additional output.", 
                        default=False, action='store_true')

    description = 'actions for solving Puzzles in Python'
    subparsers = parser.add_subparsers(help='puzzles actions',
                                       title='actions',
                                       description=description,
                                       dest="command")

    # print version and exit
    version = subparsers.add_parser("version",
                                    help="show software version")

    # Solve
    solve = subparsers.add_parser("solve",
                                  help="solve a puzzle based on a picture.")

    solve.add_argument("pictures", nargs='*',
                       help='one or more pictures of pieces that make up the puzzle', 
                       type=str)


    return parser


def get_subparsers(parser):

    '''get_subparser will get a dictionary of subparsers,
       to help with printing help
    '''

    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]
    subparsers = dict()
    for action in actions:
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers



def main():
    ''' the main entrypoint for the "puzzles" client.
    '''

    parser = get_parser()
    subparsers = get_subparsers(parser)

    def help(return_code=0):
        '''print help, including the software version and exit with return code.
        '''

        version = puzzles.__version__

        print("\nPython Puzzles v%s" % version)
        parser.print_help()
        sys.exit(return_code)
    
    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # if environment logging variable not set, make silent
    if args.debug is False:
        os.environ['MESSAGELEVEL'] = "INFO"

    # Show the version and exit
    if args.command == "version":
        print(puzzles.__version__)
        sys.exit(0)

    # The only option now is solver
    from .solver import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args,
             parser=parser,
             subparser=subparsers[args.command])
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)

if __name__ == '__main__':
    main()
