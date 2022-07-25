import urllib.parse
import json
import pytz

from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from datetime import datetime, timedelta

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
from .gates import createcircuit
from .binarys import getBinaryCalcList


from . import cloze as c

################################################
################# General ######################
################################################

def index(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        topics, data = ['Computer-Models', 'Gates', 'Calculus', 'Optimization', 'Assembler', 'Quantencomputing'], {}

        for topic in topics:
            data[topic.replace("-", "")] = assets if (assets := QAWSet.objects.filter(Topic=topic)) is not None and len(assets) else []

        return render(request, 'index.html', data)
    except Exception as error:
        print(error)
    return redirect('homeview')


def calculateTimeDuration(start_time,end_time):
    tz = pytz.timezone('Europe/Berlin')
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')

    start_time = start_time.replace(tzinfo=None)
    end_time = end_time.replace(tzinfo=None)

    seconds = int((end_time-start_time).total_seconds())

    return (end_time-start_time).total_seconds()


################################################
############### Generator ######################
################################################

# check?
def generateOctaQuestions(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            endtime = datetime.now()
            NameID = ""
            duration = ""
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")
            answers = []

            for element in raw_request_split:
                if element.startswith("NameID="):
                    NameID += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   
                if element.startswith("BeginTime="):
                    beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))

            iscorrect, message = False, "You answer is wrong"
            question = int(request.POST['Question'])
            answer = int(request.POST['Answer'], 10)
            if question == answer:
                iscorrect, message = True, "Your answer is correct."
            qaw_set = QAWSet.objects.get(NameID=NameID)
            useranswer = CalculusSingleUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set,Answer=answer, UserID=request.user.id, Correct=iscorrect, Question=question, CalcType="Octa")
            useranswer.save()
            return render(request, 'octarandexample.html', {'message': message, 'correct': iscorrect})
        else: 
            octaex = OctaStatement.objects.filter(Set__NameID=(str(cat)))[0]
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            expression = randint(5, octaex.MaxValue)
            expression = format(expression, "o")

            beginTime = timezone.now()
            answerform = OctaAnswerForm(initial={'Question': expression, 'BeginTime': beginTime, 'NameID': (str(cat))})
            return render(request, 'octarandexample.html', {'octacode': expression, "Form": answerform, "Target": target})
    except Exception as error:
        print(error)
    return redirect('homeview')

## Link: https://stackoverflow.com/questions/5920643/add-an-item-between-each-item-already-in-the-list
#check?
def generateBinaryQuestions(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            endtime = datetime.now()
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")
            NameID = ""
            for element in raw_request_split:
                if element.startswith("NameID="):
                    NameID = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   
                if element.startswith("BeginTime="):
                    beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))

            iscorrect, message = False, "You answer is wrong"
            question = int(request.POST['Question'], 2)
            answer = int(request.POST['Answer'], 10)
            useranswerlist, questionslist = getBinaryCalcList(format(answer, "b")), getBinaryCalcList(format(question, "b"))
            useranswerlist = sum([[i, '+'] for i in useranswerlist], [])[:-1]
            questionslist = sum([[i, '+'] for i in questionslist], [])[:-1]
            if question == answer:
                iscorrect, message = True, "Your answer is correct."
            
            qaw_set = QAWSet.objects.get(NameID=NameID)
            useranswer = CalculusSingleUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id, Answer=answer, Correct=iscorrect, Question=question, CalcType="Bin")
            useranswer.save()
            data = {
                'message': message, 
                'correct': iscorrect, 
                "solution": int(request.POST['Question'], 2),
                "Usercalc": useranswerlist,
                "Solution": questionslist,
                "BinarySolution": format(question, "b"),
                "BinaryAnswer": format(answer, "b"),
                "NonBinarySolution": answer
                }
            return render(request, 'binaryrandexample.html', data)
        else: 
            binex = BinaryStatement.objects.filter(Set__NameID=(str(cat)))[0]
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            expression = randint(5, binex.MaxValue)
            expression = format(expression, "b")

            beginTime = timezone.now()
            answerform = BinaryAnswerForm(initial={'Question': expression, 'BeginTime': beginTime, 'NameID': (str(cat))})
            return render(request, 'binaryrandexample.html', {'binarycode': expression, "Form": answerform, "Target": target})
    except Exception as error:
        print(error)
    return redirect('homeview')

#CHECK
def generateSCQuestions(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            endtime = datetime.now()
            iscorrect, message = True, "Your answer is correct."
            question = ""
            NameID = ""
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")
            answers = []

            for element in raw_request_split:
                if element.startswith("Options_q="):
                    answers.append(urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Options_q=", ""))))
                if element.startswith("Question="):
                    question += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Question=", "")))
                if element.startswith("NameID="):
                    NameID += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   
                if element.startswith("BeginTime="):
                    beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))
                   

            answerset = [str(answer) for answer in list(Answer.objects.filter(Set__NameID=(str(cat))))]
            answerscorrection = [ans in answerset for ans in answers]

            if False in answerscorrection or len(answerscorrection) < 1:
                iscorrect, message = False, "Your answer is wrong."
            qaw_set = QAWSet.objects.get(NameID=NameID)

            useranswer = SingleChoiceUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id, Answer=answers[0], Correct=iscorrect, Question=question, Topic=str(cat))
            useranswer.save()

            return render(request, 'singlechoiceexample.html', {'message': message, 'correct':iscorrect})
        else:
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            beginTime = timezone.now()
            questionsset = Question.objects.filter(Set__NameID=(str(cat)))
            #qaw_set = QAWSet.objects.filter(NameID=(str(cat)))
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

            answerform = SCAnswerForm(initial={'Question': question_f, 'BeginTime': beginTime, 'NameID': (str(cat)), 'Options': statements_f})
            return render(request, 'singlechoiceexample.html', {'Form': answerform, 'Question': question_f, 'Categorie': (str(cat)), 'Target': target})
    except Exception as error:
        print(error)
    return redirect('homeview')

# check?
def generateMCQuestions(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            endtime = datetime.now()
            iscorrect, message = True, "Your answer is correct."
            question = ""
            NameID = ""
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")
            answers = []

            for element in raw_request_split:
                if element.startswith("Options_q="):
                    answers.append(urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Options_q=", ""))))
                if element.startswith("Question="):
                    question += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Question=", "")))
                if element.startswith("NameID="):
                    NameID += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   
                if element.startswith("BeginTime="):
                    beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))

            answerset = [str(answer) for answer in list(Answer.objects.filter(Set__NameID=(str(cat))))]
            qaw_set = QAWSet.objects.get(NameID=NameID)
            
            useranswer = MultipleChoiceUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id, AllCorrect=iscorrect, Question=question, Topic=str(cat))
            useranswer.save()

            answercorrect = False
            correctcounter = 0
            for index, element in enumerate(answers):
                if element in answerset:
                    answercorrect = True
                    correctcounter += 1
                else:
                    iscorrect, message = False, "Your answer is wrong."
                singleuseranswer = SingleMultipleChoiceUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id, Correct=answercorrect, Answer=element, AllAnswers=useranswer, Topic=str(cat))
                singleuseranswer.save()

            useranswer.AllCorrect = iscorrect
            useranswer.save()

            message += " You answered {}/{} statements correctly.".format(correctcounter, index+1)
    
            return render(request, 'multiplechoiceexample.html', {'message': message, 'correct':iscorrect})
        else:
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            questionsset = Question.objects.filter(Set__NameID=(str(cat)))
            beginTime = timezone.now()
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
        
            answerform = MCAnswerForm(initial={'Question': question_f, 'BeginTime': beginTime, 'NameID': (str(cat)), 'Options': statements_f})
            return render(request, 'multiplechoiceexample.html', {'Form': answerform, 'Question': question_f, 'Categorie': (str(cat)), 'Target': target})
    except Exception as error:
        print(error)
    return redirect('homeview')

######
def clozeTextGenerator(request):
    if not request.user.is_authenticated:
        return redirect("/")

    cat = request.GET.get('t', '')
    if request.method == 'POST':
        endtime = datetime.now()
        iscorrect, message = True, "Your answer is correct."
        NameID = ""

        raw_request = request.body.decode("UTF-8")
        raw_request_split = raw_request.split("&")


        for element in raw_request_split:

            if element.startswith("NameID="):
                NameID = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   
            if element.startswith("BeginTime="):
                beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))


        qaw_set = QAWSet.objects.get(NameID=NameID)
        cloze = c.from_model(qaw_set)

        gaps = [request.POST[ClozeForm.get_gap_key(i)] for i in range(len(cloze.gaps))]
        maximal, count = len(cloze.gaps), 0

        useranswer = ClozeUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id,Topic=str(cat), AllCorrect=iscorrect)
        useranswer.save()

        for guess, solution in zip(gaps, cloze.gaps):

            if guess in solution.solutions: 
                count += 1
                singleuseranswer = SingleFieldClozeUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id,Correct=True, ExpectedAnswer=solution, UserAnswer=guess, AllGaps=useranswer)
                singleuseranswer.save()
            else:
                singleuseranswer = SingleFieldClozeUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id,Correct=False, ExpectedAnswer=solution, UserAnswer=guess, AllGaps=useranswer)
                singleuseranswer.save()
                iscorrect, message = False, "Your answer is wrong." 
        
        useranswer.AllCorrect = iscorrect
        useranswer.save()

        message += " You answered {}/{} gaps correctly.".format(count, maximal)

        return HttpResponse(message)
    else:
        qaw = Cloze.objects.first().qaw #TODO fix this

        cloze = c.from_model(qaw)
        beginTime = timezone.now()

        cloze_form = ClozeForm(len(cloze.gaps), initial={'cloze_id': (str(cat)),'BeginTime': beginTime, 'NameID': (str(cat))}, )
        cloze_items = []

        for i, gap in enumerate(cloze.gaps):
            cloze_items.extend([gap.preceeding_text, cloze_form[ClozeForm.get_gap_key(i)], gap.succeeding_text, ])

        return render(request, 'cloze_text.html',  {'cloze_items': cloze_items, 'form': cloze_form, "NameID": (str(cat)), "Target": qaw.Target})

def generateTruthTables(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            endtime = datetime.now()
            iscorrect, message, correctcounter = True, "Your answer is completely correct.", 0
            
            checklist = [i['Answer'] for i in Answer.objects.filter(Set__NameID=(str(cat))).values()]
            checklist2 = [i['Statement'] for i in WrongStatements.objects.filter(Set__NameID=(str(cat))).values()]

            NameID = ""
            question_f = ""
            qanswer = ""
            statistic = ""
            lastanswer = ""
            lastanswerdate = ""
            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")

            for element in raw_request_split:
                if element.startswith("NameID="):
                    NameID = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   
                if element.startswith("BeginTime="):
                    beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))
                if element.startswith("Question="):
                    question_f = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Question=", "")))

            qaw_set = QAWSet.objects.get(NameID=NameID)

            useranswer = TruthTableUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id, Topic=str(cat), AllCorrect=iscorrect, Question=question_f)
            useranswer.save()

            for i in range(1, 4):
                y = raw_request_split[i]
                x = urllib.parse.unquote_plus(urllib.parse.unquote(y)).split("=")
                if SingleTruthTableUserAnswer.objects.filter(UserID=request.user.id, Statement=x[0]).exists():
                    lastanswer += str((SingleTruthTableUserAnswer.objects.filter(UserID=request.user.id, Statement=x[0]).order_by('Solved'))[0].Answer) + ";"
                    lastanswerdate += str((SingleTruthTableUserAnswer.objects.filter(UserID=request.user.id, Statement=x[0]).order_by('Solved'))[0].Solved) + ";"
                else:
                    lastanswer += "not answered yet;"
                    lastanswerdate += "not answered yet;"
                if x[0] in checklist and x[1] == "True":       
                    correctcounter += 1
                    qanswer += x[0] + "=" + x[1] + "=" "True" + ";"
                    singleuseranswer = SingleTruthTableUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime, Set=qaw_set, UserID=request.user.id, Correct=True, Answer=x[1], Statement=x[0], Expectedanswer="False", AllAnswers=useranswer, Topic=str(cat))
                    singleuseranswer.save()
                elif x[0] in checklist2 and x[1] == "False": 
                    correctcounter += 1
                    qanswer += x[0] + "=" + x[1] + "=" "False" + ";"
                    singleuseranswer = SingleTruthTableUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime, Set=qaw_set, UserID=request.user.id, Correct=True, Answer=x[1], Statement=x[0], Expectedanswer="False", AllAnswers=useranswer, Topic=str(cat))
                    singleuseranswer.save()
                else:
                    eanswer = "False"
                    if x[0] in checklist:
                       eanswer = "True"
                    iscorrect, message = False, "Your answer partly is wrong."
                    qanswer += x[0] + "=" + x[1] + "=" "False" + ";"
                    singleuseranswer = SingleTruthTableUserAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime, Set=qaw_set, UserID=request.user.id, Correct=False, Answer=x[1], Statement=x[0], Expectedanswer=eanswer, AllAnswers=useranswer, Topic=str(cat))
                    singleuseranswer.save()
                statistic += str(SingleTruthTableUserAnswer.objects.filter(UserID=request.user.id, Statement=x[0], Answer="True").count()) + "=" + str(SingleTruthTableUserAnswer.objects.filter(UserID=request.user.id, Statement=x[0], Answer="False").count()) + ";"

            if correctcounter == 0:
                message = "Your answer is partly correct." 
            qanswer = qanswer[:-1]
            statistic = statistic[:-1]
            lastanswer = lastanswer[:-1]
            lastanswerdate = lastanswerdate[:-1]
            
            useranswer.AllCorrect = iscorrect
            useranswer.save()

            message += " You answered {}/{} statements correctly.".format(correctcounter, "3")
           
            return render(request, 'truthtableexample.html', {'message': message, 'Question': question_f, 'Qanswer': qanswer, 'correct': iscorrect, 'Statistic': statistic, 'Lastanswer': lastanswer, 'Lastanswerdate': lastanswerdate})
        else:
            hint = ""
            qanswer = ""
            questionsset = Question.objects.filter(Set__NameID=(str(cat)))
            question = randint(0, questionsset.count() - 1)
            question_f = questionsset[question]
            beginTime = timezone.now()
            answerset = Answer.objects.filter(Set__NameID=(str(cat)))
            wrongstatementsset = WrongStatements.objects.filter(Set__NameID=(str(cat)))

            countstatements = 3
            countanswers = generateNumbers(countstatements, 1)[0]

            answernumbers = sample(range(0, answerset.count()), countanswers)
            wrongstatementsnumbers = sample(range(0, wrongstatementsset.count()), countstatements - countanswers)
            
            statements = [str(answerset[i]) for i in answernumbers]
            statements += [str(wrongstatementsset[i]) for i in wrongstatementsnumbers]

            shuffle(statements)

            for x in statements:
                if Answer.objects.filter(Answer=(str(x))).exists():
                    hint += str(Answer.objects.get(Answer=(str(x))).Hint) + ";"
                else:
                    hint += str(WrongStatements.objects.get(Statement=(str(x))).Hint) + ";"
            hint = hint[:-1]

            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            answerform = TtAnswerForm(initial={'NameID': (str(cat)), 'BeginTime': beginTime,  'Options': statements, 'Question': question_f, 'Hint': hint, 'Qanswer': qanswer})
            return render(request, 'truthtableexample.html', {'Form': answerform, 'Categorie': (str(cat)), 'Target': target, 'Question': question_f, 'Hint': hint, 'Qanswer': qanswer})
    except Exception as error:
        print(error)
    return redirect('homeview')

def generateGateQuestions(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            endtime = datetime.now()
            iscorrect, message = False, "Answer for result and circuitfunction are both wrong"
            inputq = ""
            question = ""
            expectedanswer = ""
            answer = ""
            imgpath = ""
            expectedcircuitfunction = ""
            answercircuitfunction = ""
            NameID = ""

            raw_request = request.body.decode("UTF-8")
            raw_request_split = raw_request.split("&")          

            for element in raw_request_split:
                if element.startswith("Question="):
                    question += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Question=", "")))
                if element.startswith("Imgpath="):
                    imgpath += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Imgpath=", "")))
                if element.startswith("Expectedanswer="):
                    expectedanswer += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Expectedanswer=", "")))
                if element.startswith("Gateanswer="):
                    answer += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Gateanswer=", "")))
                if element.startswith("Expectedcircuitfunction="):
                    expectedcircuitfunction += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Expectedcircuitfunction=", "")))
                if element.startswith("Answerircuitfunction="):
                    answercircuitfunction += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Answerircuitfunction=", "")))
                if element.startswith("Input="):
                    inputq += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("Input=", "")))
                if element.startswith("NameID="):
                    NameID += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   
                if element.startswith("BeginTime="):
                    beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))

            if expectedanswer == answer and expectedcircuitfunction == answercircuitfunction:
                iscorrect = True
                message = "Answer for result and circuitfunction are both correct"
            if expectedanswer == answer and expectedcircuitfunction != answercircuitfunction:
                iscorrect = False
                message = "Answer for result is correct but circuitfunction is wrong"
            elif expectedanswer != answer and expectedcircuitfunction == answercircuitfunction:
                iscorrect = False
                message = "Answer for result is wrong but circuitfunction is correct"
            elif expectedanswer != answer and expectedcircuitfunction != answercircuitfunction:
                iscorrect = False

            qaw_set = QAWSet.objects.get(NameID=NameID)
            useranswer = GatesAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set, UserID=request.user.id, Expectedanswer=expectedanswer, Answer=answer, Correct=iscorrect, Question=question, Topic="Gates", Imgpath=imgpath, Expectedcircuitfunction=expectedcircuitfunction, Answerircuitfunction=answercircuitfunction, Input=inputq)
            useranswer.save()
            return render(request, 'gates.html', {'message': message, 'correct': iscorrect, 'Question': question, 'Expectedanswer': expectedanswer, 'Gateanswer':answer, 'Imgpath':imgpath, 'Expectedcircuitfunction':expectedcircuitfunction, 'Answerircuitfunction':answercircuitfunction, 'Input': inputq})
        else:
            questionsset = Question.objects.filter(Set__NameID=(str(cat)))
            question = randint(0, questionsset.count() - 1)
            question_f = questionsset[question]
            beginTime = timezone.now()
            target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            difficulty = (QAWSet.objects.filter(NameID=(str(cat))))[0].Difficulty
            imgpath, result, circuitfunction, input = createcircuit(difficulty)

            answerform = GatesAnswerForm(initial={'Question': question_f, 'NameID': (str(cat)), 'BeginTime': beginTime, 'Categorie': (str(cat)), 'Expectedanswer': result, 'Expectedcircuitfunction': circuitfunction, 'Imgpath': imgpath, "Input": input})
            return render(request, 'gates.html', {'Form': answerform, 'Categorie': (str(cat)), 'Target': target, 'Imgpath': imgpath, 'Question': question_f, "Input": input})
    except Exception as error:
        print(error)
    return redirect('homeview')

def generateOpenAssemblerQuestions(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        cat = request.GET.get('t', '')
        if request.method == "POST":
            endtime = datetime.now()
            correct, n_instructions = False, ""
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
                    n_instructions = ','.join(parsed.getMissingInstructions())
                    correct = (parsed.equalsState(answerdict) and parsed.hasMissingInstructions())

                NameID = ""
                raw_request = request.body.decode("UTF-8")
                raw_request_split = raw_request.split("&")

                for element in raw_request_split:

                    if element.startswith("NameID="):
                        NameID += urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("NameID=", "")))   
                    if element.startswith("BeginTime="):
                        beginTime = urllib.parse.unquote_plus(urllib.parse.unquote(element.replace("BeginTime=", "")))

                qaw_set = QAWSet.objects.get(NameID=NameID)

                correct = parsed.equalsState(answerdict)
                useranswer = OpenAssemblerAnswer(Duration=calculateTimeDuration(beginTime,endtime), Solved=endtime,Set=qaw_set,
                UserID=request.user.id,
                Question=AssemblerQuestion.Question,
                Answer=usercode,
                Correct=correct,
                QuestionID=AssemblerQuestion.id,
                OptimizedAnswer=AssemblerQuestion.OptimizedSolution)
                if len(n_instructions) > 2: useranswer.MissedStatements = n_instructions
                useranswer.save()
                
                return redirect("/learninganalytics/assembleranalysis?t={}".format(useranswer.id))
            return render(request, 'openassembler.html', {'message': "Cannot handle your request!", 'correct': correct})
        else:
            AssemblerQuestion = OpenAssemblerCodeQuestions.objects.filter(Set__NameID=(str(cat)))[0]
            Target = (QAWSet.objects.filter(NameID=(str(cat))))[0].Target
            beginTime = timezone.now()
            answerform = OpenAssemblerAnswerForm(initial={'Question': AssemblerQuestion.Question,'NameID': (str(cat)),'BeginTime': beginTime})
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