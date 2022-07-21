import pandas as pd
import numpy as np

from dataclasses import dataclass
from random import sample

from . import model
from .normal_form import TruthTable, Question, NORMAL_FORMS


@dataclass
class Difficulty:
    num_variables: int
    num_terms: int
    normal_form: str

VARIABLES = ["a", "b", "c", "d", "e"]

MINIMAL_NUM_VARIABLES = 1
MINIMAL_NUM_TERMS = 1
VARIABLE_RATE = 0.15
TERM_RATE = 0.05

def updateProgress(rate, points, total_points):
    half = total_points/2
    return rate * (points - half) / half

def chooseSize(progress, minimum, maximum):
    return int(minimum + (maximum - minimum) * progress)

def getProgress(form):
    variable_progress = max(sum(
        updateProgress(VARIABLE_RATE, correction.points, correction.total_points)
        for correction in model.NormalFormCorrection.objects\
            .filter(guess__question__normal_form=form)
    ), 0)
    term_progress = max(sum(
        updateProgress(TERM_RATE, correction.points, correction.total_points)
        for correction in model.NormalFormCorrection.objects.all()
            .filter(guess__question__normal_form=form)
    ), 0)

    return variable_progress, term_progress

def generate_randomly(difficulty: Difficulty):
    variables = VARIABLES[:difficulty.num_variables]

    num_input = 2**difficulty.num_variables
    numbers = np.arange(num_input, dtype=np.uint8)
    bits = np.unpackbits(numbers[:, np.newaxis], axis=1)[:, -difficulty.num_variables:]

    results = np.zeros(num_input, dtype=np.uint8)
    ones = sample(range(num_input), difficulty.num_terms)
    results[ones] = 1

    table = np.column_stack((bits, results))

    function_name = "f"
    columns = list(sorted(variables))
    result_name = f"{function_name}({', '.join(columns)})"
    columns.append(result_name)

    truth_table = TruthTable(
        pd.DataFrame(table, columns=columns),
        result_name,
    )

    return Question(difficulty.normal_form, truth_table)


def generate_adaptively(difficulty: model.NormalFormDifficulty) -> Question:
    variable_progress, term_progress = getProgress(difficulty.normal_form)
    num_variables = chooseSize(variable_progress, MINIMAL_NUM_TERMS, difficulty.num_variables)
    maximal_num_terms = min(2**num_variables, difficulty.num_terms)
    num_terms = chooseSize(term_progress, MINIMAL_NUM_TERMS, maximal_num_terms)
    return generate_randomly(Difficulty(num_variables, num_terms, difficulty.normal_form))
