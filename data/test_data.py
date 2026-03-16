class StatusCodes:

    SUCCESS = 200
    FORBIDDEN = 403
    BAD_REQUEST = 400
    NOT_FOUND = 404


class ErrorMessages:

    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS_MISSING = "Email, password and name are required fields"
    INVALID_CREDENTIALS = "email or password are incorrect"


class ResponseFields:

    SUCCESS = "success"
    ACCESS_TOKEN = "accessToken"
    MESSAGE = "message"
    USER = "user"


class TestData:


    SUCCESS_STATUS = StatusCodes.SUCCESS
    FORBIDDEN_STATUS = StatusCodes.FORBIDDEN


    USER_ALREADY_EXISTS = ErrorMessages.USER_ALREADY_EXISTS
    REQUIRED_FIELDS_MISSING = ErrorMessages.REQUIRED_FIELDS_MISSING


    EMPTY_PASSWORD = ""
    EMPTY_NAME = ""
    EMPTY_EMAIL = ""

def generate_user_data():
    return {
        'name': generate_name(),
        'email': generate_unique_email(),
        'password': generate_password()
    }
def get_static_user_data():
    return {
        'name': 'TestUser',
        'email': 'test@example.com',
        'password': 'Password123!'
    }