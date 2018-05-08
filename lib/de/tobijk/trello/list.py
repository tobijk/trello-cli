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
from .card import Card

class List(BaseModel):

    PATH = "/lists"

    def __init__(self, data=None):
        super().__init__(data or {})

    def cards(self):
        params = {"fields": "id,name"}
        cards_data = tci()._execute(self.PATH + "/" + self.id + Card.PATH,
                params=params)
        return [Card(data) for data in cards_data]
    #end function

    def insert(self, pos, card):
        if not isinstance(pos, int):
            raise ValueError("first argument to insert must be an integer")

        cards  = self.cards()
        ncards = len(cards)

        if pos < 0:
            pos = ncards + pos

        if pos == 0 or ncards == 0:
            pos = 0
        elif pos >= ncards:
            pos = cards[-1].pos + 1.0
        elif ncards == 1:
            pos = 0
        else:
            card_a, card_b = cards[pos-1:pos+1]
            pos = card_a.pos + (card_b.pos - card_a.pos) / 2.0
        #end if

        params = {}

        params.update(card.as_query())
        params.update({"idList": self.id, "pos": pos})

        result = tci()._execute(Card.PATH, verb="POST", params=params)

        card.update(result)
    #end function

#end class

