#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  0   paikannimi
  1   nimen kielikoodi
  2   kielen nimi
  3   paikkatyypin koodi
  4   paikkatyypin selite
  5   kkj/pkj pohjoinen
  6   kkj/pkj itä
  7   kkj/ykj pohjoinen
  8   kkj/ykj itä
  9   etrs/tm35fin pohjoinen
 10   etrs/tm35fin itä
 11   kuntakoodi
 12   kunnan nimi
 13   seutukuntakoodi
 14   seutukunnan nimi
 15   maakunnan koodi
 16   maakunnan nimi
 17   suuraluekoodi
 18   suuralueen nimi
 19   läänikoodi
 20   läänin nimi
 21   lehtijaon 5x5 tunnus
 22   pelastuslehtijaon tunnus
 23   etrs-tm35 -tunnus
 24   nimen kielen virallisuuskoodi
 25   nimen kielen virallisuusselite
 26   nimen kielen enemmistöasemakoodi
 27   nimen kielen enemmistöselitys
 28   paikannimenlähdekoodi
 29   paikannimen lähdeselitys
 30   paikka-id
 31   paikannimen id

 Suomi-englanti:
 http://www.google.fi/url?sa=t&rct=j&q=&esrc=s&source=web&cd=18&ved=0CEUQFjAHOAo&url=http%3A%2F%2Fwww.pohjois-karjala.fi%2Fdman%2FDocument.phx%2F~maakuntaliitto%2FJulkiset%2FEUFUND%2FHankesanasto%3FfolderId%3D~maakuntaliitto%252FJulkiset%252FEUFUND%26cmd%3Ddownload&ei=-RKIUISCGMKA4gS9roHYCg&usg=AFQjCNEqVl4XU868FwPn8C-_qlnozH81Vw&cad=rja
"""
from __future__ import print_function

import sys
import codecs
import sqlite3

from coordinates import Translate, COORD_TYPE_WGS84, COORD_TYPE_ETRSTM35FIN

o8 = codecs.getwriter('utf-8')(sys.stdout)
e8 = codecs.getwriter('utf-8')(sys.stderr)


# Input:     dictionary with ['type'] is coordinate system type identifier
#                            ['N'] is coordinate Northing / Lat
#                            ['E'] in coordinate Easting / Lon
#            type identifier of the coordinate system to transform the input
#                            coordinates to
# Output:    dictionary with ['type'] is coordinate system type identifier
#                            ['N'] is coordinate Northing / Lat
#                            ['E'] in coordinate Easting / Lon

class Place(object):
    def __init__(self, lst):
        self.name = lst[0]
        wgs84_coords = Translate({'type': COORD_TYPE_ETRSTM35FIN,
                                  'N': float(lst[9]), 'E': float(lst[10])}, COORD_TYPE_WGS84)
        self.lat = wgs84_coords['N']
        self.lon = wgs84_coords['E']

        self.type_id = lst[3]
        self.municipality_id = lst[11]
        self.sub_region_id = lst[13]
        self.NUTS3_region_id = lst[15]
        self.NUTS2_region_id = lst[17]
        self.id = lst[30]


    def __repr__(self):
        return "<Place %s %s>" % (self.id, str(self))

    def __str__(self):
        return unicode(self).encode('ASCII', 'backslashreplace')

    def __unicode__(self):
        return u"{0}, {1}; {2}, {3}".format(self.name, self.municipality_id, self.lat, self.lon)

    def insert_stmt(self):
        return (u"INSERT INTO places (name, municipality_id, id, lat, lon, type_id, sub_region_id, NUTS2_region_id, NUTS3_region_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (self.name,
                  self.municipality_id,
                  self.id,
                  self.lat,
                  self.lon,
                  self.type_id,
                  self.sub_region_id,
                  self.NUTS2_region_id,
                  self.NUTS3_region_id))


if __name__ == '__main__':
    conn = sqlite3.connect(sys.argv[2])
    c = conn.cursor()
    c.execute('''CREATE TABLE places
                 (name text, municipality_id int, id int, lat float, lon float, type_id int, sub_region_id int, NUTS2_region_id int, NUTS3_region_id int)''')
    c.execute('''CREATE INDEX name_idx ON places (name)''')
    c.execute('''CREATE VIRTUAL TABLE places_fts USING fts3(name, id, type_id);''')
    conn.commit()

    with codecs.open(sys.argv[1], 'r', encoding='iso-8859-10') as f:
        for linenum, line in enumerate(f):
            parts = [item.strip() for item in line.replace("\n", "").split(";") if len(item) > 0]

            p = Place(parts)
            c.execute(*p.insert_stmt())
            c.execute(u"INSERT INTO places_fts (id, type_id, name) VALUES (?, ?, ?)", (p.id, p.type_id, p.name))

            # print(p, file=o8)

            if linenum % 10000 == 0:
                conn.commit()
                print(u"# {0}...".format(linenum))

        conn.commit()
