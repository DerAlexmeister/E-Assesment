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



class CorrectingBooleanAssessment(Assessment):
    def assess(self, guess: Guess) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )

        if guess.answer == solution:
            return "You are correct!"
        else:
            if guess.question.normal_form == DISJUNCTION:
                inner = "*"
                outer = "+"
            elif guess.question.normal_form == CONJUNCTION:
                inner = "+"
                outer = "*"
            else:
                raise Exception("Unknown normal form")

            clause = f" {outer} ".join(
                f" {inner} ".join(str(lit) for lit in clause)
                for clause in guess.answer.clauses
            )
            return f"<p>The correct solution is {clause}</p>"


class DifferenceAssessment(Assessment):
    def assess(self, guess: Guess) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )

        if guess.answer == solution:
            return "You are correct!"
        else:
            response = []
            for g in guess.answer.clauses:
                if g in solution.clauses:
                    response.append((g, True))
                    solution.clauses.remove(g)
                else:
                    response.append((g, False))

            if guess.question.normal_form == DISJUNCTION:
                inner = "*"
                outer = "+"
            elif guess.question.normal_form == CONJUNCTION:

                inner = "+"
                outer = "*"
            else:
                raise Exception("Unknown normal form")

            clause = f" {outer} ".join(
                f"""<span style="color:{"green" if right else "red"}">
                {f"{inner} ".join(str(lit) for lit in clause)}
                </span>"""
                for clause, right in response
            )
            return f"<p>Not every thing is correct: {clause}</p>"


ASSESSMENTS = {
    'boolean': BooleanAssessment(),
    'grading': GradingAssessment(),
    'correcting_boolean': CorrectingBooleanAssessment(),
    'difference': DifferenceAssessment(),
}
