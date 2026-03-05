import argparse
import os


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic news-style articles with a local GGUF model."
    )
    parser.add_argument("--model", required=True, help="Path to a local GGUF file.")
    parser.add_argument("--out", default="synthetic_news", help="Output directory.")
    parser.add_argument(
        "--per-topic", type=int, default=25, help="Target article count for each topic."
    )

    parser.add_argument(
        "--n-ctx", type=int, default=4096, help="Context window to allocate."
    )
    parser.add_argument(
        "--n-batch", type=int, default=512, help="Prompt processing batch size."
    )
    parser.add_argument(
        "--threads", type=int, default=max(4, os.cpu_count() or 4), help="CPU threads."
    )
    parser.add_argument("--seed", type=int, default=42, help="Base RNG seed.")
    parser.add_argument(
        "--gpu-layers",
        type=int,
        default=-1,
        help="-1 tries to offload all layers to GPU.",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=8,
        help="Retries for each article before failing.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume using an existing manifest.json in the output directory.",
    )
    parser.add_argument(
        "--date-start",
        default="2021-01-01",
        help="Random publication date lower bound (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--date-end",
        default="2025-12-31",
        help="Random publication date upper bound (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--topic-seeds-dir",
        default=None,
        help="Optional directory of per-topic JSON overrides like politics.json or sports.json.",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="Optional log file path. Defaults to <out>/generation.log.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable extra debug logging in the console. File logging is always verbose.",
    )
    return parser.parse_args()
