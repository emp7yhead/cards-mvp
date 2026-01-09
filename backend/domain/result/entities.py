from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    score: int
    common: list[str]
    difference: list[str]
