import urllib

from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime

from . form import NormalForm
from . import model

from .normal_form import CONJUNCTION, DISJUNCTION, Question
from .generator import generate_randomly, generate_adaptively, Difficulty
from .assessment import ASSESSMENTS, DifferenceAssessment
from ..views import calculateTimeDuration


QUESTION_KEY = 'question'

SYMBOLS = {
    DISJUNCTION: ('∧', '∨', '*', '+'),
    CONJUNCTION: ('∨', '∧', '+', '*')
}

def generate_task(task, qaw, request, cat, correction = None):
    n = task.normal_form
    question = generate_adaptively(n, qaw, request.user)
    request.session[QUESTION_KEY] = question.to_dict()

    beginTime = timezone.now()
    return render_question(
        request,
        question,
        NormalForm(question, initial={'penalty': 0, 'NameID': qaw.NameID, 'BeginTime': beginTime}),
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
    qaw = model.QAWSet.objects.get(NameID=str(cat))
    task = model.NormalForm.objects.get(Set=qaw.id)

    if request.method == 'POST':
        if 'new' in request.POST:
            return generate_task(task, qaw, request, cat)

        question = Question.from_dict(request.session[QUESTION_KEY])
        answer = NormalForm(question, request.POST)

        finished = False
        if answer.is_valid():
            guess = answer.cleaned_data['guess']
            penalty = answer.cleaned_data['penalty']

            params = dict()

            if 'check' in request.POST:
                assessment = DifferenceAssessment()

                answer = NormalForm(question, initial={
                    'penalty': penalty + 1,
                    'guess': answer.data['guess'],
                    'BeginTime': answer.data['BeginTime'],
                    'NameID': answer.data['NameID'],
                })
            else:
                endtime = datetime.now()
                raw_request = request.body.decode("UTF-8")
                raw_request_split = raw_request.split("&")
                NameID = ""
                print(raw_request)
                for element in raw_request_split:
                    if element.startswith("NameID="):
                        NameID = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))
                    if element.startswith("BeginTime="):
                        beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))

                print(NameID)

                qaw = model.QAWSet.objects.get(NameID=NameID)
                finished = True
                assessment = ASSESSMENTS[task.assessment]
                params = dict(duration=calculateTimeDuration(beginTime, endtime))

            correction = assessment.assess(guess, qaw=task.Set, user=request.user, penalty=penalty, **params)
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
        
        return generate_task(task, qaw, request, cat)
