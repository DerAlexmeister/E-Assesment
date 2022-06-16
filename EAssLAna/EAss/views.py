import urllib.parse

from django.http.response import HttpResponse
from django.shortcuts import render

from .models import Answer
from .models import Question
from .models import BinaryStatement
from .models import WrongStatements
from .models import Cloze

from .forms import BinaryAnswerForm
from .forms import MCAnswerForm
from .forms import ClozeForm

from random import randint
from random import shuffle

from .core import generateNumbers

from . import cloze as c

################################################
############### Model und Assmbler #############
################################################

def generateMCQuestions(request):
    try:
        if request.method == "POST":
            pass
        else:
            pass
    except Exception as error:
        print(error)

################################################
############### Examples #######################
################################################

def generateMCExample(request):
    try:
        if request.method == "POST":
            message = "You are wrong"
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")
            answers = []
            for element in raw_request_split:
                if element.startswith("Options_q="):
                    answers.append(urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Options_q=", ""))))
            answerset = [str(answer) for answer in list(Answer.objects.filter(Set__Categorie='DLX-Pipeline'))]
            answerscorrection = [ans in answerset for ans in answers]
            print(answerscorrection, answerset)
            if False in answerscorrection or len(answerscorrection) < 1:
                message = "Your answer is not correct."
            else:
                message = "Your answer is correct."
            return render(request, 'multiplechoiceexample.html', {'message': message})
        else:
            questionsset = Question.objects.filter(Set__Categorie='DLX-Pipeline')
            answerset = Answer.objects.filter(Set__Categorie='DLX-Pipeline')
            wrongstatementsset = WrongStatements.objects.filter(Set__Categorie='DLX-Pipeline')
            answer = randint(0, answerset.count() - 1)
            question = randint(0, questionsset.count() - 1)
            numbers = generateNumbers(wrongstatementsset.count() - 1, 3)

            statements = [str(wrongstatementsset[i]) for i in numbers]
            statements.append(answerset[answer])
            question_f = questionsset[question]

            shuffle(statements)

            statements_f = []
            for index, i in enumerate(statements):
                statements_f.append((i, i))

            mcform = MCAnswerForm(initial={'Question': question_f, 'Categorie': 'DLX-Pipeline', 'Options': statements_f})
            return render(request, 'multiplechoiceexample.html', {'Form': mcform, 'Question': question_f, 'Categorie': 'DLX-Pipeline'})
    except Exception as error:
        print(error)
    return render(request, 'multiplechoiceexample.html')

def generateBinaryExpression(request):
    try:
        if request.method == "POST":
            message = "You are wrong"
            question = int(request.POST['Question'], 2)
            answer = int(request.POST['Answer'], 10)
            if question == answer:
                message = "Well done"
            return render(request, 'binaryrandexample.html', {'message': message})
        else: 
            binex = BinaryStatement.objects.first()
            expression = randint(5, binex.MaxValue)
            expression = format(expression, "b")
            answerform = BinaryAnswerForm(initial={'Question': expression})
        return render(request, 'binaryrandexample.html', {'binarycode': expression, "Form": answerform})
    except Exception as error:
        print(error)
        return render(request, 'multiplechoiceexample.html')

def clozeText(request):
    if request.method == 'POST':
        cloze_id = request.POST['cloze_id']
        qaw = QAWSet.objects.get(id=cloze_id)

        cloze = c.from_model(qaw)

        gaps = [
            request.POST[ClozeForm.get_gap_key(i)]
            for i in range(len(cloze.gaps))
        ]

        maximal = len(cloze.gaps)
        count = 0

        for guess, solution in zip(gaps, cloze.gaps):
            if guess in solution.solutions:
                count += 1

        return HttpResponse(f"{count} of {maximal} are correct.")
    else:
        qaw = Cloze.objects\
             .first()\
             .qaw
        cloze = c.from_model(qaw)

        cloze_form = ClozeForm(
            len(cloze.gaps),
            initial={
                'cloze_id': qaw.id,
            },
        )

        cloze_items = []

        for i, gap in enumerate(cloze.gaps):
            cloze_items.extend([
                gap.preceeding_text,
                cloze_form[ClozeForm.get_gap_key(i)],
                gap.succeeding_text,
            ])

        return render(request, 'cloze_text.html',  {
            'cloze_items': cloze_items,
            'form': cloze_form,
        })

def generateDragNDropExample(request):
    try:
        return render(request, 'dragndropexample.html')
    except Exception as error:
        print(error)
        return render(request, 'multiplechoiceexample.html')


