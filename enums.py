from enum import Enum


class City(Enum):
    BOS = "bos"
    JNU = "jnu"
    MIA = "mia"

    @classmethod
    def from_string(cls, input_city: str):
        try:
            return cls(input_city)
        except ValueError:
            raise ValueError(
                f"Invalid input ({input_city}). Please choose from: {[c.value for c in cls]}"
            )

    @property
    def full_name(self) -> str:
        mapping = {City.BOS: "boston", City.JNU: "juneau", City.MIA: "miami"}
        return mapping[self]
