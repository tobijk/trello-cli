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

import os
import json

from .error import TrelloConfigUnusable

class Config:

    DEFAULT_CONFIG = {
        "key": "INSERT API KEY",
        "token": "INSERT APP TOKEN"
    }

    @classmethod
    def get_config_folder(cls):
        return os.path.join(os.path.expanduser("~"), ".trello-cli")

    @classmethod
    def load_config(cls):
        config_dir  = Config.get_config_folder()
        config_file = os.path.join(config_dir, "config.json")

        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)

        if not os.path.isfile(config_file):
            with open(config_file, "w", encoding="utf-8") as fp:
                fp.write(json.dumps(Config.DEFAULT_CONFIG, indent=4,
                    ensure_ascii=False))
            msg = "please insert API key and APP token in ~/.trello-cli/config.json"
            raise TrelloConfigUnusable(msg)
        #end if

        with open(config_file, "r", encoding="utf-8") as fp:
            try:
                return json.load(fp)
            except json.JSONDecodeError as e:
                msg = "error in configuration on line %d, column %d." % \
                        (e.lineno, e.colno)
                raise TrelloConfigUnusable(msg)
            #end try
        #end with
    #end function

#end class

