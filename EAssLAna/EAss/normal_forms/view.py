from django.http.response import HttpResponse

from django.shortcuts import render

from random import choice

from . form import NormalForm

from .normal_form import Guess, TruthTable, Question, DISJUNCTION, CONJUNCTION
from .assessment import BooleanAssessment
from ..core import generateNumbers


QUESTION_KEY = 'question'


def render_question(request, question, answer, correction = None):
    return render(request, 'normal_form.html', {
        'question': question,
        'table': question.function.table.to_html(),
        'input': answer,
        'correction': correction,
    })


def normal_form(request):
    if request.method == 'POST':
        assessment = BooleanAssessment()

        question = Question.from_dict(request.session[QUESTION_KEY])
        answer = NormalForm(question, request.POST)

        if answer.is_valid():
            guess = answer.cleaned_data['guess']
            correction = assessment.assess(guess)
        else:
            correction = answer.errors.get('guess')

        return render_question(
            request,
            question,
            answer,
            correction,
        )

    else:
        variables = {"a", "b"}
        results = generateNumbers(1, 2**len(variables))
        table = TruthTable.create(variables, "f", results)
        normal_form = choice([DISJUNCTION, CONJUNCTION])

        question = Question(normal_form, table)

        request.session[QUESTION_KEY] = question.to_dict()

        return render_question(
            request,
            question,
            NormalForm(question)
        )
