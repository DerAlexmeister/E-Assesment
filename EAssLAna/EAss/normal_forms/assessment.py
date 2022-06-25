from abc import ABC, abstractmethod

from .normal_form import Guess

class Assessment(ABC):
    @abstractmethod
    def assess(self, guess: Guess) -> str:
        pass

class BooleanAssessment(Assessment):
    def assess(self, guess: Guess) -> str:
        pass
