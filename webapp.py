#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import traceback
from bottle import route, run, get, request, response, abort
from db import search, info

@route('/v1/pois.json')
def pois_v1():
    global _db

    filter = request.query.get('filter', None)
    if filter is None:
        abort(501, "Unfiltered searches not allowed.")

    result = search(database=_db, verbose=False, query=filter)
    response.content_type = 'application/json'

    return json.dumps(result, ensure_ascii=False)

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("--host", dest="host",
                      help="bind to HOST", metavar="HOST", default="localhost")
    parser.add_option("--port", dest="port",
                      help="bind to PORT", metavar="PORT", type="int", default=8022)

    parser.add_option("-d", "--database", dest="db",
                      help="use database FILE", metavar="FILE", default="paikkis.db")

    opts, args = parser.parse_args()
    _db = opts.db
    run(host=opts.host, port=opts.port)
