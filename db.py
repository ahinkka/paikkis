# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import codecs
from model import Place

CREATE_TABLE = '''CREATE TABLE places
                   (name text,
                    municipality_id int,
                    id int,
                    lat float,
                    lon float,
                    type_id int,
                    sub_region_id int,
                    NUTS2_region_id int,
                    NUTS3_region_id int)'''
CREATE_FTS_TABLE = '''CREATE VIRTUAL TABLE places_fts USING fts3(name, id);'''

# "CREATE INDEX name_idx ON places (name)",
CREATE_INDEX = "CREATE INDEX id_place_idx ON places (id)"

def build(input, database, verbose):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(CREATE_TABLE)
    c.execute(CREATE_INDEX)
    c.execute(CREATE_FTS_TABLE)
    conn.commit()

    size = os.path.getsize(input)
    total_read = 0
    with codecs.open(input, 'r', encoding='iso-8859-10') as f:
        for linenum, line in enumerate(f):
            total_read += len(line)
            parts = [item.strip()
                     for item in line.replace("\n", "").split(";")
                     if len(item) > 0]

            p = Place(parts)
            c.execute(*p.insert_stmt())
            c.execute(*p.insert_fts_stmt())

            if linenum % 10000 == 0:
                conn.commit()
                print(u"# {0:.3}% {1}...".format(100 * (float(total_read) / float(size)),
                                                str(p)))
        conn.commit()

FTS_QUERY = \
        u"""SELECT p.id, f.name, p.lat, p.lon, p.type_id
                FROM places_fts AS f, places AS p
                WHERE f.name MATCH ? || '*' AND f.id = p.id"""

# SEARCH_QUERY = \
#     u"SELECT id, name, lat, lon FROM places WHERE name LIKE ? || '%"

def search(database, verbose, query):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(FTS_QUERY, (query,))

    result = []
    for row in c:
        result.append({ 'id': row[0],
                        'name': row[1],
                        'lat': row[2], 'lon': row[3],
                        'type_id': row[4] })
    return result

INFO_QUERY = \
    u"""SELECT name, municipality_id, id, lat, lon, type_id,
              sub_region_id, NUTS2_region_id, NUTS3_region_id
            FROM places WHERE id=?"""

def info(database, verbose, id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute(INFO_QUERY, (id,))

    row = c.fetchone()
    result = {
        'name': row[0],
        'municipality_id': row[1],
        'id': row[2],
        'lat': row[3],
        'lon': row[4],
        'type_id': row[5],
        'sub_region_id': row[6],
        'NUTS2_region_id': row[7],
        'NUTS3_region_id': row[8]
        }

    return result
