import numpy as np
import pandas as pd

from django.shortcuts import render
from django.http.response import HttpResponse

from random import choice

from .form import NormalForm
from .normal_form import BooleanAssessment, TruthTable, Question, DISJUNCTION, CONJUNCTION
from ..core import generateNumbers


def normal_form(request):
    if request.method == 'POST':
        assessment = BooleanAssessment()
        table = TruthTable.from_dict(request.session['table'])
        normal_form = request.session['normal_form']

        question = Question(normal_form, table)
        guess = NormalForm(table.variables, request.POST)

        if guess.is_valid():
            return render(request, 'normal_form.html', {
                'question': question,
                'table': question.function.table.to_html(),
                'input': guess,
            })
        else:
            return HttpResponse(guess.errors.get('guess'))
    else:
        variables = {"a", "b"}
        results = generateNumbers(1, 2**len(variables))
        table = TruthTable.create(variables, "f", results)
        normal_form = choice([DISJUNCTION, CONJUNCTION])

        question = Question(normal_form, table)

        request.session['table'] = table.to_dict()
        request.session['normal_form'] = normal_form

        return render(request, 'normal_form.html', {
            'question': question,
            'table': question.function.table.to_html(),
            'input': NormalForm(question.function.variables),
        })
