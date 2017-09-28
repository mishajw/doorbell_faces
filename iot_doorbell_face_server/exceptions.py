from typing import Optional, Any


class ServerException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

    def to_json(self) -> str:
        return str({
            "status_code": self.status_code,
            "error_type": type(self).__name__,
            "message": self.message
        })


class IncorrectValueException(ServerException):
    def __init__(self, message: str):
        super().__init__(400, message)

    @classmethod
    def from_message(cls, message: str):
        return cls(message)

    @classmethod
    def from_value_and_explanation(cls, value_name: str, given_value: Any, explanation: Optional[str]):
        return cls("User provided \"%s\"=\"%s\", incorrect because %s" % (value_name, given_value, explanation))


class UnimplementedException(ServerException):
    def __init__(self):
        super().__init__(500, "This functionality is unimplemented")
