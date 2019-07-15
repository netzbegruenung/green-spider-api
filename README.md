[![Docker Repository on Quay](https://quay.io/repository/netzbegruenung/green-spider-api/status "Docker Repository on Quay")](https://quay.io/repository/netzbegruenung/green-spider-api)

# green-spider-api

Web service API für die [Green Spider Webapp](https://github.com/netzbegruenung/green-spider-webapp)

## API Dokumentation

Hinweis: Die API ist in einer frühen Entwicklungsphase. Änderungen (breaking changes) ohne vorherige Ankündigung sind zu erwarten.

### `GET /api/v1/spider-results/last-updated/`

Gibt den Zeitpunkt der letzten Aktualisierung der Spider-Ergebnisse zurück.

```json
{
  "last_updated": "2018-10-25T15:23:30.589683"
}
```

### `GET /api/v1/spider-results/table/`

Gibt Ergebnisse für alle Sites in einem tabellenfreundlichen Format aus.

Wenn per `Accept`-Header der Typ `text/csv` angefordert wird, erfolgt die Ausgabe
im CSV-Format. Ansonsten wird JSON ausgegeben.

```json
[
  {
    "input_url": "http://die-gruenen-burscheid.de/",
    "created": "2019-07-05T17:42:00.884759+00:00",
    "score": 12.5,
    "meta.type": "REGIONAL_CHAPTER",
    "meta.city": "Burscheid",
    "meta.district": "Rheinisch-Bergischer Kreis",
    "meta.level": "DE:ORTSVERBAND",
    "meta.state": "Nordrhein-Westfalen",
    "rating.FEEDS.value": true,
    "rating.FEEDS.score": 1,
    "rating.HTTP_RESPONSE_DURATION.score": 0.5,
    "rating.HTTP_RESPONSE_DURATION.value": 425,
    ...
    "rating.SITE_REACHABLE.value": true,
    "rating.SITE_REACHABLE.score": 1,
    "generator": "wordpress-urwahl",
    "resulting_urls": "http://die-gruenen-burscheid.de/"
  },
  ...
]
```

### `GET /api/v1/spider-results/site?url={site_url}`

Gibt sämtliche Inhalte zu einer Site aus.

Ein Beispiel würde hier den Rahmen sprengen.

### `GET /api/v1/screenshots?url={site_url}`

Gibt Daten zu allen vorhandenen Screenshots zu einer Site aus.

```json
[
  {
    "url": "http://wordpress.gruene-hameln-pyrmont.de/category/hessisch-oldendorf-gesamt/",
    "screenshot_url": "http://green-spider-screenshots.sendung.de/1500x1500/4fc61b4918dc9eaaef645c694c84224e.png",
    "user_agent": "phantomjs-2.1.1",
    "size": [1500, 1500],
    "created": "2018-10-08T08:33:21.284933+00:00"
  },
  {
    "url": "http://wordpress.gruene-hameln-pyrmont.de/category/hessisch-oldendorf-gesamt/",
    "screenshot_url": "http://green-spider-screenshots.sendung.de/360x640/4fc61b4918dc9eaaef645c694c84224e.png",
    "user_agent": "phantomjs-2.1.1",
    "size": [360, 640],
    "created": "2018-10-08T08:33:19.353841+00:00"
  }
]
```

## Konfiguration

Umgebungsvariablen:

- `GCLOUD_DATASTORE_CREDENTIALS_PATH`: Pfad der JSON-Datei mit Google Cloud Service-Account-Credentials. Benötigt lesenden Zugriff auf `spider-results` Datastore-Entitäten.
