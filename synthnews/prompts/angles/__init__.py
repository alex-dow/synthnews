from typing import TypedDict


class Angle(TypedDict):
    id: str
    category: str
    angle: str
    focus: str
    questions: list[str]
