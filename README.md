[![Docker Repository on Quay](https://quay.io/repository/netzbegruenung/green-spider-api/status "Docker Repository on Quay")](https://quay.io/repository/netzbegruenung/green-spider-api)

# green-spider-api

Web service API für Green Spider

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

## Konfiguration

Umgebungsvariablen:

- `GCLOUD_DATASTORE_CREDENTIALS_PATH`: Pfad der JSON-Datei mit Google Cloud Service-Account-Credentials. Benötigt lesenden Zugriff auf `spider-results` Datastore-Entitäten.
