from typing import Any, Dict, List, Optional, Set, Tuple
import random
import os
from datetime import datetime

from synthnews.prompts import TOPICS


def build_article_config(topic: str):
    if topic not in TOPICS:
        raise ValueError(f"Invalid topic: {topic}")
    pass


def build_plan_prompt(
    topic: str, config: Dict[str, List[str]], publication_dt: datetime
) -> str:
    angle = random.choice(config["angles"])
    entities = sample_entities(config, k=4)
    style = random.choice(config["styles"])
    approx_words = random.choice([450, 550, 650, 750, 900])
    topic_label = topic.replace("_", " & ")
    pub_date = (
        publication_dt.strftime("%B %-d, %Y")
        if os.name != "nt"
        else publication_dt.strftime("%B %#d, %Y")
    )

    extra = ""

    return f"""
Create a JSON object for one synthetic {topic_label} article plan.

Constraints:
- Central angle: {angle}
- Writing style: {style}
- Use at least 3 of these real entities naturally if relevant: {entities}
- Target article length: about {approx_words} words
- Treat the article as if it were published on: {pub_date}
- The event itself can be fictional, but it must feel plausible.
- Avoid repeating common stock phrases.
- {extra}

Return a JSON object with these keys:
headline: string
section_label: string
style: string
dek: string
dateline: string
news_hook: string
angle: string
named_entities: array of strings
fictional_people: array of strings
story_facts: array of 6 to 10 concise bullet-like strings
target_words: integer
""".strip()
