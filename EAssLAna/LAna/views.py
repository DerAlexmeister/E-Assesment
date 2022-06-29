from django.shortcuts import render
from django.shortcuts import redirect

from EAss.models import CalculusSingleUserAnswer
from EAss.models import OpenAssemblerAnswer

def calcUserCIR(q_set):
    correct, incorrect = 0, 0
    for i in q_set:
        if i.Correct:
            correct += 1
        else:
            incorrect += 1
    return correct, incorrect

def index(request):
    try:
        calc_c, calc_ic = calcUserCIR(CalculusSingleUserAnswer.objects.all().order_by('-Solved'))
        ass_c, ass_ic = calcUserCIR(OpenAssemblerAnswer.objects.all().order_by('-Solved'))
        data = {
            "labels": ['Correct', 'Incorrect'], 
            "datacalc": [calc_c, calc_ic],
            "dataassembler": [ass_c, ass_ic],
        }
        print(data)
        return render(request, 'laindex.html', data)
    except Exception as error:
        print(error)
    return redirect('lahomeview')
