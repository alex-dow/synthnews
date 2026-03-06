from typing import TypedDict
from synthnews.prompts.angles.crime_and_law import ANGLES as CRIME_AND_LAW_ANGLES
from synthnews.prompts.angles.economy_and_business import (
    ANGLES as ECONOMY_AND_BUSINESS_ANGLES,
)
from synthnews.prompts.angles.entertainment import ANGLES as ENTERTAINMENT_ANGLES
from synthnews.prompts.angles.politics import ANGLES as POLITICS_ANGLES
from synthnews.prompts.angles.science_and_technology import (
    ANGLES as SCIENCE_AND_TECHNOLOGY_ANGLES,
)
from synthnews.prompts.angles.sports import ANGLES as SPORTS_ANGLES

from synthnews.prompts.entities import Entity
from synthnews.prompts.entities.crime_and_law import ENTITIES as CRIME_AND_LAW_ENTITIES
from synthnews.prompts.entities.economy_and_business import (
    ENTITIES as ECONOMY_AND_BUSINESS_ENTITIES,
)
from synthnews.prompts.entities.entertainment import ENTITIES as ENTERTAINMENT_ENTITIES
from synthnews.prompts.entities.politics import ENTITIES as POLITICS_ENTITIES
from synthnews.prompts.entities.science_and_technology import (
    ENTITIES as SCIENCE_AND_TECHNOLOGY_ENTITIES,
)
from synthnews.prompts.entities.sports import ENTITIES as SPORTS_ENTITIES


TOPICS = [
    "crime_and_law",
    "economy_and_business",
    "entertainment",
    "politics",
    "science_and_technology",
    "sports",
]

ARTICLE_STYLES = [
    "straight wire report",
    "market wrap style",
    "campaign trail dispatch",
    "breaking-news update",
    "analysis-led news report",
    "city desk report",
    "international desk report",
    "sports desk gamer",
    "investigative journalism",
]

ANGLES = {
    "crime_and_law": CRIME_AND_LAW_ANGLES,
    "economy_and_business": ECONOMY_AND_BUSINESS_ANGLES,
    "entertainment": ENTERTAINMENT_ANGLES,
    "politics": POLITICS_ANGLES,
    "science_and_technology": SCIENCE_AND_TECHNOLOGY_ANGLES,
    "sports": SPORTS_ANGLES,
}

ENTITIES = {
    "crime_and_law": CRIME_AND_LAW_ENTITIES,
    "economy_and_business": ECONOMY_AND_BUSINESS_ENTITIES,
    "entertainment": ENTERTAINMENT_ENTITIES,
    "politics": POLITICS_ENTITIES,
    "science_and_technology": SCIENCE_AND_TECHNOLOGY_ENTITIES,
    "sports": SPORTS_ENTITIES,
}

SYSTEM_PROMPT = """You write synthetic news-style articles for internal testing.
Requirements:
- Write in a neutral, professional news tone.
- Use a realistic headline, optional one-line dek, a dateline, and then 5 to 10 paragraphs.
- Use real institutions, locations, leagues, teams, companies, agencies, and public bodies when appropriate.
- Use the names of real politicians, celebrities, and scientists.
- Do NOT impersonate a real outlet or claim the article was published by a real newsroom.
- Do NOT invent direct quotes from real living people.
- Avoid obviously impossible facts, magic, sci-fi, or satire.
- Output only the requested JSON or article text, with no notes or disclaimers.
"""


class ArticleConfig(TypedDict):
    topic: str
    headline: str
    entities: list[Entity]
    style: str


class TopicConfig:
    def __init__(self, topic: str, angle: str, entities: list[str], style: str):
        self.topic = topic
        self.angle = angle
        self.entities = entities
        self.style = style
