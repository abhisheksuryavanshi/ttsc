# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    baseurl = "http://abhishek7.pythonanywhere.com/days/"
    result = req.get("result")
    parameters = result.get("parameters")
    number = str(parameters.get("number-integer"))

    yql_url = baseurl + number
    result = urlopen(yql_url).read()
    data = json.loads(result)

    speech = "Today is: "+ data.get('day_name') +"day\n"+ \
            "Today's schedule:" +"\n" + \
            "Slot 1: " + data.get('slot_1') +"\n" + \
            "Slot 2: " + data.get('slot_2') +"\n" + \
            "Slot 3: " + data.get('slot_3') +"\n" + \
            "Slot 4: " + data.get('slot_4') +"\n" + \
            "Slot 5: " + data.get('slot_5') +"\n" + \
            "Slot 6: " + data.get('slot_6')

    res = {
        "speech": speech,
        "displayText": data.get('slot_1'),
        # "data": data,
        # "contextOut": [],
        "source": "my-timetable"
    }

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')