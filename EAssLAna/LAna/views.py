from datetime import datetime, timedelta, time

from django.shortcuts import render
from django.shortcuts import redirect

from EAss.models import CalculusSingleUserAnswer
from EAss.models import OpenAssemblerAnswer

from EAss.assembly import parser

from EAss.models import QAWSet

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

def equalizeLists(alist, blist):
    try:
        if len(alist) < len(blist):
            for _ in range(len(blist) - len(alist)):
                alist.append({None: None})
        elif len(alist) > len(blist):
            for _ in range(len(alist) - len(blist)):
                blist.append({None: None})
        else:
            return alist, blist
    except Exception as error:
        print(">> ", error)
    return alist, blist

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
            o_status, u_states = equalizeLists(o_status, u_states)
            if answer.MissedStatements:
                for i in str(answer.MissedStatements).split(","):
                    if len(i) > 2: u_missing.append(i)
            for i in zip(u_states, o_status):
                if i[0] is not None and i[1] is not None:
                    for i in zip(i[0].values(), i[1].values()):
                        if i[0] == i[1]:
                            stateequal.append(True)
                        elif i[0] != i[1] and answer.Correct:
                            stateequal.append(None)
                        else:
                            stateequal.append(False)
            for i, v in enumerate(stateequal):
                u_states[i]['Com'] = v
            list_of_user_inst, list_of_opt_inst = len(u_parsed.getCode()), len(o_parsed.getCode())
            number_of_used_reg_user, number_of_used_reg_opt = len(u_parsed.getLastStates()), len(o_parsed.getLastStates())
            data = {
                "AssemblerAnswer": answer, 
                "States": zip(o_status, u_states), 
                "MissingInstructions": u_missing, 
                "InstructionCycles": (list_of_user_inst*5, list_of_opt_inst*5),
                "NumberOfUsedRegs": [number_of_used_reg_user, number_of_used_reg_opt],
                "NumberOfUsedRegsLabels": ["User", "Solution"],
                "NumberOfUsedInst": [list_of_user_inst, list_of_opt_inst],
                "NumberOfUsedInstLabel": ["User", "Solution"],
                }
            return render(request, 'assemblerdetails.html', data)
        else:
            data = {"AssemblerAnswers": OpenAssemblerAnswer.objects.all().order_by('-Solved'),}
            return render(request, 'assemblerov.html', data)
    except Exception as error:
        print(error)
    return redirect('lahomeview')

def index(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
      


        return render(request, 'laindex.html', data)
    except Exception as error:
        print(error)
    return redirect('lahomeview')

def index(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        topics, data = ['Computer-Models', 'Gates', 'Calculus', 'Optimization', 'Assembler', 'Quantencomputing'], {}

        for topic in topics:
            data[topic.replace("-", "")] = assets if (assets := QAWSet.objects.filter(Topic=topic)) is not None and len(assets) else []



        if request.user.is_superuser:
            user = "Teacher"
        else:
            user = request.user.id

        data["labels"] = ['Correct', 'Incorrect']
        data["user"] = user
        return render(request, 'laindex.html', data)
    except Exception as error:
        print(error)
    return redirect('lahomeview')
