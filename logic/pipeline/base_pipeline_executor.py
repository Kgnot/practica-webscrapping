from abc import ABC, abstractmethod


class BasePipelineExecutor(ABC):
    def run(self):
        self.initialize_resources()
        global_context = self.load_global_context()
        self.process_all_contexts(global_context)

    @abstractmethod
    def initialize_resources(self):
        pass

    @abstractmethod
    def load_global_context(self):
        pass

    @abstractmethod
    def process_all_contexts(self, global_context):
        pass
