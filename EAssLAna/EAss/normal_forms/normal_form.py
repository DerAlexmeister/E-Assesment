import pandas as pd
import numpy as np

from abc import ABC, abstractmethod

from dataclasses import dataclass


DISJUNCTION = "disjunctive"
CONJUNCTION = "conjunctive"


@dataclass
class Difficulty:
    num_variables: int
    num_disjunctions: int
    num_conjunctions: int


class TruthTable:
    def __init__(self, table, function_name):
        self.table = table
        self.function = function_name

    @staticmethod
    def create(variables, function_name, results):
        num_bits = len(variables)
        num_input = 2**num_bits
        assert len(results) == num_input

        numbers = np.arange(num_input, dtype=np.uint8)

        bits = np.unpackbits(numbers[:, np.newaxis], axis=1)[:, -num_bits:]
        table = np.column_stack((bits, results))


        columns = list(sorted(variables))
        function = f"{function_name}({', '.join(columns)})"
        columns.append(function)
        table = pd.DataFrame(table, columns=columns)
        return TruthTable(table, function)

    @property
    def variables(self):
        return self.table.loc[:, self.table.columns != self.function]

    @property
    def results(self):
        return self.table[self.function]

    def to_dict(self):
        return {
            'function_name': self.function,
            'table': self.table.to_dict(),
        }

    @staticmethod
    def from_dict(dictionary):
        function_name = dictionary['function_name']
        table = pd.DataFrame(dictionary['table'])

        return TruthTable(table, function_name)


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
        self.clause = normalise_formula(
            map(normalise_clause, clauses)
        )


@dataclass
class Question:
    normal_form: str
    function: TruthTable


@dataclass
class Guess:
    question: Question
    answer: NormalForm


def to_dnf(formula: TruthTable) -> NormalForm:
    clauses = []
    for _, assignment in formula.table[formula.results==1].iterrows():
        clause = []
        for v in formula.variables:
            clause.append(Literal(v, bool(assignment[v])))
        clauses.append(clause)
    return NormalForm(clauses)

def to_cnf(formula: TruthTable) -> NormalForm:
    pass


class Assessment(ABC):
    @abstractmethod
    def assess(self, guess: Guess) -> str:
        pass

class BooleanAssessment(Assessment):
    def assess(self, guess: Guess) -> str:
        pass
