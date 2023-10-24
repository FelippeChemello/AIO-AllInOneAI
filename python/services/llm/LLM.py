from abc import ABC, abstractmethod


class LLM(ABC):
    @abstractmethod
    def get_models(self):
        pass

    @abstractmethod
    def generate(self, messages, model_name):
        pass
