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
]

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


class TopicConfig:
    def __init__(self, topic: str, angle: str, entities: list[str], style: str):
        self.topic = topic
        self.angle = angle
        self.entities = entities
        self.style = style
