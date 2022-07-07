from django.http.response import HttpResponse

from django.shortcuts import render

from .. import models

from . form import NormalForm

from .. import models

from .normal_form import Question
from .generator import Generator, Difficulty
from .assessment import ASSESSMENTS


QUESTION_KEY = 'question'


def render_question(request, question, answer, category, correction = None):
    return render(request, 'normal_form.html', {
        'question': question,
        'table': question.function.table.to_html(),
        'input': answer,
        'category': category,
        'correction': correction,
    })


def normal_form(request):
    cat = request.GET.get('t', '')
    task = models.NormalForm\
              .objects\
              .filter(Set__NameID=(str(cat)))\
              .first()

    if request.method == 'POST':
        assessment = ASSESSMENTS[task.assessment]
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
            cat,
            correction,
        )

    else:
        n = task.normal_form
        difficulty = Difficulty(n.num_variables, n.num_ones, n.normal_form)
        question = Generator().create(difficulty)
        request.session[QUESTION_KEY] = question.to_dict()

        return render_question(
            request,
            question,
            NormalForm(question),
            cat,
        )
