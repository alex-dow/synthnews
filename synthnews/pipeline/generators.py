import json
import os
import random
from time import perf_counter
from llama_cpp import Llama
from synthnews.enums import DocumentRejectionReason
from synthnews.exceptions import InvalidPlanError, TopicNotFoundError
from synthnews.logging import LOGGER
from synthnews.pipeline import Article, PipelineConfig, Plan
from synthnews.prompts import ANGLES, ARTICLE_STYLES, ENTITIES, SYSTEM_PROMPT
from synthnews.prompts.builders import build_plan_prompt
from synthnews.utils import format_seconds


def verify_plan(planText: str) -> Plan:
    """
    Verifies if a generated plan is valid.

    If the plan is invalid an InvalidPlanError is raised, otherwise the plan is returned as
    a Plan dictionary.
    """
    try:
        plan = json.loads(planText)
        if not isinstance(plan, dict):
            raise InvalidPlanError("The plan is not a dictionary.", planText)
        if "headline" not in plan:
            raise InvalidPlanError("The plan does not have a headline.", planText)
        if "story_facts" not in plan:
            raise InvalidPlanError("The plan does not have story facts.", planText)
        if "section_label" not in plan:
            raise InvalidPlanError("The plan does not have a section label.", planText)
        if "style" not in plan:
            raise InvalidPlanError("The plan does not have a style.", planText)
        if "dateline" not in plan:
            raise InvalidPlanError("The plan does not have a dateline.", planText)
        if "news_hook" not in plan:
            raise InvalidPlanError("The plan does not have a news hook.", planText)
        if "angle" not in plan:
            raise InvalidPlanError("The plan does not have an angle.", planText)
        if "named_entities" not in plan:
            raise InvalidPlanError("The plan does not have named entities.", planText)
        if "fictional_people" not in plan:
            raise InvalidPlanError("The plan does not have fictional people.", planText)
        if "story_facts" not in plan:
            raise InvalidPlanError("The plan does not have story facts.", planText)
        if "target_words" not in plan:
            raise InvalidPlanError("The plan does not have a target words.", planText)
        return plan
    except json.JSONDecodeError:
        raise InvalidPlanError("The plan is not valid JSON.", planText)


def generate_plan(article: Article, config: PipelineConfig, llm: Llama) -> Plan:
    """
    Generates a plan for a given article.
    """
    started = perf_counter()

    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_plan_prompt(article),
            },
        ],
        response_format={"type": "json_object"},
        temperature=config["planTemperature"],
        top_p=config["planTopP"],
        max_tokens=config["planMaxTokens"],
    )

    ended = perf_counter()
    LOGGER.info(
        f"|{article['topic']}| Article [{article['index'] + 1}/{config['numArticles']}] Plan generated in {format_seconds(ended - started)}"
    )

    text = response["choices"][0]["message"]["content"]
    LOGGER.info(
        f"|{article['topic']}| Article [{article['index'] + 1}/{config['numArticles']}] Plan: {text}"
    )

    try:
        return verify_plan(text)
    except InvalidPlanError as e:
        LOGGER.error(
            f"|{article['topic']}| Article [{article['index'] + 1}/{config['numArticles']}] Plan is invalid: {e.message}"
        )
        raise e


def new_article(topic: str, config: PipelineConfig, idx: int):
    """
    Create a new Article dictionary for a given topic. Will populate the article with random data
    """
    if not ANGLES[topic]:
        raise TopicNotFoundError(topic, f"No angles found for topic: {topic}")

    if not ENTITIES[topic]:
        raise TopicNotFoundError(topic, f"No entities found for topic: {topic}")

    numEntities = random.randint(config["minEntities"], config["maxEntities"])
    entities = random.sample(ENTITIES[topic], k=numEntities)

    angle = random.choice(ANGLES[topic])

    article: Article = {
        "topic": topic,
        "angle": angle,
        "entities": entities,
        "style": random.choice(ARTICLE_STYLES),
        "attempts": 0,
        "rejectedReasons": [],
        "targetWords": random.randint(config["minWords"], config["maxWords"]),
        "index": idx,
    }

    return article


def generate_corpus(topic: str, config: PipelineConfig, llm: Llama):
    """
    Generates a corpus of articles for a given topic.
    """
    started = perf_counter()
    LOGGER.info(f"|{topic}| Generating corpus for topic")

    topicPath = os.path.join(config["outputDir"], topic)
    os.makedirs(topicPath, exist_ok=True)
    LOGGER.info(f"|{topic}| Topic directory created: {topicPath}")

    for i in range(config["numArticles"]):
        article = new_article(topic, config, i + 1)

        for attempt in range(config["maxArticleRetries"]):
            article["attempts"] += 1
            try:
                LOGGER.info(
                    f"|{topic}| Article [{i + 1}/{config['numArticles']}] angle={
                        article['angle']['angle']
                    } - entities={
                        ', '.join(map(lambda e: e['name'], article['entities']))
                    }  - style={article['style']} - targetWords={
                        article['targetWords']
                    }"
                )

                planText = generate_plan(article, config, llm)
            except InvalidPlanError as e:
                LOGGER.warning(
                    f"|{topic}| Article [{i + 1}/{config['numArticles']}] Plan is invalid: {e.message}"
                )
                article["rejectedReasons"].append(DocumentRejectionReason.INVALID_PLAN)
                continue
            except Exception as e:
                LOGGER.warning(
                    f"|{topic}| Article [{i + 1}/{config['numArticles']}] Unknown error: {e.message}"
                )
                article["rejectedReasons"].append(DocumentRejectionReason.UNKNOWN_ERROR)
                continue

    ended = perf_counter()
    LOGGER.info(f"|{topic}| Corpus generated in {format_seconds(ended - started)}")
