Paikkis
=======

MML:n nimistöaineisto ja automaattitäydennys sqlitellä.

Käyttöohjeet
------------

::
    
    # Luo tietokanta (kestää mulla vartin)
    ./model.py PNR_2012_01.TXT tietokannannimi.db
    # Tee haku (full-text -indeksi)
    ./search_fts.py tietokannannimi.db hakusana
    # ...tai... (LIKE "hakusana%" -haku)
    ./search.py tietokannannimi.db hakusana


TODO
----

Kunnollinen optparsella varustellu db_tool.py, joka tuottaisi tietokannan,
antaisi hyvää debuggia ja jolla voisi tuottaa kannan vaikka vain osajoukosta
rivejä (rivinumeroiden mukaan, karttakoordinaattien mukaan).

search.py ja search_fts.py vain referensseinä, nekin pitäisi eristää
kunnollisen abstraktion taakse.


Resurssit
---------

- http://kartat.kapsi.fi/files/nimisto/paikannimet_kaikki/etrs89/
