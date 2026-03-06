from pathlib import Path
from typing import TypedDict

from synthnews.prompts.angles import Angle
from synthnews.prompts.entities import Entity


class Plan(TypedDict):
    headline: str
    section_label: str
    style: str
    dateline: str
    news_hook: str
    angle: str
    named_entities: list[str]
    fictional_people: list[str]
    story_facts: list[str]
    target_words: int


class PipelineConfig(TypedDict):
    numArticles: str
    maxArticleRetries: int
    outputDir: Path
    minWords: int
    maxWords: int
    minEntities: int
    maxEntities: int
    contextSize: int
    batchSize: int
    seed: int | None
    planTemperature: float
    planTopP: float
    planMaxTokens: int


class Article(TypedDict):
    id: str
    index: int
    topic: str
    angle: Angle
    entities: list[Entity]
    style: str
    attempts: int
    text: str
    rejectedReasons: list[str]
    accepted: bool
    similarity: float
    targetWords: int
