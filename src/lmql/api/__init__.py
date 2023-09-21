"""
LMQL API is a set of library functions that can be used to access some of the core
functionality of LMQL without actually writing any LMQL code.
"""

from typing import Union, Optional
import asyncio

from .llm import LLM, set_default_model, get_default_model

from .queries import query, F, query_from_string
from .run import run_file, run_sync, run
from .scoring import ScoringResult

async def generate(prompt: str, max_tokens: int, model: Optional[Union[LLM, str]] = None, **kwargs):
    """
    Generates up to max_tokens tokens of text from the given model, using the given prompt.

    If model is None, the default model will be used.
    """
    model = LLM.from_descriptor(model)
    return await model.generate(prompt, max_tokens, **kwargs)

def generate_sync(prompt: str, max_tokens: int, model=None, **kwargs):
    """
    Generates up to max_tokens tokens of text from the given model, using the given prompt.

    Like generate(), but runs synchronously and thus cannot be parallelized with other async code.
    When in an async context, use generate() instead.
    """
    return asyncio.run(generate(prompt, max_tokens, model, **kwargs))

async def score(prompt, values, *args, model: Optional[Union[str, LLM]] = None, **kwargs) -> ScoringResult:
    """
    Returns a ScoringResult object containing the score of the given prompt concatenated with each of the given values.
    """
    model = LLM.from_descriptor(model)
    return await model.score(prompt, values, *args, **kwargs)

def score_sync(prompt, values, *args, model=None, **kwargs) -> ScoringResult:
    """
    Like score(), but runs synchronously and thus cannot be parallelized with other async code.
    When in an async context, use score() instead.
    """
    return asyncio.run(score(prompt, values, *args, model=model, **kwargs))