from abc import ABC, abstractmethod


class TTS(ABC):
    @abstractmethod
    def get_voices(self):
        pass

    @abstractmethod
    def synthesize(self, text, voice):
        pass
