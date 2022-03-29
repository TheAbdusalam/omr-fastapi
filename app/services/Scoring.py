from typing import Optional


class Scoring:
    def __init__(
        self, correct_answers: float, questions: int, weight: Optional[float] = 1
    ):
        # validate before assigning
        assert (
            questions != 0 and correct_answers != None
        ), "questions and correct_answers cannot be 0"

        self.correct = correct_answers
        self.questions = questions
        self.weight = weight

    @property
    def percentage(self) -> None:
        """return the percentage of correct answers"""
        self.correct = str((self.correct / self.questions) * 100) + "%"
        self.questions = str(100.0) + "%"

    @property
    def weight(self) -> None:
        """return the mark of correct answers based on the given weight of each answer"""
        self.correct = self.correct * self.weight
        self.questions = self.questions * self.weight

    def __repr__(self) -> str:
        return f"{self.correct} / {self.questions}"
