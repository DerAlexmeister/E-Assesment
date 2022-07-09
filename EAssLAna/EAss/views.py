import urllib.parse
import json

from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from .models import Answer
from .models import OctaStatement
from .models import Question
from .models import BinaryStatement
from .models import WrongStatements
from .models import Cloze
from .models import QAWSet
from .models import OpenAssemblerCodeQuestions

from .models import CalculusSingleUserAnswer
from .models import SingleChoiceUserAnswer
from .models import MultipleChoiceUserAnswer
from .models import SingleMultipleChoiceUserAnswer
from .models import TruthTableUserAnswer
from .models import SingleTruthTableUserAnswer
from .models import ClozeUserAnswer
from .models import SingleFieldClozeUserAnswer
from .models import OpenAssemblerAnswer
from .models import GatesAnswer

from .forms import BinaryAnswerForm
from .forms import OctaAnswerForm
from .forms import SCAnswerForm
from .forms import MCAnswerForm
from .forms import TtAnswerForm
from .forms import ClozeForm
from .forms import OpenAssemblerAnswerForm
from .forms import GatesAnswerForm

from random import randint
from random import shuffle
from random import sample

from .core import generateNumbers
from .assembly import parser

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
    return redirect('homeview')


################################################
############### Generator ######################
################################################

def generateOctaQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            iscorrect, message = False, "You answer is wrong"
            question = int(request.POST['Question'])
            answer = int(request.POST['Answer'], 10)
            if question == answer:
                iscorrect, message = True, "Your answer is correct."
            useranswer = CalculusSingleUserAnswer(Answer=answer, Correct=iscorrect, Question=question, CalcType="Octa")
            useranswer.save()
            return render(request, 'octarandexample.html', {'message': message, 'correct': iscorrect})
        else: 
            octaex = OctaStatement.objects.filter(Set__NameID=(str(cat)))[0]
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            expression = randint(5, octaex.MaxValue)
            expression = format(expression, "o")
            answerform = OctaAnswerForm(initial={'Question': expression})
            return render(request, 'octarandexample.html', {'octacode': expression, "Form": answerform, "Target": target})
    except Exception as error:
        print(error)
    return redirect('homeview')

def generateBinaryQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            iscorrect, message = False, "You answer is wrong"
            question = int(request.POST['Question'], 2)
            answer = int(request.POST['Answer'], 10)
            if question == answer:
                iscorrect, message = True, "Your answer is correct."
            useranswer = CalculusSingleUserAnswer(Answer=answer, Correct=iscorrect, Question=question, CalcType="Bin")
            useranswer.save()
            return render(request, 'binaryrandexample.html', {'message': message, 'correct': iscorrect})
        else: 
            binex = BinaryStatement.objects.filter(Set__NameID=(str(cat)))[0]
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            expression = randint(5, binex.MaxValue)
            expression = format(expression, "b")
            answerform = BinaryAnswerForm(initial={'Question': expression})
            return render(request, 'binaryrandexample.html', {'binarycode': expression, "Form": answerform, "Target": target})
    except Exception as error:
        print(error)
    return redirect('homeview')

def generateSCQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            iscorrect, message = True, "Your answer is correct."
            question = ""
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")
            answers = []

            for element in raw_request_split:
                if element.startswith("Options_q="):
                    answers.append(urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Options_q=", ""))))
                if element.startswith("Question="):
                    question += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Question=", "")))
            answerset = [str(answer) for answer in list(Answer.objects.filter(Set__NameID=(str(cat))))]
            answerscorrection = [ans in answerset for ans in answers]

            if False in answerscorrection or len(answerscorrection) < 1:
                iscorrect, message = False, "Your answer is wrong."
    
            useranswer = SingleChoiceUserAnswer(Answer=answers[0], Correct=iscorrect, Question=question, Topic=str(cat))
            useranswer.save()

            return render(request, 'singlechoiceexample.html', {'message': message, 'correct':iscorrect})
        else:
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            questionsset = Question.objects.filter(Set__NameID=(str(cat)))
            answerset = Answer.objects.filter(Set__NameID=(str(cat)))
            wrongstatementsset = WrongStatements.objects.filter(Set__NameID=(str(cat)))
            answer = randint(0, answerset.count() - 1)
            question = randint(0, questionsset.count() - 1)
            numbers = generateNumbers(wrongstatementsset.count() - 1, 3)

            statements = [str(wrongstatementsset[i]) for i in numbers]
            statements.append(answerset[answer])
            question_f = questionsset[question]

            shuffle(statements)

            statements_f = []
            for i in statements: statements_f.append((i, i))

            answerform = SCAnswerForm(initial={'Question': question_f, 'Categorie': (str(cat)), 'Options': statements_f})
            return render(request, 'singlechoiceexample.html', {'Form': answerform, 'Question': question_f, 'Categorie': (str(cat)), 'Target': target})
    except Exception as error:
        print(error)
    return redirect('homeview')

def generateMCQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            iscorrect, message = True, "Your answer is correct."
            question = ""
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")
            answers = []
            for element in raw_request_split:
                if element.startswith("Options_q="):
                    answers.append(urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Options_q=", ""))))
                if element.startswith("Question="):
                    question += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Question=", "")))
            answerset = [str(answer) for answer in list(Answer.objects.filter(Set__NameID=(str(cat))))]
            
            useranswer = MultipleChoiceUserAnswer(AllCorrect=iscorrect, Question=question, Topic=str(cat))
            useranswer.save()

            answercorrect = False
            correctcounter = 0
            for index, element in enumerate(answers):
                if element in answerset:
                    answercorrect = True
                    correctcounter += 1
                else:
                    iscorrect, message = False, "Your answer is wrong."
                singleuseranswer = SingleMultipleChoiceUserAnswer(Correct=answercorrect, Answer=element, AllAnswers=useranswer)
                singleuseranswer.save()

            useranswer.AllCorrect = iscorrect
            useranswer.save()

            message += " You answered {}/{} statements correctly.".format(correctcounter, index+1)
    
            return render(request, 'multiplechoiceexample.html', {'message': message, 'correct':iscorrect})
        else:
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            questionsset = Question.objects.filter(Set__NameID=(str(cat)))
            answerset = Answer.objects.filter(Set__NameID=(str(cat)))
            wrongstatementsset = WrongStatements.objects.filter(Set__NameID=(str(cat)))
            answer = randint(0, answerset.count() - 1)
            question = randint(0, questionsset.count() - 1)
            numbers = generateNumbers(wrongstatementsset.count() - 1, 3)

            statements = [str(wrongstatementsset[i]) for i in numbers]
            statements.append(answerset[answer])
            question_f = questionsset[question]

            shuffle(statements)

            statements_f = []
            for i in statements: statements_f.append((i, i))

            answerform = MCAnswerForm(initial={'Question': question_f, 'Categorie': (str(cat)), 'Options': statements_f})
            return render(request, 'multiplechoiceexample.html', {'Form': answerform, 'Question': question_f, 'Categorie': (str(cat)), 'Target': target})
    except Exception as error:
        print(error)
    return redirect('homeview')

def clozeTextGenerator(request):
    cat = request.GET.get('t', '')
    if request.method == 'POST':
        iscorrect, message = True, "Your answer is correct."
        cloze_id = request.POST['cloze_id']
        qaw = QAWSet.objects.get(id=cloze_id)
        cloze = c.from_model(qaw)

        gaps = [request.POST[ClozeForm.get_gap_key(i)] for i in range(len(cloze.gaps))]
        maximal, count = len(cloze.gaps), 0

        useranswer = ClozeUserAnswer(Topic=str(cat), AllCorrect=iscorrect)
        useranswer.save()

        for guess, solution in zip(gaps, cloze.gaps):

            if guess in solution.solutions: 
                count += 1
                singleuseranswer = SingleFieldClozeUserAnswer(Correct=True, ExpectedAnswer=solution, UserAnswer=guess, AllGaps=useranswer)
                singleuseranswer.save()
            else:
                singleuseranswer = SingleFieldClozeUserAnswer(Correct=False, ExpectedAnswer=solution, UserAnswer=guess, AllGaps=useranswer)
                singleuseranswer.save()
                iscorrect, message = False, "Your answer is wrong." 
        
        useranswer.AllCorrect = iscorrect
        useranswer.save()

        message += " You answered {}/{} gaps correctly.".format(count, maximal)

        return HttpResponse(message)
    else:
        qaw = Cloze.objects.first().qaw #TODO fix this
        print(qaw)
        cloze = c.from_model(qaw)

        cloze_form = ClozeForm(len(cloze.gaps), initial={'cloze_id': qaw.id,}, )
        cloze_items = []

        for i, gap in enumerate(cloze.gaps):
            cloze_items.extend([gap.preceeding_text, cloze_form[ClozeForm.get_gap_key(i)], gap.succeeding_text, ])

        return render(request, 'cloze_text.html',  {'cloze_items': cloze_items, 'form': cloze_form, "NameID": str(cat), "Target": qaw.Target})

def generateTruthTables(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            iscorrect, message, correctcounter = True, "Your answer is correct.", 0
            postresult = dict(request.POST)
            checklist = [i['Answer'] for i in Answer.objects.filter(Set__NameID=(str(cat))).values()]
            postresult.pop('csrfmiddlewaretoken')
            postresult.pop('NameID')
            useranswer = TruthTableUserAnswer(Topic=str(cat), AllCorrect=iscorrect)
            useranswer.save()

            for k, v in postresult.items():
                if k in checklist:
                    correctcounter += 1
                    singleuseranswer = SingleTruthTableUserAnswer(Correct=True, Answer=v[0], Question=k, AllAnswers=useranswer)
                    singleuseranswer.save()
                else:
                    singleuseranswer = SingleTruthTableUserAnswer(Correct=False, Answer=v[0], Question=k, AllAnswers=useranswer)
                    singleuseranswer.save()
                    iscorrect, message = False, "Your answer is wrong."

            useranswer.AllCorrect = iscorrect
            useranswer.save()

            message += " You answered {}/{} statements correctly.".format(correctcounter, k+1)
           
            return render(request, 'truthtableexample.html', {'message': message})
        else:
            answerset = Answer.objects.filter(Set__NameID=(str(cat)))
            wrongstatementsset = WrongStatements.objects.filter(Set__NameID=(str(cat)))

            countstatements = 3
            countanswers = generateNumbers(countstatements, 1)[0]

            answernumbers = sample(range(0, answerset.count()), countanswers)
            wrongstatementsnumbers = sample(range(0, wrongstatementsset.count()), countstatements - countanswers)
            
            statements = [str(answerset[i]) for i in answernumbers]
            statements += [str(wrongstatementsset[i]) for i in wrongstatementsnumbers]

            shuffle(statements)

            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            answerform = TtAnswerForm(initial={'Categorie': (str(cat)), 'Options': statements})
            return render(request, 'truthtableexample.html', {'Form': answerform, 'Categorie': (str(cat)), 'Target': target})
    except Exception as error:
        print(error)
    return redirect('homeview')

def generateGateQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            iscorrect, message = True, "Your answer is correct."
            
           
            return render(request, 'gates.html', {'message': message})
        else:

            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            answerform = GatesAnswerForm(initial={'Categorie': (str(cat))})
            return render(request, 'gates.html', {'Form': answerform, 'Categorie': (str(cat)), 'Target': target})
    except Exception as error:
        print(error)
    return redirect('homeview')

def generateOpenAssemblerQuestions(request):
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            answer_text, correct = "Your answer is wrong.", False
            form = OpenAssemblerAnswerForm(request.POST)
            if form.is_valid():
                usercode = form.cleaned_data['CodeAnswer'].replace("\r", "")
                parsed = parser(usercode)
                parsed.eval()
                AssemblerQuestion = OpenAssemblerCodeQuestions.objects.filter(Set__NameID=(str(cat)))[0]
                answerdict = json.loads(AssemblerQuestion.RegisterAnswer)
                if (AssemblerQuestion.CheckNeededInstructions):
                    n_instructions = list(filter(lambda i: len(i), AssemblerQuestion.NeededInstructions.split(",")))
                    parsed.checkForStatement(n_instructions)
                    correct = (parsed.equalsState(answerdict) and parsed.hasMissingInstructions())
                    if correct:
                        answer_text = "Your answer is correct and you used all needed instructions."
                    else:
                        answer_text = "Your answer might be correct but you missed some needed instructions. Needed Instructions: {}".format(str(AssemblerQuestion.NeededInstructions).rstrip(','))
                else:
                    correct = parsed.equalsState(answerdict)
                    answer_text = "Your answer is correct."
                useranswer = OpenAssemblerAnswer(
                    Question=AssemblerQuestion.Question,
                    Answer=usercode,
                    Correct=correct
                )
                useranswer.save()
                return render(request, 'openassembler.html', {'message': answer_text, 'correct': correct})
            return render(request, 'openassembler.html', {'message': "Cannot handle your request!", 'correct': correct})
        else:
            AssemblerQuestion = OpenAssemblerCodeQuestions.objects.filter(Set__NameID=(str(cat)))[0]
            Target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            answerform = OpenAssemblerAnswerForm(initial={'Question': AssemblerQuestion.Question})
            return render(request, 'openassembler.html', {'Form': answerform, 'Categorie': (str(cat)), 'Target': Target, 'Question': AssemblerQuestion.Question,})
    except Exception as error:
        print(error)
    return redirect('homeview')

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
            answerset = [str(answer) for answer in list(Answer.objects.filter(Set__NameID='DLX-Pipeline'))]
            answerscorrection = [ans in answerset for ans in answers]
            if False in answerscorrection or len(answerscorrection) < 1:
                message = "Your answer is wrong."
            else:
                message = "Your answer is correct."
            return render(request, 'multiplechoiceexample.html', {'message': message})
        else:
            questionsset = Question.objects.filter(Set__NameID='DLX-Pipeline')
            answerset = Answer.objects.filter(Set__NameID='DLX-Pipeline')
            wrongstatementsset = WrongStatements.objects.filter(Set__NameID='DLX-Pipeline')
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

            answerform = MCAnswerForm(initial={'Question': question_f, 'Categorie': 'DLX-Pipeline', 'Options': statements_f})
            return render(request, 'multiplechoiceexample.html', {'Form': answerform, 'Question': question_f, 'Categorie': 'DLX-Pipeline'})
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

def generateDragNDropExample(request):
    try:
        return render(request, 'dragndropexample.html')
    except Exception as error:
        print(error)
        return render(request, 'multiplechoiceexample.html')


################################################
################ Testing #######################
################################################

def returnMasterTemplate(request):
    return render(request, 'master.html')