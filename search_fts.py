#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import codecs
import sqlite3

o8 = codecs.getwriter('utf-8')(sys.stdout)
e8 = codecs.getwriter('utf-8')(sys.stderr)


if __name__ == '__main__':
    conn = sqlite3.connect(sys.argv[1])
    c = conn.cursor()
    c.execute(u"""SELECT name FROM places_fts WHERE name MATCH '{0}*'""".format(sys.argv[2]))

    # names = []
    for row in c:
        # names.append(row[0])
        print(row)

    # for n in names:
    #     c.execute(u"SELECT * FROM places WHERE name=?", (n,))
    #     print(c.fetchone())
