import pandas as pd
import numpy as np

from dataclasses import dataclass
from random import sample

from . import model
from .normal_form import DISJUNCTION, TruthTable, Question


@dataclass
class Difficulty:
    num_variables: int
    num_terms: int
    normal_form: str

VARIABLES = ["a", "b", "c", "d", "e"]

MINIMAL_NUM_VARIABLES = 2
MINIMAL_NUM_TERMS = 1
VARIABLE_RATE = .5
TERM_RATE = .5

def updateProgress(rate, points, total_points):
    half = total_points/2
    return rate * (points - half) / half

def chooseSize(progress, minimum, maximum):
    return int(minimum + (maximum - minimum) * progress)

def getProgress(form, qaw, user):
    variable_progress = min(max(sum(
        updateProgress(VARIABLE_RATE, correction.points, correction.total_points)
        for correction in model.NormalFormCorrection.objects\
            .filter(guess__Set__id=qaw.id)
            .filter(guess__UserID=user.id)
            .filter(guess__question__normal_form=form)
    ), 0), 1)
    term_progress = min(max(sum(
        updateProgress(TERM_RATE, correction.points, correction.total_points)
        for correction in model.NormalFormCorrection.objects.all()
            .filter(guess__question__normal_form=form)
    ), 0), 1)

    return variable_progress, term_progress

def generate_randomly(difficulty: Difficulty):
    variables = VARIABLES[:difficulty.num_variables]

    num_input = 2**difficulty.num_variables
    numbers = np.arange(num_input, dtype=np.uint8)
    bits = np.unpackbits(numbers[:, np.newaxis], axis=1)[:, -difficulty.num_variables:]

    ones = sample(range(num_input), difficulty.num_terms)
    if difficulty.normal_form == DISJUNCTION:
        results = np.zeros(num_input, dtype=np.uint8)
        results[ones] = 1
    else:
        results = np.ones(num_input, dtype=np.uint8)
        results[ones] = 0


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


def generate_adaptively(difficulty: model.NormalFormDifficulty, qaw, user) -> Question:
    variable_progress, term_progress = getProgress(difficulty.normal_form, qaw, user)
    num_variables = chooseSize(variable_progress, MINIMAL_NUM_VARIABLES, difficulty.num_variables)
    maximal_num_terms = min(2**num_variables-1, difficulty.num_terms)
    num_terms = chooseSize(term_progress, MINIMAL_NUM_TERMS, maximal_num_terms)
    return generate_randomly(Difficulty(num_variables, num_terms, difficulty.normal_form))
