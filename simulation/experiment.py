import json
from dataclasses import dataclass, asdict
from .task.task import Task

@dataclass
class ExperimentRun:
    latency: float
    success: bool
    comment: str

    def __init__(self,
                 latency: float | None = None,
                 success: bool | None = None,
                 comment: str | None = None):
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

    def get_model(self) -> str:
        return self.model

    def write_to_file(self, path):
        with open(path, "a") as f:
            # asdict() seamlessly converts the dataclass to a dictionary
            json_str = json.dumps(asdict(self))
            f.write(json_str + "\n")