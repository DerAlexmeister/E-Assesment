from django.http.response import HttpResponse

from django.shortcuts import render

from . form import NormalForm
from . import model

from .normal_form import CONJUNCTION, DISJUNCTION, Question
from .generator import generate_randomly, generate_adaptively, Difficulty
from .assessment import ASSESSMENTS, DifferenceAssessment


QUESTION_KEY = 'question'

SYMBOLS = {
    DISJUNCTION: ('∧', '∨', '*', '+'),
    CONJUNCTION: ('∨', '∧', '+', '*')
}

def generate_task(task, request, cat, correction = None):
    n = task.normal_form
    question = generate_adaptively(n)
    request.session[QUESTION_KEY] = question.to_dict()

    return render_question(
        request,
        question,
        NormalForm(question, initial={'penalty': 0}),
        cat,
        False,
        correction,
    )


def render_question(request, question, answer, category, finished, correction = None):
    real_inner, real_outer, inner, outer = SYMBOLS[question.normal_form]

    return render(request, 'normal_form.html', {
        'question': question,
        'table': question.function.table.to_html(classes='table table-striped table-bordered table-hover table-sm'),
        'input': answer,
        'category': category,
        'correction': correction,
        'real_inner': real_inner,
        'real_outer': real_outer,
        'outer': outer,
        'inner': inner,
        'finished': finished,
    })


def normal_form(request):
    cat = request.GET.get('t', '')
    task = model.NormalForm\
              .objects\
              .filter(Set__NameID=(str(cat)))\
              .first()

    if request.method == 'POST':
        if 'new' in request.POST:
            return generate_task(task, request, cat)

        question = Question.from_dict(request.session[QUESTION_KEY])
        answer = NormalForm(question, request.POST)

        finished = False
        if answer.is_valid():
            guess = answer.cleaned_data['guess']
            penalty = answer.cleaned_data['penalty']
            if 'check' in request.POST:
                assessment = DifferenceAssessment()
                answer = NormalForm(question, initial={
                    'penalty': penalty + 1,
                    'guess': answer.data['guess'],
                })
            else:
                finished = True
                assessment = ASSESSMENTS[task.assessment]

            correction = assessment.assess(guess, qaw=task.Set, user=request.user, penalty=penalty)
        else:
            correction = answer.errors.get('guess')

        return render_question(
            request,
            question,
            answer,
            cat,
            finished,
            correction,
        )

    else:
        n = task.normal_form
        question = generate_adaptively(n)
        request.session[QUESTION_KEY] = question.to_dict()

        return generate_task(task, request, cat)
