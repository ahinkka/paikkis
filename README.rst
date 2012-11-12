Paikkis
=======

MML:n nimistöaineisto ja automaattitäydennys sqlitellä.

Käyttöohjeet
------------
Komennot tottelevat -h ja --help -parametrejä.


Web-API:
::

    # http://api.paikkis.fi/versio/pois.json\?parametrit  esim:
    http://api.paikkis.fi/v1/pois.json?filter=Kourilehto


Asennus:
::

    # Luo tietokanta (kestää hetken)
    ./paikkis build
    # Tee haku (full-text -indeksi)
    ./paikkis search hakusana(t)
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
- Paikkatyypit (type_id): http://paikkis.fi/paikkatyypit.txt
- Kuntien koodit (municipality_id): http://www.tilastokeskus.fi/meta/luokitukset/kunta/001-2012/index.html

Käytetyt kirjastot
------------------

- coordinates.py: Olli Lammin erinomainen kirjasto suomalaisten
  koordinaattijärjestelmien muuntamiseen WGS84-muotoon,
  <http://olammi.iki.fi/sw/coordinates_v1_0a.zip>, MIT-lisenssi
- bottle.py: <http://bottlepy.org/>, MIT-lisenssi
- docopt.py: <https://github.com/docopt/docopt>, MIT-lisenssi


Lisenssi
--------

MIT-lisenssi, katso tiedosto LICENSE.
