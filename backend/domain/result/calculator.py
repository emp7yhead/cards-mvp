from typing import Protocol

from backend.domain.result.entities import Result
from backend.domain.session.value_objects import Answers, Preference


class ResultCalculator(Protocol):
    def calculate(self, answers_1: Answers, answers_2: Answers) -> Result: ...


class SimpleResultsCalculator:
    def _is_common(self, preference_1: Preference, preference_2: Preference):
        is_neutral = preference_1 == Preference.NEUTRAL
        return preference_1 == preference_2 and not is_neutral

    def _get_score(self, common: list, answers_1: Answers, answers_2: Answers):
        total = len(answers_1.keys() & answers_2.keys())
        if total == 0:
            return 0
        return round(len(common) / total * 100)

    def calculate(self, answers_1: Answers, answers_2: Answers) -> Result:
        common = []
        difference = []

        for question_id in answers_1.keys() & answers_2.keys():
            answer_1 = answers_1[question_id]
            answer_2 = answers_2[question_id]

            if self._is_common(answer_1, answer_2):
                common.append(question_id)
            else:
                difference.append(question_id)

        score = self._get_score(
            common,
            answers_1,
            answers_2,
        )
        return Result(
            score=score,
            common=common,
            difference=difference,
        )
