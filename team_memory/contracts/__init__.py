"""Versioned collaboration contracts, not a replacement for service v2.

Importing the ports needs only the standard library. Schema validation requires
the optional ``contracts`` extra. No model, authentication or storage is started.
"""

from .ports import CallContext, Port, VERSION

__all__ = ["CallContext", "Port", "VERSION"]
