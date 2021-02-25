from flask import jsonify


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


USER_NOT_FOUND = template(['User not found'], code=404)
USER_ALREADY_REGISTERED = template(['User already registered'], code=422)
SIGN_UP_DATA_IS_INVAlID = template(['The username must be more than 3 characters long and less than 33 characters long',
                                    'The password must be more than 7 characters long and less than 33 characters long'],
                                   code=400)
PARAMS_MISSED = template(['Parameters not defined, please add any params to your request'], code=400)
UNKNOWN_ERROR = template([], code=500)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def params_are_missed(cls):
        return cls(**PARAMS_MISSED)

    @classmethod
    def user_not_found(cls):
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls):
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def sign_up_data_is_invalid(cls):
        return cls(**SIGN_UP_DATA_IS_INVAlID)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)