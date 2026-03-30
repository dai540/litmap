from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PipelineStep:
    name: str
    purpose: str
    outputs: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RunResult:
    run_id: str
    run_path: str
    summary: str
    steps: list[PipelineStep] = field(default_factory=list)
