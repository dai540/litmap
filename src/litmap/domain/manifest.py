from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ArtifactRecord:
    key: str
    path: str
    description: str


@dataclass(slots=True)
class RunManifest:
    run_id: str
    project_name: str
    source_type: str
    artifact_records: list[ArtifactRecord] = field(default_factory=list)

    def add(self, key: str, path: str, description: str) -> None:
        self.artifact_records.append(ArtifactRecord(key=key, path=path, description=description))
