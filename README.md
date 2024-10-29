# kg-enricher

[![PyPI version](https://badge.fury.io/py/kg-enricher.svg)](https://badge.fury.io/py/kg-enricher)

`kg-enricher` is an open source Python library for enriching strings, entities and knowledge graphs using Wikibase knowledge graphs. It's adapted for people, organizations and German geographic entities, both modern and historical. By default it connects to Wikidata, but it can be configured for any Wikibase instance.

**Context.** In project [BERD@NFDI](https://www.berd-nfdi.de) there are multiple knowledge graphs with German company data. We link strings to entities and enrich strings with data from knowledge graphs. For geographic strings we also check whether geographic coordinates of an entity correspond to a point inside modern or historical German boundaries using [the CShapes 2.0 Dataset](https://doi.org/10.1177/00220027211013).

## Table of contents
* [Installation](#installation)
* [How to use](#how-to-use)
* [Geographic linking](#geographic-linking)
* [Extra parameters](#extra-parameters)
* [Archived code](#archived-code)

## Installation

```
pip install kg-enricher
```

or

```
git clone https://github.com/UB-Mannheim/kg-enricher
cd kg-enricher/
pip install .
```

## How to use

Just import `enrich`-function and apply it to strings, which correspond to people, organizations or geographic entities.

An example for a person:
```python
from enricher import enrich
enrich("Adolf Daimler")
{'label': 'Adolf Daimler',
 'description': 'German entrepreneur (1871-1913)',
 'aliases': [],
 'id': 'Q361191',
 'url': 'https://www.wikidata.org/wiki/Special:EntityData/Q361191',
 'date_of_birth': {'time': '+1871-09-08T00:00:00Z',
  'timezone': 0,
  'before': 0,
  'after': 0,
  'precision': 11,
  'calendarmodel': 'http://www.wikidata.org/entity/Q1985727'},
 'date_of_death': {'time': '+1913-03-24T00:00:00Z',
  'timezone': 0,
  'before': 0,
  'after': 0,
  'precision': 11,
  'calendarmodel': 'http://www.wikidata.org/entity/Q1985727'},
 'VIAF ID': '77537760',
 'ISNI': '0000 0000 2006 7510',
 'GND ID': '135728673',
 'Google Knowledge Graph ID': '/g/11mvrmlm7'}
```

An example for a geographic entity:
```python
from enricher import enrich
enrich("Mannheim")
{'label': 'Mannheim',
 'description': 'city in Baden-Württemberg, Germany',
 'aliases': ['Mannem',
  'Monnem',
  'Universitätsstadt Mannheim',
  'Mannheim, Germany',
  'Mannheim (Germany)',
  'Mannheim Germany'],
 'id': 'Q2119',
 'url': 'https://www.wikidata.org/wiki/Special:EntityData/Q2119',
 'GeoNames ID': '2873891',
 'Geographic coordinates': {'latitude': 49.48777777777778,
  'longitude': 8.466111111111111,
  'altitude': None,
  'precision': 0.0002777777777777778,
  'globe': 'http://www.wikidata.org/entity/Q2'},
 'OSM Relation ID': '62691',
 'German district key': '08222',
 'German municipality key': '08222000',
 'German regional key': '082220000000',
 'UN/LOCODE': 'DEMHG',
 'Freebase ID': '/m/0pf5y',
 'OpenStreetMap node ID': '240060919',
 'is_within_current_germany': True,
 'is_within_historical_germany_1886_1919': True,
 'is_within_historical_germany_1919_1920': True,
 'is_within_historical_germany_1920_1938': True,
 'is_within_historical_germany_1938_1945': True,
 'is_within_historical_GFR_1945_1949': True,
 'is_within_historical_GFR_1949_1990': True,
 'is_within_historical_GFR_1990_2019': True,
 'is_within_historical_GDR_1945_1949': False,
 'is_within_historical_GDR_1949_1990': False}
```

An example for an organization:

```python
from enricher import enrich
enrich("BASF SE")
{'label': 'BASF',
 'description': 'German chemical company with worldwide reach',
 'aliases': ['Badische Anilin- & Soda-Fabrik',
  'Baden Aniline and Soda Factory',
  'BASF SE',
  'Badische Anilin- und Soda-Fabrik'],
 'id': 'Q9401',
 'url': 'https://www.wikidata.org/wiki/Special:EntityData/Q9401',
 'inception': {'time': '+1865-04-06T00:00:00Z',
  'timezone': 0,
  'before': 0,
  'after': 0,
  'precision': 11,
  'calendarmodel': 'http://www.wikidata.org/entity/Q1985727'},
 'LEI code': '529900PM64WH8AF1E917',
 'GRID ID': 'grid.3319.8',
 'ISIN': 'DE000BASF111',
 'EU Transparency Register ID': '7410939793-88',
 'Freebase ID': '/m/01713t',
 'EU Research participant ID': '999829926',
 'German Lobbyregister ID': 'R002326',
 'LinkedIn organization ID': 'basf',
 'PermID': '4295869198',
 'PM20 folder ID': 'co/002589'}
```

## Geographic linking

For geographic linking we use the geographic coordinates of an entity from Wikidata and check whether the point belongs to the boundaries of Germany using geojson files provided by [the CShapes 2.0 Dataset](https://doi.org/10.1177/00220027211013). The historical geographic boundaries of Germany from the CShapes 2.0 Dataset can be found at [https://demo.ldproxy.net](https://demo.ldproxy.net/cshapes/collections/boundary/items?limit=20&name=German%2A) under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0).

We use the following maps of Germany:

| State | Unique identifier | Start date | End date | Source identifier | Country capital |
| :---         |     :---:      |     :---:  | :---:  | :---:  | :---:  | 
| Germany (Prussia)   | [84](https://demo.ldproxy.net/cshapes/collections/boundary/items/84?f=html)     | 01/01/1886    | 27/06/1919 | 255 | Berlin |
| Germany (Prussia)   | [85](https://demo.ldproxy.net/cshapes/collections/boundary/items/85?f=html)     | 28/06/1919    | 09/02/1920 | 255 | Berlin |
| Germany (Prussia)   | [86](https://demo.ldproxy.net/cshapes/collections/boundary/items/86?f=html)     | 10/02/1920    | 29/09/1938 | 255 | Berlin |
| Germany (Prussia)   | [87](https://demo.ldproxy.net/cshapes/collections/boundary/items/87?f=html)     | 30/09/1938    | 07/05/1945 | 255 | Berlin |
| German Federal Republic   | [88](https://demo.ldproxy.net/cshapes/collections/boundary/items/88?f=html)     | 08/05/1945    | 20/09/1949 | 260 | Bonn |
| German Federal Republic   | [89](https://demo.ldproxy.net/cshapes/collections/boundary/items/89?f=html)     | 21/09/1949    | 02/10/1990 | 260 | Bonn |
| German Federal Republic   | [90](https://demo.ldproxy.net/cshapes/collections/boundary/items/90?f=html)     | 03/10/1990    | 31/12/2019 | 260 | Berlin |
| German Democratic Republic   | [91](https://demo.ldproxy.net/cshapes/collections/boundary/items/91?f=html)     | 08/05/1945    | 04/10/1949 | 265 | East Berlin |
| German Democratic Republic   | [92](https://demo.ldproxy.net/cshapes/collections/boundary/items/92?f=html)     | 05/10/1949    | 02/10/1990 | 265 | East Berlin |

If you use `kg-enricher` on geographic entities, please cite the following paper due to the license of the CShapes 2.0 Dataset:
`Schvitz, G., Girardin, L., Rüegger, S., Weidmann, N. B., Cederman, L.-E., & Gleditsch, K. S. (2022). Mapping the International System, 1886-2019: The CShapes 2.0 Dataset. Journal of Conflict Resolution, 66(1), 144-161. https://doi.org/10.1177/00220027211013563.`

An example for "West Berlin":
```python
from enricher import enrich
enrich("West Berlin")
{'label': 'West Berlin',
 'description': 'the Western sectors of Berlin between 1945 and 1990',
 'aliases': ['Berlin (West)', 'Westberlin', 'WB'],
 'id': 'Q56036',
 'url': 'https://www.wikidata.org/wiki/Special:EntityData/Q56036',
 'GeoNames ID': '11612751',
 'Geographic coordinates': {'latitude': 52.5,
  'longitude': 13.28,
  'altitude': None,
  'precision': 0.0002777777777777778,
  'globe': 'http://www.wikidata.org/entity/Q2'},
 'Freebase ID': '/m/082g6',
 'is_within_current_germany': True,
 'is_within_historical_germany_1886_1919': True,
 'is_within_historical_germany_1919_1920': True,
 'is_within_historical_germany_1920_1938': True,
 'is_within_historical_germany_1938_1945': True,
 'is_within_historical_GFR_1945_1949': False,
 'is_within_historical_GFR_1949_1990': False,
 'is_within_historical_GFR_1990_2019': True,
 'is_within_historical_GDR_1945_1949': True,
 'is_within_historical_GDR_1949_1990': True}
```

An example for "East Berlin":
```python
from enricher import enrich
enrich("East Berlin")
{'label': 'East Berlin',
 'description': 'Soviet sector of Berlin between 1949 and 1990',
 'aliases': ['Soviet zone of Berlin',
  'Berlin-Ost',
  'Ostberlin',
  'Soviet sector of Berlin',
  'Berlin, Hauptstadt der DDR',
  'Berlin Hauptstadt der DDR'],
 'id': 'Q56037',
 'url': 'https://www.wikidata.org/wiki/Special:EntityData/Q56037',
 'Geographic coordinates': {'latitude': 52.518611111111,
  'longitude': 13.404444444444,
  'altitude': None,
  'precision': None,
  'globe': 'http://www.wikidata.org/entity/Q2'},
 'Freebase ID': '/m/02lcc',
 'is_within_current_germany': True,
 'is_within_historical_germany_1886_1919': True,
 'is_within_historical_germany_1919_1920': True,
 'is_within_historical_germany_1920_1938': True,
 'is_within_historical_germany_1938_1945': True,
 'is_within_historical_GFR_1945_1949': False,
 'is_within_historical_GFR_1949_1990': False,
 'is_within_historical_GFR_1990_2019': True,
 'is_within_historical_GDR_1945_1949': True,
 'is_within_historical_GDR_1949_1990': True}
```

## Extra parameters

To get more than one matched entities, use `limit`-parameter (default is 1):
````
enrich('Heidelberg', limit=3)
```

To get labels, descriptions, and aliases in a specific language, use `language`-parameter (default is "en"):
````
enrich('Breslau', language="de")
```

## Archived code

Shigapov, R. (2023). KG-enricher: An open-source Python library for enriching strings, entities and knowledge graphs using Wikibase knowledge graphs (0.1.0). Zenodo. https://doi.org/10.5281/zenodo.10405073