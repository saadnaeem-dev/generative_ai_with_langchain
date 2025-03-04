# Chapter 3 - Getting Started with LangChain

Please make sure, you set up your environment with pip, conda, poetry, or docker!

You can set up the keys for the different providers with a `config.py` like this:
```python
import os

def set_environment():
    os.environ["OPENAI_API_KEY"] = "... "  # <- this has to be your api key!
    # I'm omitting all other keys
```

You can subsequently set all these keys for LangChain importing and executing the `set_environment()` function in your projects or notebooks:
```python
from config import set_environment
set_environment()
```


| Section	| File | Colab	 | Kaggle	| Gradient |
|-----------|--------|--------|-----------|----------|
| Intro to LangGraph |  [notebook](langgraph_intro.ipynb)   |        | | |
| Output parsers |  [notebook](output_parsers.ipynb.ipynb)   |        | | |
| Error handling | [notebook](error_handling.ipynb)  |        | | |
| Prompt templates | [notebook](prompt-templates.ipynb)     |        | | |
| Multimodaliry | [notebook](multimodality.ipynb)   |        | | |
| Tracking costs |  [notebook](tracking_costs.ipynb)  |        | | |


