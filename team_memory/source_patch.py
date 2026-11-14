"""Compatibility import; implementation: team_memory.experiments.review.source_patch.

New code should import the implementation path directly.
"""
from importlib import import_module as _import_module
import sys as _sys

_implementation = _import_module("team_memory.experiments.review.source_patch")
_sys.modules[__name__] = _implementation
