import json

class BaseTest:
    def check_response_is_correct(self, response):
        self._check_status_code(response)
        self.check_response_is_json(response)

    def _check_status_code(self, response):
        assert response.status_code == 200, f"Status is code is not 200. It is {response.status_code}"

    def check_response_is_json(self, response):
        assert response.headers.get('Content-Type') == 'application/json; charset=utf-8', "Response is not in JSON format"
        try:
            json.loads(response.text)
        except ValueError:
            assert False, "Response body is not valid JSON format"
