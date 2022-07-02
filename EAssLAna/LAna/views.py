from django.shortcuts import render
from django.shortcuts import redirect

from EAss.models import CalculusSingleUserAnswer
from EAss.models import OpenAssemblerAnswer

from EAss.assembly import parser

def assemblerAnalysis(request):
    try:
        pass
    except Exception as error:
        pass

def calcUserCIR(q_set):
    correct, incorrect = 0, 0
    for i in q_set:
        if i.Correct:
            correct += 1
        else:
            incorrect += 1
    return correct, incorrect

def radarGraph():
    try:
        pass
    except Exception as error:
        pass

def handleAssemblerAnalytics(request):
    try:
        target = request.GET.get('t', '')
        if request.method == "GET" and target != '':
            answer = OpenAssemblerAnswer.objects.get(id=target)
            u_parsed = parser(answer.Answer)
            u_parsed.eval()
            u_states = u_parsed.getStates()
            o_parsed, o_status, u_missing, stateequal = None, None, [], []
            if answer.OptimizedAnswer:
                o_parsed = parser(answer.OptimizedAnswer)
                o_parsed.eval()
                o_status = o_parsed.getStates()
            if answer.MissedStatements:
                for i in str(answer.MissedStatements).split(","):
                    if len(i) > 2: u_missing.append(i)
            for i in zip(u_states, o_status):
                for i in zip(i[0].values(), i[1].values()):
                    if i[0] == i[1]:
                        stateequal.append(True)
                    elif i[0] != i[1] and answer.Correct:
                        stateequal.append(None)
                    else:
                        stateequal.append(False)
            for i, v in enumerate(stateequal):
                u_states[i]['Com'] = v 
            print(u_states)
            data = {"AssemblerAnswer": answer, "States": zip(o_status, u_states), "MissingInstructions": u_missing,}
            return render(request, 'assemblerdetails.html', data)
        else:
            data = {"AssemblerAnswers": OpenAssemblerAnswer.objects.all().order_by('-Solved'),}
            return render(request, 'assemblerov.html', data)
    except Exception as error:
        print(error)
    return redirect('lahomeview')

def index(request):
    try:
        calc_c, calc_ic = calcUserCIR(CalculusSingleUserAnswer.objects.all().order_by('-Solved'))
        ass_c, ass_ic = calcUserCIR(OpenAssemblerAnswer.objects.all().order_by('-Solved'))
        data = {
            "labels": ['Correct', 'Incorrect'], 
            "datacalc": [calc_c, calc_ic],
            "dataassembler": [ass_c, ass_ic],
        }
        return render(request, 'laindex.html', data)
    except Exception as error:
        print(error)
    return redirect('lahomeview')
