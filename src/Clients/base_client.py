import requests
from requests import Response


class BaseClient:

    @staticmethod
    def custom_request(method, url, **kwargs) -> Response:
        with requests.Session() as session:
            request = requests.Request(method, url, **kwargs)
            prepped = session.prepare_request(request)
            response = session.send(prepped)
            return response
