#!/usr/bin/env python
import argparse
import requests
import json


class ArgumentParser(object):

    def __init__(self):
        self._params = []
        self._parse_arguments()

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = value

    def _parse_arguments(self):
        parser = argparse.ArgumentParser(description='Small utility for calling some rest services and saving the result.')
        parser.add_argument('params', type=str, action='store', help='List of comma separated parameters.')
        args = parser.parse_args()
        self.params = [p.strip() for p in args.params.split(',')]


class RestRequest(object):

    def __init__(self, url, filename):
        self._url = url
        self._filename = filename
        self._request = None

    @property
    def request(self):
        return self._request

    @property
    def filename(self):
        return self._filename

    def process(self):
        try:
            print('Calling ' + self._url + '...')
            self._request = requests.get(self._url)
            return self
        except Exception, e:
            print(e)


class RequestManager(object):

    def __init__(self):
        self._result = []
        self._requests = []

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result.append(value)

    @property
    def requests(self):
        return self._requests

    @requests.setter
    def requests(self, value):
        self._requests.append(value)
        
    def process(self):
        for request in self._requests:
            self._result.append(request.process())


class FileSaver(object):

    def __init__(self, result):
        self._result = result

    def save(self):
        try:
            for r in self._result:
                with open(r.filename, 'w') as f:
                    parsed_json = json.loads(r.request.text)
                    f.write(json.dumps(parsed_json, indent=4, sort_keys=False))
        except Exception, e:
            print(e)


def main():
    parser = ArgumentParser()
    request_manager = RequestManager()

    for param in parser.params:
        url = 'Put your URL here' + param
        filename = ''.join(['document-', param, '.json'])
        request_manager.requests = RestRequest(url, filename)

    request_manager.process()

    file_saver = FileSaver(request_manager.result)
    file_saver.save()


if __name__ == '__main__':
    main()
