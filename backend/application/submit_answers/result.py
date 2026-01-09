from dataclasses import dataclass


@dataclass(frozen=True)
class SubmitAnswersResult:
    session_completed: bool
