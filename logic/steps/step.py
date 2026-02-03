from abc import ABC, abstractmethod

from logic.steps.result.step_result import StepResult


class Step(ABC):

    @abstractmethod
    def run(self, ctx) -> StepResult:
        pass
