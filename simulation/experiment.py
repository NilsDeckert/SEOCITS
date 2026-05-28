from dataclasses import dataclass
from .task.task import Task

class ExperimentRun:
    latency: float
    success: bool
    comment: str

    def __init__(self, latency: float | None, success: bool | None, comment: str | None):
        self.latency = latency
        self.success = success
        self.comment = comment

    def add_latency(self, latency: float):
        self.latency = latency

    def add_success(self, success: bool):
        self.success = success

    def add_comment(self, comment: str):
        self.comment = comment

@dataclass
class ExperimentSetup:
    model: str
    task: Task
    runs: list[ExperimentRun]

    def record_run(self, run: ExperimentRun):
        self.runs.append(run)