from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BaseSource:
    name: str
    description: str

    def blueprint(self) -> dict[str, str]:
        return {"name": self.name, "description": self.description}
