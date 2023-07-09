class SuccesfullRegistration:
    status_code = 200
    expected_keys = ["user", "email", "username", "bio", "image", "token"]


class RegistrationDataAlreadyBeenTaken:
    status_code = 422
    expected_text = '''{"errors":{"email":["has already been taken"],"username":["has already been taken"]}}'''


class SuccesfullLogin:
    status_code = 200
    expected_keys = ["user", "email", "username", "bio", "image", "token"]


class UserIsNotRegistered:
    status_code = 403
    expected_text = '''{"errors":{"email or password":["is invalid"]}}'''
