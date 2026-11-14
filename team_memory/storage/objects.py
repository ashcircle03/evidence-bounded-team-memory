"""Canonical storage entry point; the original file is a frozen hash anchor.

Historical dataset manifests bind team_memory/store.py byte-for-byte. Import
that one implementation instead of duplicating it or changing those manifests.
"""
from importlib import import_module as _import_module
import sys as _sys

_sys.modules[__name__] = _import_module("team_memory.store")
