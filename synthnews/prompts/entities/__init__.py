from typing import TypedDict


class Entity(TypedDict):
    name: str
    entity_type: str
    country_or_region: str
    notes: str
