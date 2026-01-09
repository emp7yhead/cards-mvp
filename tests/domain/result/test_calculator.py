from backend.domain.result.calculator import SimpleResultsCalculator
from backend.domain.session.value_objects import Preference


def test_like_like_is_common():
    calc = SimpleResultsCalculator()
    answer_1 = {'question_1': Preference.LIKE}
    answer_2 = {'question_1': Preference.LIKE}
    res = calc.calculate(answer_1, answer_2)
    assert res.common == ['question_1']
    assert res.score == 100

