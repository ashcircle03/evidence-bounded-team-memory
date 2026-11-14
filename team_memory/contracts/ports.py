"""Transport-independent ports. JSON objects cross module boundaries."""

from dataclasses import dataclass
from typing import Any, Protocol

VERSION = "team-memory.modules/v1"
MODULES = ("records", "relations", "retrieval", "answering", "gateway")


@dataclass(frozen=True)
class CallContext:
    """Trusted caller context, constructed by the transport authenticator.

    Never deserialize this from untrusted request JSON. Capability checks and
    ownership checks belong to the receiving port, including records itself.
    This value represents authenticated identity; it does not authenticate it.
    """

    workspace_id: str
    principal_id: str
    capabilities: frozenset[str]


class Port(Protocol):
    def handle(self, request: dict[str, Any], *, context: CallContext) -> dict[str, Any]:
        """Return a versioned response; do not mutate the request object."""
        ...


class RecordsPort(Port, Protocol):
    """record.append, proposal.submit, review.apply, snapshot.get."""


class RelationsPort(Port, Protocol):
    """relations.compare: read-only pair comparison over a fixed snapshot."""


class RetrievalPort(Port, Protocol):
    """evidence.retrieve: read-only retrieval with provenance and state."""


class AnsweringPort(Port, Protocol):
    """answer.generate: claim-level answers over an immutable evidence bundle."""


class GatewayPort(Port, Protocol):
    """gateway.ask, gateway.ingest, gateway.review: authenticated orchestration."""
