import collections
from datetime import datetime
from os import getenv
from wsgiref import simple_server

import falcon
from falcon import media
import jsonhandler

from google.cloud import datastore


credentials_path = getenv('GCLOUD_DATASTORE_CREDENTIALS_PATH')
datastore_client = datastore.Client.from_service_account_json(credentials_path)

spider_results_kind = 'spider-results'
webscreenshots_kind = 'webscreenshot'


def convert_datastore_datetime(field):
    """
    return datetime in different ways, depending on whether the lib returns
    a str, int, or datetime.datetime
    """
    dt = ''
    if type(field) == datetime:
        dt = field
    elif type(field) == int:
        dt = datetime.utcfromtimestamp(field / 1000000)
    elif type(field) == str:
        dt = datetime.utcfromtimestamp(int(field) / 1000000)
    return dt


def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_compact_results(client):
    query = client.query(kind=spider_results_kind,
                         order=['-created'],
                         #projection=['created', 'meta', 'score'],
                         )

    out = []
    for entity in query.fetch(eventual=True):
        created = convert_datastore_datetime(entity.get('created'))
        
        out.append({
            'input_url': entity.key.name,
            'created': created.isoformat(),
            'meta': entity.get('meta'),
            'score': entity.get('score'),
        })
    return out


def get_full_results(client):
    query = client.query(kind=spider_results_kind)

    out = []
    for entity in query.fetch(eventual=True):
        created = convert_datastore_datetime(entity.get('created'))

        record = {
            'input_url': entity.key.name,
            'created': created.isoformat(),
            'score': entity.get('score'),
        }
        record.update(flatten(entity.get('meta'), parent_key='meta'))
        record.update(flatten(entity.get('rating'), parent_key='rating'))
        out.append(record)
    return out


class LastUpdated(object):

    def on_get(self, req, resp):
        """
        Informs about the most recent update to the spider results data
        """
        query = datastore_client.query(kind=spider_results_kind,
                                       order=['-created'],
                                       projection=['created'])
        items = list(query.fetch(limit=1, eventual=True))
        ts = int(items[0].get('created')) / 1000000
        dt = datetime.utcfromtimestamp(ts).isoformat()

        maxage = 60 * 60  # one hour in seconds
        resp.cache_control = ["max_age=%d" % maxage]
        resp.media = {
            "last_updated": dt
        }


class CompactResults(object):

    def on_get(self, req, resp):
        """
        Returns compact sites overview and score
        """
        out = get_compact_results(datastore_client)

        maxage = 6 * 60 * 60  # six hours in seconds
        resp.cache_control = ["max_age=%d" % maxage]
        resp.media = out


class BigResults(object):

    def on_get(self, req, resp):
        """
        Returns big sites results
        """
        out = get_full_results(datastore_client)

        maxage = 48 * 60 * 60  # two days
        resp.cache_control = ["max_age=%d" % maxage]
        resp.media = out


class SiteDetails(object):

    def on_get(self, req, resp):
        """
        Returns details for one URL
        """

        url = req.get_param('url')
        if url is None or url == '':
            raise falcon.HTTPError(falcon.HTTP_400,
                               'Bad request',
                               'The parameter url must not be empty')

        key = datastore_client.key(spider_results_kind, req.get_param('url'))
        entity = datastore_client.get(key)
        if entity is None:
            raise falcon.HTTPError(falcon.HTTP_404,
                               'Not found',
                               'A site with this URL does not exist')

        maxage = 24 * 60 * 60  # 24 hours in seconds
        resp.cache_control = ["max_age=%d" % maxage]
        resp.media = dict(entity)


class SiteScreenshots(object):

    def on_get(self, req, resp):
        """
        Returns screenshots for one URL
        """

        url = req.get_param('url')
        if url is None or url == '':
            raise falcon.HTTPError(falcon.HTTP_400,
                               'Bad request',
                               'The parameter url must not be empty')

        query = datastore_client.query(kind=webscreenshots_kind)
        query.add_filter('url', '=', req.get_param('url'))
        entities = list(query.fetch())

        maxage = 24 * 60 * 60  # 24 hours in seconds
        if len(entities) == 0:
            maxage = 3 * 60 * 60  # 3 hours in seconds

        resp.cache_control = ["max_age=%d" % maxage]
        resp.media = entities


class Index(object):
    def on_get(self, req, resp):
        resp.media = {
            "message": "This is green-spider-api",
            "url": "https://github.com/netzbegruenung/green-spider-api",
            "endpoints": [
                "/api/v1/spider-results/last-updated/",
                "/api/v1/spider-results/big/",
                "/api/v1/spider-results/compact/",
                "/api/v1/spider-results/site",
                "/api/v1/screenshots/site",
            ]
        }

handlers = media.Handlers({
    'application/json': jsonhandler.JSONHandler(),
})

app = falcon.API()

app.req_options.media_handlers = handlers
app.resp_options.media_handlers = handlers

app.add_route('/api/v1/spider-results/last-updated/', LastUpdated())
app.add_route('/api/v1/spider-results/compact/', CompactResults())
app.add_route('/api/v1/spider-results/big/', BigResults())
app.add_route('/api/v1/spider-results/site', SiteDetails())
app.add_route('/api/v1/screenshots/site', SiteScreenshots())
app.add_route('/', Index())


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 5000, app)
    httpd.serve_forever()
