import os
import json

import pytest
import requests_cache
import requests
from jsonschema import validate

TEST_URL = 'https://jsonplaceholder.typicode.com/users'
TEST_URL_NOT_FOUND = 'https://jsonplaceholder.typicode.com/user/0'
TEST_URL_SINGLE_RECORD = 'http://jsonplaceholder.typicode.com/users/10'

SCHEMA = {
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'name': {'type': 'string'},
        'username': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},

        'address': {
            'type': 'object',
            'properties': {
                'street': {'type': 'string'},
                'suite': {'type': 'string'},
                'city': {'type': 'string'},
                'zipcode': {'type': 'string',
                            'pattern': r'^([0-9]{5})?(\-?[0-9]{4})?$'},

                'geo': {
                    'type': 'object',
                    'properties': {
                        'lat': {'type': 'string',
                                'pattern': r'^-?([0-9]{1,3})\.([0-9]{4})$'},
                        'lng': {'type': 'string',
                                'pattern': r'^-?([0-9]{1,3})\.([0-9]{4})$'},
                    },
                },
            },
        },

        'phone': {'type': 'string', 'format': 'phone'},
        'website': {'type': 'string', 'format': 'hostname'},

        'company': {
            'type': 'object',
            'properties': {
                    'name': {'type': 'string'},
                    'catchPhrase': {'type': 'string'},
                    'bs': {'type': 'string'},
            }
        }



    },
}


class Test2:
    """Test for ex. 2."""

    def test_url(self):
        """Test normal flow."""
        # with requests_cache.CachedSession() as sess:
        with requests.Session() as sess:

            req = sess.get(TEST_URL)
            data = json.loads(req.text)

            # check response code is 200 - OK
            assert req.status_code == 200

            # check response has 10 JSON objects
            assert len(data) == 10

            # check jsonschema validation
            for obj in data:
                assert isinstance(validate(instance=obj, schema=SCHEMA),
                                  type(None))

    def test_url_not_found(self):
        """Attempt to simulate negative test."""
        with requests.Session() as sess:
            req = sess.get(TEST_URL_NOT_FOUND)

            # check response code is 404 - not found
            assert req.status_code == 404

            # check for empty data
            assert req.text == '{}'

    def test_url_single_record(self):
        """Some test for detail api url."""
        with requests.Session() as sess:
            req = sess.get(TEST_URL_SINGLE_RECORD)
            data = json.loads(req.text)

            # check response code is 200
            assert req.status_code == 200

            # check for answer contain single valid record
            assert isinstance(data, dict)
            assert isinstance(
                validate(instance=data, schema=SCHEMA), type(None))


if __name__ == '__main__':
    pytest.main([os.path.abspath(__file__), '-m', 'not documentation'])
