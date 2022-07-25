from abc import ABC, abstractmethod
from dataclasses import dataclass

from . import model
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
    def assess(self, guess: Guess, **kwargs) -> str:
        pass


class BooleanAssessment(Assessment):
    def assess(self, guess: Guess, **kwargs) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )
        if guess.answer == solution:
            return "You are correct!"
        else:
            return "You are false!"


class GradingAssessment(Assessment):
    def assess(self, guess: Guess, guess_model, **kwargs) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )
        counter = 0
        for g, e in zip(solution.clauses, guess.answer.clauses):
            if g == e:
                counter += 1

        if guess_model:
            correction = model.NormalFormCorrection(guess=guess_model, points=counter, total_points=len(solution.clauses))
            correction.save()

        return f"You have {counter} of {len(solution.clauses)} correct!"



class CorrectingBooleanAssessment(Assessment):
    def assess(self, guess: Guess, **kwargs) -> str:
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
    def assess(self, guess: Guess, **kwargs) -> str:
        solution = SOLUTIONS_CALCULATORS[guess.question.normal_form](
            guess.question.function,
        )

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
        return f"<p>f(a)  =    {clause}</p>"


@dataclass
class RememberingAssessment(Assessment):
    assessment: Assessment

    def assess(self, guess: Guess, qaw, **kwargs) -> str:
        question = model.NormalFormQuestion(normal_form=guess.question.normal_form)
        question.save()

        for col, _ in guess.question.function.table[guess.question.function.results==1].iterrows():
            function_value = model.FunctionValue(question=question, one=col)
            function_value.save()

        answer = model.NormalFormAnswer()
        answer.save()

        for clause in guess.answer.clauses:
            term = model.NormalFormTerm(answer=answer)
            term.save()

            for lit in clause:
                literal = model.NormalFormLiteral(term=term, variable=lit.variable, sign=lit.sign)
                literal.save()

        guess_model = model.NormalFormGuess(qaw=qaw, question=question, answer=answer)
        guess_model.save()

        return self.assessment.assess(guess, **{'guess_model': guess_model, **kwargs})


ASSESSMENTS = {
    name: RememberingAssessment(assessment)
    for name, assessment in {
        'boolean': BooleanAssessment(),
        'grading': GradingAssessment(),
        'correcting_boolean': CorrectingBooleanAssessment(),
        'difference': DifferenceAssessment(),
    }.items()
}
