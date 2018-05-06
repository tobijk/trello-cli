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

import json
from .client import tci 

class BaseModel(dict):

    @classmethod
    def by_id(cls, obj_id):
        result = tci()._execute(self.PATH + "/" + obj_id)
        return cls(result)
    #end function

    def __init__(self, data):
        super().__init__(data)

    def __getattr__(self, name):
        if not name in self:
            if self.get("id", None) is not None:
                self.refresh()
        return self[name]
    #end function

    def __setattr__(self, name, value):
        self[name] = value

    def to_json(self):
        return json.dumps(self, indent=4, ensure_ascii=False)

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as fp:
            return json.load(fp)
    #end function

    def as_query(self):
        params = {}

        for name, type_ in self.FIELDS:
            if name in self:
                if type_ == str:
                    params[name] = self[name]
                elif type_ == bool:
                    params[name] = "true" if self[name] else "false"
                elif type_ == list:
                    params[name] = ",".join([str(item) for item in self[name]])
                else:
                    params[name] = str(self[name])
            #end if
        #end for

        return params
    #end function

    def refresh(self):
        data = tci()._execute(self.PATH + "/" + self.id)
        self.update(data)
    #end function

#end class

