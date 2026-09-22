from __future__ import annotations

from dataclasses import dataclass

from xcodefy.library.schema.values.typed_string_wrapper import TypedStringWrapper

KNOWN_CAPABILITY_FOR_TESTING = "known capability for testing"


@dataclass(frozen=True, slots=True)
class Capability(TypedStringWrapper):
    @property
    def is_satisfied(self) -> bool:
        return self.raw_value in KNOWN_CAPABILITIES

    @classmethod
    def known_capability_for_testing(cls) -> Capability:
        return cls(KNOWN_CAPABILITY_FOR_TESTING)


KNOWN_CAPABILITIES = frozenset({KNOWN_CAPABILITY_FOR_TESTING})
