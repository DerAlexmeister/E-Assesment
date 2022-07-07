from abc import ABC, abstractmethod

from .normal_form import Guess, TruthTable, Literal, NormalForm, DISJUNCTION, CONJUNCTION



def to_dnf(formula: TruthTable) -> NormalForm:
    clauses = []
    for _, assignment in formula.table[formula.results==1].iterrows():
        clause = []
        for v in formula.variables:
            clause.append(Literal(v, bool(assignment[v])))
        clauses.append(clause)
    return NormalForm(clauses)


def to_cnf(formula: TruthTable) -> NormalForm:
    clauses = []
    for _, assignment in formula.table[formula.results==0].iterrows():
        clause = []
        for v in formula.variables:
            clause.append(Literal(v, bool(assignment[v])))
        clauses.append(clause)
    return NormalForm(clauses)


SOLUTIONS_CALCULATORS = {
    DISJUNCTION: to_dnf,
    CONJUNCTION: to_cnf,
}


class Assessment(ABC):
    @abstractmethod
    def assess(self, guess: Guess) -> str:
        pass


class BooleanAssessment(Assessment):
    def assess(self, guess: Guess) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )
        if guess.answer == solution:
            return "You are correct!"
        else:
            return "You are false!"


class GradingAssessment(Assessment):
    def assess(self, guess: Guess) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )
        counter = 0
        for g, e in zip(solution.clauses, guess.answer.clauses):
            if g == e:
                counter += 1
        return f"You have {counter} of {len(solution.clauses)} correct!"


ASSESSMENTS = {
    'boolean': BooleanAssessment(),
    'grading': GradingAssessment(),
}
