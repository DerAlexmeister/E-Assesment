import pandas as pd
import numpy as np

from dataclasses import dataclass
from random import sample

from .normal_form import TruthTable, Question


@dataclass
class Difficulty:
    num_variables: int
    num_terms: int
    normal_form: str


@dataclass
class Knowledge:
    num_variables: float
    num_terms: float

VARIABLES = ["a", "b", "c", "d", "e"]

class AdaptiveGenerator:
    def create(self, difficulty: Difficulty) -> Question:
        pass

@dataclass
class Generator:
    def create(self, difficulty: Difficulty) -> Question:
        #variables = [f"x{i}" for i in range(difficulty.num_variables)]
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
