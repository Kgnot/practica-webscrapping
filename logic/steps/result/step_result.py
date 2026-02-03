from enum import Enum


class StepResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    SKIP = "skip"
