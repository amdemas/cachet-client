"""Fake cachet api"""
import random
import string
import re
from requests.exceptions import HTTPError

from cachetclient.v1 import (
    Subscriber,
)


class FakeData:

    def __init__(self, routes):
        self.routes = routes
        self.data = []
        self.map = {}
        self.last_id = 0

    def add_entry(self, entry):
        """Add a data entry"""
        self.data.append(entry)
        self.map[entry['id']] = entry

    def delete_by_id(self, resource_id):
        """Delete a resource"""
        resource = self.map.get(int(resource_id))
        if not resource:
            raise HTTPError("404")

        del self.map[int(resource_id)]
        self.data.remove(resource)

    def next_id(self):
        """Generate unique instance id"""
        self.last_id += 1
        return self.last_id


class FakeSubscribers(FakeData):

    def get(self, params=None, **kwargs):
        """List only supported"""
        return self.data

    def post(self, params=None, data=None):
        instance = {
            "id": self.next_id(),
            "email": data['email'],
            "verify_code": ''.join(random.choice(string.ascii_lowercase) for i in range(16)),
            "verified_at": "2015-07-24 14:42:24",
            "created_at": "2015-07-24 14:42:24",
            "updated_at": "2015-07-24 14:42:24"
        }
        self.add_entry(instance)

    def delete(self, subscriber_id=None, **kwargs):
        self.delete_by_id(subscriber_id)


class FakeComponents(FakeData):
    def get(self):
        print("moo")


class FakePing(FakeData):
    def get(self, *args, **kwargs):
        return { "data": "Pong!" }


class FakeVersion(FakeData):

    def request(self, *args, **kwargs):
        return {
            "meta": {
                "on_latest": True,
                "latest": {
                    "tag_name": "v2.3.10",
                    "prelease": False,
                    "draft": False
                }
            },
            "data": "2.3.11-dev"
        }


class Routes:
    """Requesting routing"""

    def __init__(self):
        self.ping = FakePing(self)
        self.version = FakeVersion(self)
        self.components = FakeComponents(self)
        self.component_groups = None
        self.incidents = None
        self.incident_updates = None
        self.metrics = None
        self.metric_points = None
        self.subscribers = FakeSubscribers(self)

        self._routes = [
            (r'^ping', self.ping, ['get']),
            (r'^version', self.version, ['get']),
            (r'^component/groups/(?P<group_id>\w+)', self.components, ['get', 'post', 'delete']),
            (r'^component/groups', self.components, ['get', 'post']),
            (r'^components/(?P<component_id>\w+)', self.components, ['get', 'post', 'delete']),
            (r'^components', self.components, ['GET', 'POST']),
            (r'^incidents/(?P<incident_id>\w+)/updates/(?P<update_id>\w+)', ['get', 'post', 'delete']),
            (r'^incident/(?P<incident_id>\w+)/updates', self.incident_updates, ['get', 'post']),
            (r'^incidents', self.incidents, ['get', 'post']),
            (r'^metric/points', self.metric_points, ['get']),
            (r'^metrics', self.metrics, ['get']),
            (r'^subscribers/(?P<subscriber_id>\w+)', self.subscribers, ['delete']),
            (r'^subscribers', self.subscribers, ['get', 'post']),
        ]

    def dispatch(self, method, path, data=None, params=None):
        for route in self._routes:
            print(route[0], path, params, data)
            match = re.search(route[0], path)
            if not match:
                continue

            if method in route[2]:
                func = getattr(route[1], method, None)
                if func:
                    return func(params=params, data=data, **match.groupdict())

            raise ValueError("Method '{}' not allowed for '{}'".format(method, path))


class FakeHttpClient:
    """Fake implementation of the httpclient"""

    def __init__(self, base_url, api_token, timeout=None, verify_tls=True, user_agent=None):
        self.routes = Routes()
        self.base_url = base_url
        self.api_token = api_token
        self.timeout = timeout
        self.verify_tls = verify_tls
        self.user_agent = user_agent

    def get(self, path, params=None):
        return self.request('get', path, params=params)

    def post(self, path, data=None, params=None):
        return self.request('post', path, data=data, params=params)

    def delete(self, path):
        return self.request('delete', path)

    def request(self, method, path, params=None, data=None):
        return self.routes.dispatch(method, path, params=params, data=data)


if __name__ == '__main__':
    client = FakeHttpClient('http://status.example.com', 's4cr337k33y')
    client.post('subscribers', data={'email': 'user@example.com'})
    subs = client.get('subscribers')
    print("Subscribers:", subs)
    client.delete('subscribers/{}'.format(subs[0]['id']))
    print("Subscribers:", subs)