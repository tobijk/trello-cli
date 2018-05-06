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

from .client import tci
from .basemodel import BaseModel
from .list import List
from .label import Label

class Board(BaseModel):

    PATH = "/boards"

    @classmethod
    def all(cls, filter="open"):
        valid_filters = [
            "all",
            "closed",
            "members",
            "open",
            "organization",
            "public",
            "starred"
        ]

        if not filter in valid_filters:
            raise ValueError("invalid filter name '%s'" % filter)

        params = {"filter": filter}

        boards_data = tci()._execute("/members/me/boards", params=params)

        list_of_boards = []

        for data in boards_data:
            list_of_boards.append(Board(data))

        return list_of_boards
    #end function

    def __init__(self, data=None):
        super().__init__(data or {})

    def lists(self):
        params = { "card_fields": "id,name,pos" }

        lists_data = tci()._execute(self.PATH + "/" + self.id + List.PATH,
                params=params)

        list_of_lists = []

        for data in lists_data:
            list_of_lists.append(List(data))

        return list_of_lists
    #end function

    def labels(self):
        labels_data = tci()._execute(self.PATH + "/" + self.id + Label.PATH)

        list_of_labels = []

        for data in labels_data:
            list_of_labels.append(Label(data))

        return list_of_labels
    #end function

#end class

