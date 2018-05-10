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

from dateutil.parser import parse as dateparse

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
        try:
            # load config from .trello-cli/config.json
            config = Config.load_config()

            # initialize Trello API client context
            TrelloClient(config["key"], config["token"])

            # go figure out what to do
            Cli.execute_command()
        except TrelloBaseError as e:
            sys.stderr.write("trello-cli: %s\n" % str(e))
            sys.exit(Cli.EXIT_ERR)
        #end try

        return Cli.EXIT_OK
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
            "   delete                                                         \n"
            "   move                                                           \n"
            "                                                                  \n"
            "Run 'trello-cli <command> --help' for more information.           \n"
        )
    #end function

    @staticmethod
    def execute_command():
        try:
            command = sys.argv[1]
        except IndexError:
            Cli.usage()
            sys.exit(Cli.EXIT_OK)
        #end function

        if command == "list":
            return CliList(sys.argv[1:]).execute_command()
        if command == "create":
            return CliCreate(sys.argv[1:]).execute_command()
        if command == "delete":
            return CliDelete(sys.argv[1:]).execute_command()
        if command == "move":
            return CliMove(sys.argv[1:]).execute_command()
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

        for i in range(len(boards)):
            b = boards[i]
            print("| %3d | %s | %-40.40s |" % (i, b.id, b.name))
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
            print("| %3d | %s | %-27.27s | %-10.10s |" % (i, l.id, l.name, l.color))
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
            " --name <text>     Specify the name of the new item.              \n"
            " --desc <text>     More verbose description of the item.          \n"
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
            " --comment <text>  An initial comment to attache to the card.     \n"
            " --due <date>      An optional due date.                          \n"
            "                                                                  \n"
        )
    #end function

    def execute_command(self):
        try:
            type_ = self._argv[1]
        except IndexError:
            type_ = None

        self._parse_opts()

        if type_ == "card":
            self.create_card()
        else:
            CliCreate.usage()
            sys.exit(Cli.EXIT_ERR)
    #end function

    def create_card(self):
        if not "list-id" in self._options:
            raise CliInvocationError("please specify a list id.")

        try:
            list_ = List.by_id(self._options["list-id"])
        except TrelloClientError as e:
            raise CliInvocationError("failed to locate the specified list.")

        labels = self._options.get("labels", [])

        for l in labels:
            try:
                Label.by_id(l)
            except TrelloClientError as e:
                raise CliInvocationError(
                    "unable to locate or no such label: '%s'" % l)
        #end for

        card = Card()

        pos = self._options.get("position", len(list_.cards()))

        if ("name" in self._options) and self._options["name"]:
            card.name = self._options["name"]
        if ("desc" in self._options) and self._options["desc"]:
            card.desc = self._options["desc"]
        if ("due" in self._options) and self._options["due"]:
            card.due = self._options["due"]

        card.idLabels = labels

        list_.insert(pos, card)

        comment = self._options.get("comment")
        if comment:
            card.add_comment(comment)
    #end function

    def _parse_opts(self):
        try:
            opts, args = getopt.getopt(self._argv[2:], "h",
                    ["help", "name=", "desc=", "position=", "list-id=",
                        "labels=", "comment=", "due="])
        except getopt.GetoptError as e:
            CliCreate.usage()
            sys.exit(Cli.EXIT_ERR)
        #end try

        for o, v in opts:
            if o == "--help":
                CliCreate.usage()
                sys.exit(Cli.EXIT_OK)
            elif o == "--name":
                self._options["name"] = v.strip()
            elif o == "--desc":
                self._options["desc"] = v.strip()
            elif o == "--position":
                try:
                    v = int(v.strip())
                except ValueError:
                    raise CliInvocationError(
                            "expected an integer argument for --position.")
                #end try

                self._options["position"] = v
            elif o == "--list-id":
                self._options["list-id"] = v.strip()
            elif o == "--labels":
                self._options["labels"] = list(
                        filter(bool, v.strip().split(",")))
            elif o == "--comment":
                self._options["comment"] = v.strip()
            elif o == "--due":
                try:
                    due_date = dateparse(v)
                except ValueError:
                    raise CliInvocationError("could not parse due date.")
                self._options["due"] = str(due_date.date())
            #end if
        #end for
    #end function

#end class

class CliDelete:

    def __init__(self, argv):
        self._argv    = argv
        self._options = {}
    #end function

    @staticmethod
    def usage():
        Cli.copyright()

        sys.stdout.write(
            "Usage: trello-cli delete <TYPE> [OPTIONS]                         \n"
            "                                                                  \n"
            "TYPES:                                                            \n"
            "                                                                  \n"
            "   card                                                           \n"
            "                                                                  \n"
            "OPTIONS:                                                          \n"
            "                                                                  \n"
            " --card-id <id>    Specify the card to delete.                    \n"
            "                                                                  \n"
        )
    #end function

    def execute_command(self):
        try:
            type_ = self._argv[1]
        except IndexError:
            type_ = None

        self._parse_opts()

        if type_ == "card":
            self.delete_card()
        else:
            CliDelete.usage()
            sys.exit(Cli.EXIT_ERR)
    #end function

    def delete_card(self):
        if not "card-id" in self._options:
            raise CliInvocationError("please specify a card id.")

        try:
            Card(data={"id": self._options["card-id"]}).delete()
        except TrelloClientError as e:
            raise CliInvocationError("failed to delete the specified card.")
    #end function

    def _parse_opts(self):
        try:
            opts, args = getopt.getopt(self._argv[2:], "h",
                    ["help", "card-id="])
        except getopt.GetoptError as e:
            CliDelete.usage()
            sys.exit(Cli.EXIT_ERR)
        #end try

        for o, v in opts:
            if o == "--help":
                CliDelete.usage()
                sys.exit(Cli.EXIT_OK)
            elif o == "--card-id":
                self._options["card-id"] = v.strip()
            #end if
        #end for
    #end function

#end class

class CliMove:

    def __init__(self, argv):
        self._argv    = argv
        self._options = {}
    #end function

    @staticmethod
    def usage():
        Cli.copyright()

        sys.stdout.write(
            "Usage: trello-cli move <TYPE> [OPTIONS]                           \n"
            "                                                                  \n"
            "TYPES:                                                            \n"
            "                                                                  \n"
            "   card                                                           \n"
            "                                                                  \n"
            "OPTIONS:                                                          \n"
            "                                                                  \n"
            " --list-id <id>    Specify the id of the list to move the card to.\n"
            "                                                                  \n"
        )
    #end function

    def execute_command(self):
        try:
            type_ = self._argv[1]
        except IndexError:
            type_ = None

        self._parse_opts()

        if type_ == "card":
            self.move_card()
        else:
            CliMove.usage()
            sys.exit(Cli.EXIT_ERR)
    #end function

    def move_card(self):
        if not "list-id" in self._options:
            raise CliInvocationError("please specify a list id.")

        try:
            Card(data={"id": self._options["card-id"]})\
                    .move_to(self._options["list-id"])
        except TrelloClientError as e:
            raise CliInvocationError("failed to move the card.")
    #end function

    def _parse_opts(self):
        try:
            opts, args = getopt.getopt(self._argv[2:], "h",
                    ["help", "card-id=", "list-id="])
        except getopt.GetoptError as e:
            CliDelete.usage()
            sys.exit(Cli.EXIT_ERR)
        #end try

        for o, v in opts:
            if o == "--help":
                CliDelete.usage()
                sys.exit(Cli.EXIT_OK)
            elif o == "--card-id":
                self._options["card-id"] = v.strip()
            elif o == "--list-id":
                self._options["list-id"] = v.strip()
            #end if
        #end for
    #end function

#end class

