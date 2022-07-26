from dataclasses import dataclass
from typing import List, Set

from . import models


@dataclass
class Gap:
    preceeding_text: str
    succeeding_text: str
    solutions: Set[str]

@dataclass
class Cloze:
    gaps: List[Gap]


def to_model(cloze: Cloze, qaw: models.QAWSet):
    for i, gap in enumerate(cloze.gaps):
        gap_model = models.Gap(
            preceeding_text=gap.preceeding_text,
            succeeding_text=gap.succeeding_text,
        )
        gap_model.save()

        # Assign gap position in cloze
        models.Cloze(qaw=qaw, gap=gap, position=i).save()

        # Associate solutions with gap
        for solution in gap.solutions:
            solution_model = models.GapSolution(
                solution=solution,
                gap=gap_model,
            )
            solution_model.save()


def from_model(clozes) -> Cloze:

    gaps = []
    for cloze in clozes:
        solutions = {s.solution for s in cloze.gap.gapsolution_set.all()}
        gap = Gap(
            cloze.gap.preceeding_text,
            cloze.gap.succeeding_text,
            solutions,
        )
        gaps.append(gap)

    return Cloze(gaps)
