Paikkis
=======

MML:n nimistöaineisto ja automaattitäydennys sqlitellä.

Käyttöohjeet
------------
Komennot tottelevat -h ja --help -parametrejä.

::
    
    # Luo tietokanta (kestää mulla vartin)
    ./paikkis build
    # Tee haku (full-text -indeksi)
    ./paikkis search hakusana(t)


Web-API:
::

    # Käynnistys (tietokanta täytyy olla ensin luotuna)
    ./webapp.py
    # Eri terminaalissa:
    curl http://localhost:8022/v1/pois.json\?filter\=Kourilehto | python -mjson.tool
    # Haku ei toimi ilman filter-parametria, vaan palauttaa 501-statuksen.    

TODO
----

- hakutulosten pisteyttäminen ja järjestäminen pisteytyksen mukaan
- triviaalina pisteytysalgoritmina toimii alkuun etäisyys nykysijainnista,
  jonka voi tarjota parametrina
- hakutulosten sivutus (mahdollistaisi kaikkien kohteiden haun sivutettuna)


Resurssit
---------

- http://kartat.kapsi.fi/files/nimisto/paikannimet_kaikki/etrs89/
