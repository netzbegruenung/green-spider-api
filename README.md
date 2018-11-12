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

### `GET /api/v1/spider-results/compact/`

Gibt die kompakte Liste aller Sites aus. Diese enthält nur die Details, die für eine Übersicht benötigt werden.

```json
[
  {
    "input_url": "https://www.gruenekoeln.de/bezirke/bezirk7.html",
    "created": "2018-10-31T01:21:03.361931+00:00",
    "meta": {
      "level": "DE:ORTSVERBAND",
      "state": "Nordrhein-Westfalen",
      "type": "REGIONAL_CHAPTER",
      "city": "Köln-Porz/Poll",
      "district": "Köln"
    },
    "score": 11.5
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
