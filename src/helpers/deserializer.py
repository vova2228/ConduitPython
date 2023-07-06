from typing import Type, Any


class Deserializer:
    @classmethod
    def deserialize(cls, response_body: str, cls_to_deserialize: Type) -> Any:
        return cls_to_deserialize.from_dict(response_body)
