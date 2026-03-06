![synthnews image](./synthnews.png)
# synthnews

An experiment in generating synthetic news articles using [llama.cpp](https://github.com/abetlen/llama-cpp-python).

## Installation

Requirements:

  - Python 3.11+
  - C Compiler
  - An LLM model in GGUF format
  - A GPU is highly recommended

For simple installation:

```bash
python -m venv .venv
pip install -r requirements.txt
```

To use NVIDIA CUDA
```bash
python -m venv .venv
CMAKE_ARGS="-DGGML_CUDA=on" pip install -r requirements.txt
```

## Theory of Operation

- Generate a large number of topics/angles/other hints to build a planning prompt
- Generate a number of "styles" of article writing to increase diversification
- Plan to generate an article related to the randomly selected hints
- Generate the article
- Compare the article to the entire corpus to see how similar the article is
- Skip the article it's too short or not diverse enough

## Article Planning

Each news topic has a list of relevant entities, angles, focuses, questions, and other hints that are used to create a plan for generating an article. 

There is also a list of article writing styles.

Each entity, angle, style, etc, are picked randomly to finally create a plan for creating the article.































