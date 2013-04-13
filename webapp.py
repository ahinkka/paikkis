#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import re
import traceback
from itertools import islice
from bottle import route, run, get, request, response, abort
from db import search, info
from utils import levenshtein
from municipalities import municipalities

municipalities_set = set([m.lower() for m in municipalities.itervalues()])

@route('/v1/pois.json')
def pois_v1():
    global _db

    filter_s = unicode(request.query.get('filter', None), encoding='utf-8')
    if filter_s is None:
        abort(501, "Unfiltered searches not allowed.")

    result = search(database=_db, verbose=False, query=filter_s)

    municipality = request.query.get('municipality', None)
    if municipality:
        if municipality.lower() in municipalities_set:
            municipality_key = None
            for k, v in municipalities.iteritems():
                if v.lower() == municipality.lower():
                    municipality_key = k
                    break
            if not municipality_key:
                abort(501, "Unknown municipality: %s." % municipality)
            else:
                result = [r for r in result if r['municipality_id'] == municipality_key]


    try:
        result_count = int(request.query.get('resultcount', -1))

        if int(result_count) != -1:
            for r in result:
                distance = levenshtein(filter_s, r['name'])
                r['edit_distance'] = distance

            result.sort(key=lambda x: x['edit_distance'])
            result = list(islice(result, result_count))
    except:
        abort(501, "Cannot parse resultcount:%s." % request.query.get('resultcount'))

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
