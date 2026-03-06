import argparse
import os
from pathlib import Path
import random
from time import perf_counter

from synthnews.exceptions import ModelNotFoundError
from synthnews.llm import load_model
from synthnews.logging import configure_logging, LOGGER
from synthnews.pipeline import PipelineConfig
from synthnews.pipeline.generators import generate_corpus
from synthnews.prompts import TOPICS
from synthnews.utils import format_seconds


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic news-style articles with a local GGUF model."
    )
    parser.add_argument("--model", required=True, help="Path to a local GGUF file.")
    parser.add_argument("--out", default="output", help="Output directory.")
    parser.add_argument(
        "--num-articles",
        type=int,
        default=25,
        help="Number of articles to create per topic.",
    )

    parser.add_argument(
        "--min-words",
        type=int,
        default=450,
        help="Minimum number of words per article.",
    )

    parser.add_argument(
        "--max-words",
        type=int,
        default=1240,
        help="Maximum number of words per article.",
    )

    parser.add_argument(
        "--min-entities",
        type=int,
        default=3,
        help="Minimum number of entities to use when planning an article.",
    )

    parser.add_argument(
        "--max-entities",
        type=int,
        default=5,
        help="Maximum number of entities to use when planning an article.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="If provided, will be the base seed used when randomally picking angles, entities, and other random choices",
    )

    parser.add_argument(
        "--sim-threshold",
        type=float,
        default=None,
        help="If provided, documents that score a similarity score (relative to the other documents in the same topic) above this threshold will be rejected. Don't set to ignore similarity",
    )

    parser.add_argument(
        "--context-size", type=int, default=4096, help="Context window to allocate."
    )
    parser.add_argument(
        "--batch-size", type=int, default=512, help="Prompt processing batch size."
    )
    parser.add_argument(
        "--threads", type=int, default=max(4, os.cpu_count() or 4), help="CPU threads."
    )

    parser.add_argument(
        "--gpu-layers",
        type=int,
        default=-1,
        help="-1 tries to offload all layers to GPU.",
    )
    parser.add_argument(
        "--plan-temperature",
        type=float,
        default=1.0,
        help="Temperature for the plan prompt.",
    )
    parser.add_argument(
        "--plan-top-p",
        type=float,
        default=0.95,
        help="Top-p for the plan prompt.",
    )
    parser.add_argument(
        "--plan-max-tokens",
        type=int,
        default=800,
        help="Maximum number of tokens for the plan prompt.",
    )
    parser.add_argument(
        "--max-article-retries",
        type=int,
        default=8,
        help="Retries for each article before failing.",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="Optional log file path.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable extra debug logging in the console. File logging is always verbose.",
    )
    return parser.parse_args()


def main() -> None:
    exit_code = 0
    started = perf_counter()

    args = parse_args()
    configure_logging(log_file=args.log_file, verbose=args.verbose)

    LOGGER.info("Synthnews v0.0.1")

    pipelineConfig: PipelineConfig = {
        "batchSize": args.batch_size,
        "contextSize": args.context_size,
        "minWords": args.min_words,
        "maxWords": args.max_words,
        "minEntities": args.min_entities,
        "maxEntities": args.max_entities,
        "maxArticleRetries": args.max_article_retries,
        "outputDir": Path(args.out),
        "numArticles": args.num_articles,
        "seed": args.seed,
        "planTemperature": args.plan_temperature,
        "planTopP": args.plan_top_p,
        "planMaxTokens": args.plan_max_tokens,
    }

    LOGGER.info(f"Pipeline config: {pipelineConfig}")

    if pipelineConfig["seed"] is not None:
        random.seed(pipelineConfig["seed"])

    try:
        if not os.path.exists(args.model):
            raise ModelNotFoundError(args.model)

        llm = load_model(
            model_path=args.model,
            batch_size=args.batch_size,
            context_size=args.context_size,
            gpu_layers=args.gpu_layers,
            threads=args.threads,
            verbose=args.verbose,
            seed=args.seed,
        )

        for topic in TOPICS:
            generate_corpus(topic, pipelineConfig, llm)

    except ModelNotFoundError as e:
        LOGGER.error(f"Model not found: {args.model}")
        exit_code = 1
    except Exception as e:
        LOGGER.fatal("Unknown error!")
        LOGGER.fatal(e, exc_info=True)
        exit_code = 1
    finally:
        ended = perf_counter()

        LOGGER.info(f"Corpus has been created in {format_seconds(ended - started)}")

        exit(exit_code)


if __name__ == "__main__":
    main()
