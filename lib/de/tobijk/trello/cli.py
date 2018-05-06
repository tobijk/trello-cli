# -*- encoding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Tobias Koch <tobias.koch@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import sys
import getopt
import argparse

from .client import Client as TrelloClient
from .config import Config
from .error  import TrelloBaseError, CliInvocationError, TrelloClientError
from .board  import Board
from .list   import List
from .card   import Card
from .label  import Label

class Cli:

    EXIT_OK  = 0
    EXIT_ERR = 1

    @staticmethod
    def main():
        rval = Cli.EXIT_ERR

        try:
            # load config from .trello-cli/config.json
            config = Config.load_config()

            # initialize Trello API client context
            TrelloClient(config["key"], config["token"])

            rval = Cli.execute_command()
        except TrelloBaseError as e:
            sys.stderr.write("trello-cli: %s\n" % str(e))
            sys.exit(Cli.EXIT_ERR)
        #end try

        return rval
    #end function

    @staticmethod
    def copyright():
        sys.stdout.write(
            "Trello mini CLI                                                   \n"
            "Copyright 2018 Tobias Koch <tobias.koch@gmail.com>                \n"
            "                                                                  \n"
        )
    #end function

    @staticmethod
    def usage():
        Cli.copyright()

        sys.stdout.write(
            "Usage: trello-cli <COMMAND> [options] <arguments>                 \n"
            "                                                                  \n"
            "COMMANDS:                                                         \n"
            "                                                                  \n"
            "   list                                                           \n"
            "   create                                                         \n"
            "                                                                  \n"
            "Run 'trello-cli <command> --help' for more information.           \n"
        )
    #end function

    @staticmethod
    def execute_command():
        known_commands = ["list", "show", "create", "delete"]

        try:
            command = sys.argv[1]
        except IndexError:
            Cli.usage()
            sys.exit(Cli.EXIT_OK)
        #end function

        if command == "list":
            return CliList(sys.argv[1:]).execute_command()
        else:
            Cli.usage()
            sys.exit(Cli.EXIT_ERR)
    #end function

#end class

class CliList:

    def __init__(self, argv):
        self._argv    = argv
        self._options = {}
    #end function

    @staticmethod
    def usage():
        Cli.copyright()

        sys.stdout.write(
            "Usage: trello-cli list <TYPE> [OPTIONS]                           \n"
            "                                                                  \n"
            "TYPES:                                                            \n"
            "                                                                  \n"
            "   boards                                                         \n"
            "   lists                                                          \n"
            "   cards                                                          \n"
            "   labels                                                         \n"
            "                                                                  \n"
            "OPTIONS:                                                          \n"
            "                                                                  \n"
            " --board-id <id>   When listing lists or labels, a board needs to \n"
            "                   be specified.                                  \n"
            " --list-id <id>    When listing cards, a list (column) needs to be\n"
            "                   specifed.                                      \n"
            "                                                                  \n"
        )
    #end function

    def execute_command(self):
        known_types = ["boards", "lists", "cards", "labels"]

        try:
            type_ = self._argv[1]
        except IndexError:
            type_ = None

        self._parse_opts()

        if type_ == "boards":
            self.list_boards()
        elif type_ == "lists":
            self.list_lists()
        elif type_ == "cards":
            self.list_cards()
        elif type_ == "labels":
            self.list_labels()
        else:
            CliList.usage()
            sys.exit(Cli.EXIT_ERR)
    #end function

    def list_boards(self):
        if "board-id" in self._options:
            boards = [Board.by_id(self._options["board-id"])]
        else:
            boards = Board.all()
        #end if

        for b in boards:
            print("| %s | %-45.45s |" % (b.id, b.name))
    #end function

    def list_lists(self):
        if not "board-id" in self._options:
            raise CliInvocationError("please specify the board id.")

        try:
            board = Board.by_id(self._options["board-id"])
        except TrelloClientError as e:
            raise CliInvocationError("failed to locate the specified board.")

        lists = board.lists()

        for i in range(len(lists)):
            l = lists[i]
            print("| %3d | %s | %-40.40s |" % (i, l.id, l.name))
    #end function

    def list_cards(self):
        if not "list-id" in self._options:
            raise CliInvocationError("please specify the list id.")

        try:
            list_ = List.by_id(self._options["list-id"])
        except TrelloClientError as e:
            raise CliInvocationError("failed to locate the specified list.")

        cards = list_.cards()

        for i in range(len(cards)):
            c = cards[i]
            print("| %3d | %s | %-40.40s |" % (i, c.id, c.name))
    #end function

    def list_labels(self):
        if not "board-id" in self._options:
            raise CliInvocationError("please specify the board id.")

        try:
            board = Board.by_id(self._options["board-id"])
        except TrelloClientError as e:
            raise CliInvocationError("failed to locate the specified board.")

        labels = board.labels()

        for i in range(len(labels)):
            l = labels[i]
            print("| %3d | %s | %-30.30s | %-10.10s |" % (i, l.id, l.name, l.color))
    #end function

    def _parse_opts(self):
        try:
            opts, args = getopt.getopt(self._argv[2:], "h",
                    ["help", "board-id=", "list-id="])
        except getopt.GetoptError as e:
            CliList.usage()
            sys.exit(Cli.EXIT_ERR)
        #end try

        for o, v in opts:
            if o == "--help":
                CliList.usage()
                sys.exit(Cli.EXIT_OK)
            elif o == "--board-id":
                self._options["board-id"] = v.strip()
            elif o == "--list-id":
                self._options["list-id"] = v.strip()
        #end for
    #end function

#end class

class CliCreate:

    def __init__(self, argv):
        self._argv    = argv
        self._options = {}
    #end function

    @staticmethod
    def usage():
        Cli.copyright()

        sys.stdout.write(
            "Usage: trello-cli create <TYPE> [OPTIONS]                         \n"
            "                                                                  \n"
            "TYPES:                                                            \n"
            "                                                                  \n"
            "   card                                                           \n"
            "                                                                  \n"
            "OPTIONS:                                                          \n"
            "                                                                  \n"
            " --name            Specify the name of the new item.              \n"
            " --desc            More verbose description of the item.          \n"
            "                                                                  \n"
            " --position        Where to insert the item (relevant for cards). \n"
            "                   This must be an integer. The item will be      \n"
            "                   inserted just before the item which is         \n"
            "                   currently at the given index (counting from 0).\n"
            "                                                                  \n"
            "                   In programmer parlance, this behaves like      \n"
            "                   Python list's `insert` method.                 \n"
            "                                                                  \n"
            "                   Examples:                                      \n"
            "                                                                  \n"
            "                   0         - insert at the very beginning       \n"
            "                   2         - insert before item at index 2      \n"
            "                   len(list) - insert at the very end             \n"
            "                                                                  \n"
            " --list-id <id>    When creating cards, a list (column) needs to  \n"
            "                   be specifed.                                   \n"
            " --labels <id..>   Comma separate list of label IDs to tag a      \n"
            "                   card with.                                     \n"
            "                                                                  \n"
        )
    #end function

    def execute_command(self):
        known_types = ["card"]

        try:
            type_ = self._argv[1]
        except IndexError:
            type_ = None

        self._parse_opts()

        if type_ == "card":
            self.create_card()
        else:
            CliList.usage()
            sys.exit(Cli.EXIT_ERR)
    #end function

    def create_card(self):
        pass

#end class

