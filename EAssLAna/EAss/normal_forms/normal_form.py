from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


from dataclasses import dataclass


DISJUNCTION = "disjunctive"
CONJUNCTION = "conjunctive"


@dataclass
class Difficulty:
    num_variables: int
    num_disjunctions: int
    num_conjunctions: int


class TruthTable:
    def __init__(self, table, result_name):
        self.table = table
        self.result_name = result_name

    @staticmethod
    def create(variables, function_name, results) -> "TruthTable":
        num_bits = len(variables)
        num_input = 2**num_bits
        assert len(results) == num_input

        numbers = np.arange(num_input, dtype=np.uint8)

        bits = np.unpackbits(numbers[:, np.newaxis], axis=1)[:, -num_bits:]
        table = np.column_stack((bits, results))


        columns = list(sorted(variables))
        result_name = f"{function_name}({', '.join(columns)})"
        columns.append(result_name)
        table = pd.DataFrame(table, columns=columns)

        return TruthTable(table, result_name)

    @property
    def variables(self):
        return self.table.loc[:, self.table.columns != self.result_name]

    @property
    def results(self):
        return self.table[self.result_name]


@dataclass
class Literal:
    variable: str
    sign: bool


def normalise_clause(clause):
    return list(sorted(clause, key=lambda l: (l.variable, l.sign)))


def normalise_formula(clauses):
    return list(sorted(clauses, key=lambda c: len(c)))


class NormalForm:
    def __init__(self, clauses):
        self.clauses = normalise_formula(
            map(normalise_clause, clauses)
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NormalForm):
            return self.clauses == other.clauses

        return False

    def __ne__(self, other: object) -> bool:
        return not self == other


@dataclass
class Question:
    NORMAL_FORM_KEY = 'type'
    TABLE_KEY = 'table'
    RESULT_NAME_KEY = 'result'

    normal_form: str
    function: TruthTable

    def to_dict(self):
        return {
            self.NORMAL_FORM_KEY: self.normal_form,
            self.TABLE_KEY: self.function.table.to_dict(),
            self.RESULT_NAME_KEY: self.function.result_name,
        }

    @staticmethod
    def from_dict(d):
        normal_form = d[Question.NORMAL_FORM_KEY]
        table = pd.DataFrame(d[Question.TABLE_KEY])
        result_name = d[Question.RESULT_NAME_KEY]

        return Question(
            normal_form,
            TruthTable(table, result_name),
        )



@dataclass
class Guess:
    question: Question
    answer: NormalForm
