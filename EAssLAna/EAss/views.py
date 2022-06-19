import urllib.parse

from django.http.response import HttpResponse
from django.shortcuts import render

from .models import Answer
from .models import OctaStatement
from .models import Question
from .models import BinaryStatement
from .models import WrongStatements
from .models import Cloze
from .models import QAWSet

from .forms import BinaryAnswerForm
from .forms import OctaAnswerForm
from .forms import MCAnswerForm
from .forms import TtAnswerForm
from .forms import ClozeForm

from random import randint
from random import shuffle
from random import sample

from .core import generateNumbers

from . import cloze as c

################################################
################# General ######################
################################################

def index(request):
    try:
        topics, data = ['Computer-Models', 'Gates', 'Calculus', 'Optimization', 'Assembler', 'Quantencomputing'], {}

        for topic in topics:
            data[topic.replace("-", "")] = assets if (assets := QAWSet.objects.filter(Topic=topic)) is not None and len(assets) else []

        return render(request, 'index.html', data)
    except Exception as error:
        print(error)


################################################
############### Generator ######################
################################################

def generateOctaQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            message = "You are wrong"
            question = int(request.POST['Question'], 8)
            answer = int(request.POST['Answer'], 10)
            if question == answer:
                message = "Well done"
            return render(request, 'octarandexample.html', {'message': message})
        else: 
            octaex = OctaStatement.objects.filter(Set__Categorie=(str(cat)))[0]
            target = (QAWSet.objects.filter(Categorie=(str(cat))))[0].Target
            expression = randint(5, octaex.MaxValue)
            expression = format(expression, "o")
            answerform = OctaAnswerForm(initial={'Question': expression})
            return render(request, 'octarandexample.html', {'octacode': expression, "Form": answerform, "Target": target})
    except Exception as error:
        print(error)
        return render(request, 'index.html')

def generateBinaryQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            message = "You are wrong"
            question = int(request.POST['Question'], 2)
            answer = int(request.POST['Answer'], 10)
            if question == answer:
                message = "Well done"
            return render(request, 'binaryrandexample.html', {'message': message})
        else: 
            binex = BinaryStatement.objects.filter(Set__Categorie=(str(cat)))[0]
            target = (QAWSet.objects.filter(Categorie=(str(cat))))[0].Target
            expression = randint(5, binex.MaxValue)
            expression = format(expression, "b")
            answerform = BinaryAnswerForm(initial={'Question': expression})
            return render(request, 'binaryrandexample.html', {'binarycode': expression, "Form": answerform, "Target": target})
    except Exception as error:
        print(error)
        return render(request, 'index.html')

def generateMCQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            message = "You are wrong"
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")
            answers = []
            for element in raw_request_split:
                if element.startswith("Options_q="):
                    answers.append(urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Options_q=", ""))))
            answerset = [str(answer) for answer in list(Answer.objects.filter(Set__Categorie=(str(cat))))]
            answerscorrection = [ans in answerset for ans in answers]
            if False in answerscorrection or len(answerscorrection) < 1:
                message = "Your answer is not correct."
            else:
                message = "Your answer is correct."
            return render(request, 'multiplechoiceexample.html', {'message': message})
        else:
            target = (QAWSet.objects.filter(Categorie=(str(cat))))[0].Target
            questionsset = Question.objects.filter(Set__Categorie=(str(cat)))
            answerset = Answer.objects.filter(Set__Categorie=(str(cat)))
            wrongstatementsset = WrongStatements.objects.filter(Set__Categorie=(str(cat)))
            answer = randint(0, answerset.count() - 1)
            question = randint(0, questionsset.count() - 1)
            numbers = generateNumbers(wrongstatementsset.count() - 1, 3)

            statements = [str(wrongstatementsset[i]) for i in numbers]
            statements.append(answerset[answer])
            question_f = questionsset[question]

            shuffle(statements)

            statements_f = []
            for i in statements: statements_f.append((i, i))

            mcform = MCAnswerForm(initial={'Question': question_f, 'Categorie': (str(cat)), 'Options': statements_f})
            return render(request, 'multiplechoiceexample.html', {'Form': mcform, 'Question': question_f, 'Categorie': (str(cat)), 'Target': target})
    except Exception as error:
        print(error)
    return render(request, 'multiplechoiceexample.html')

################################################
############### Examples #######################
################################################
def generateTtExample(request):
    try:
        if request.method == "POST":
           
            postresult = dict(request.POST)

            result = {}

            checklist = list(Answer.objects.filter(Set__Categorie='test'))
            postresult.pop('csrfmiddlewaretoken')
            for k, v in postresult.items():
                if k in checklist:
                    result[k].append([v, True])
                else:
                    result[k].append([v, False])
            
            """
            useransweredwithright = request.POST['Right1']
            useransweredwithwrong = request.POST['Wrong']
            
            for x in useransweredwithright:
                if x in list(Answer.objects.filter(Set__Categorie='test')):
                    result.update({x:[True, True]})
                else:
                    result.update({x:[True, False]})

            for x in useransweredwithwrong:
                if x in list(WrongStatements.objects.filter(Set__Categorie='test')):
                    result.update({x:[False, True]})
                else:
                    result.update({x:[False, False]})
            """

            correctcounter = [ True if i else False for i in result.values([1])].count(True)

            message = "You answered {}/6 statements correctly.".format(correctcounter)
           
            return render(request, 'multiplechoiceexample.html', {'message': message, 'result': result})
        else:
            answerset = Answer.objects.filter(Set__Categorie='test')
            wrongstatementsset = WrongStatements.objects.filter(Set__Categorie='test')

            countstatements = 6
            countanswers = generateNumbers(countstatements, 1)[0]

            answernumbers = sample(range(0, answerset.count()), countanswers)
            wrongstatementsnumbers = sample(range(0, wrongstatementsset.count()), countstatements - countanswers)
            
            statements = [str(answerset[i]) for i in answernumbers]
            statements += [str(wrongstatementsset[i]) for i in wrongstatementsnumbers]

            shuffle(statements)

            mcform = TtAnswerForm(initial={'Categorie': 'test', 'Options': statements})
            return render(request, 'truthtableexample.html', {'Form': mcform, 'Categorie': 'test'})
    except Exception as error:
        print(error)
    return render(request, 'multiplechoiceexample.html')


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
        return render(request, 'index.html')

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


