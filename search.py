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
    c.execute(u"""SELECT * FROM places WHERE name LIKE '{0}%'""".format(sys.argv[2]))
    for row in c:
        print(row)

