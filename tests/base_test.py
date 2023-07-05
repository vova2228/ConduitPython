from requests import Response


class BaseTest:
    def __init__(self, response: Response):
        self.response = response

    def check_response_is_correct(self):
        self._check_status_code()
        self._check_response_is_json()

    def _check_status_code(self):
        assert self.response.status_code == 200, f"Status is code is not 200. It is {self.response.status_code}"

    def _check_response_is_json(self):
        assert self.response.headers.get('Content-Type') == 'application/json; charset=utf-8', "Response is not in JSON format"
