from typing import Type, Any


class Deserializer:

    """
    Deserializes JSON response bodies into Python objects.

    """

    @classmethod
    def deserialize(cls, response_body: str, cls_to_deserialize: Type) -> Any:
        return cls_to_deserialize.from_dict(response_body)
