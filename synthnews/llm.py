from time import perf_counter
from llama_cpp import Llama
from synthnews.logging import LOGGER
from synthnews.utils import format_seconds


def load_model(
    model_path: str,
    gpu_layers: int,
    context_size: int,
    batch_size: int,
    threads: int,
    verbose: bool,
    seed: int,
):
    started = perf_counter()
    LOGGER.info(f"Loading model from {model_path}")
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=gpu_layers,
        n_ctx=context_size,
        n_batch=batch_size,
        n_threads=threads,
        chat_format="chatml",
        verbose=verbose,
        seed=seed,
    )

    ended = perf_counter()
    LOGGER.info(f"Model loaded in {format_seconds(ended - started)}")
    return llm
