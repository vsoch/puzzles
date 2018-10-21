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

from puzzles.logger import bot
import json
import sys
import os


def main(args,parser,subparser):
    
    from puzzles.main solver import solve_puzzle

    # Here are the pictures, in a list
    if len(args.pictures) == 0:
        subparser.print_help()
        sys.exit(0)

    solution = solve_puzzle(args.pictures)
