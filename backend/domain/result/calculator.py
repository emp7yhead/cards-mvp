from typing import Protocol

from backend.domain.result.entities import Result
from backend.domain.session.value_objects import Answers, Preference, SessionId


class ResultCalculator(Protocol):
    def calculate(
        self,
        session_id: SessionId,
        answers_1: Answers,
        answers_2: Answers,
    ) -> Result: ...


class SimpleResultsCalculator:
    def _is_common(
        self,
        preference_1: Preference,
        preference_2: Preference,
    ) -> bool:
        is_neutral = preference_1 == Preference.NEUTRAL
        return preference_1 == preference_2 and not is_neutral

    def _is_difference(
        self,
        preference_1: Preference,
        preference_2: Preference,
    ) -> bool:
        if preference_1 == Preference.NEUTRAL and preference_2 == Preference.NEUTRAL:  # noqa: E501
            return False
        return preference_1 != preference_2

    def _get_score(self, common: list, answers_1: Answers, answers_2: Answers):
        total = len(answers_1.keys() & answers_2.keys())
        if total == 0:
            return 0
        return round(len(common) / total * 100)

    def calculate(
        self,
        session_id: SessionId,
        answers_1: Answers,
        answers_2: Answers,
    ) -> Result:
        common = []
        difference = []

        shared_questions = answers_1.keys() & answers_2.keys()

        for question_id in shared_questions:
            answer_1 = answers_1[question_id]
            answer_2 = answers_2[question_id]

            if self._is_common(answer_1, answer_2):
                common.append(question_id)
            if self._is_difference(answer_1, answer_2):
                difference.append(question_id)

        score = self._get_score(
            common,
            answers_1,
            answers_2,
        )
        return Result(
            session_id=session_id,
            score=score,
            common=common,
            difference=difference,
        )
