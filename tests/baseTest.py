from requests import JSONDecodeError


class BaseTest:

    @classmethod
    def check_status_code(cls, response, expected_status_code):
        assert response.status_code == expected_status_code, f"The status code of the response from the server = {response.status_code} instead of {expected_status_code}!!"

    @classmethod
    def check_response_is_json(cls, response):
        if response.text == "":
            print("Response body is empty")
        else:
            assert response.headers.get('Content-Type') == 'application/json; charset=utf-8', "Response is not in JSON format"
            try:
                response.json()
            except JSONDecodeError:
                print("Response is not in JSON format")
