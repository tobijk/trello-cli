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

import requests
from .error import TrelloClientError, TrelloServerError

def tci():
    return Client.instance()

class Client:

    INSTANCE = None

    def __init__(self, key, token, url="https://api.trello.com/1/"):
        self._url       = url
        self._key       = key
        self._token     = token
        Client.INSTANCE = self
    #end function

    @classmethod
    def instance(cls):
        return Client.INSTANCE

    def _execute(self, path, verb=None, params=None, data=None):
        if params is None:
            params = {}

        params.update({
            "key":   self._key,
            "token": self._token
        })

        full_url = self._url + path

        if verb is None:
            if data is None:
                verb = "GET"
            else:
                verb = "POST"
        #end if

        response = requests.request(verb, self._url + path, params=params,
                data=data)

        if not response.ok:
            if response.status_code >= 500:
                raise TrelloServerError(response.reason + ": " + response.text)
            if response.status_code >= 400:
                raise TrelloClientError(response.reason + ": " + response.text)
        #end if

        return response.json()
    #end function

#end class

