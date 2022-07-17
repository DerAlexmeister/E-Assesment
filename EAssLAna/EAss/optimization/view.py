import json
from sys import flags

from django.http.response import HttpResponse
from django.http import JsonResponse

from django.shortcuts import redirect, render

from typing import Dict

from .construction import minimalByConstruction
from .karnaugh import fromTruthTable, to_json, from_json
from ..normal_forms.normal_form import TruthTable


COLORS = frozenset({"red", "blue", "green"})



def coloring(request):
    cat = request.GET.get('t', '')

    if request.method == 'POST':
        data = json.loads(request.body)

        karnaugh = from_json(data["problem"])
        coloring = data["coloring"]

        return HttpResponse("Good!")

    else:
        variables = ["a", "b", "c", "d"]
        function = minimalByConstruction(variables, 2).evaluate()
        table = TruthTable.create(variables, "f", function)

        karnaugh = fromTruthTable(table)
        flags = {
            "input" : {
                "karnaugh": to_json(karnaugh),
            }
        }
        return render(request, 'mapcoloring.html', {
            "flags": flags
        })

def optimization(request):
    cat = request.GET.get('t', '')

    if request.method == 'POST':
        return HttpResponse("Test")
    else:
        return render(request, 'mapcreation.html', {
            "problem": {
                "function": [{
                    "0": True,
                    "1": False,
                    "2": False,
                    "3": True,
                }],
                "name": "f",
                "variables": {
                    "0": "x1",
                    "1": "x2",
                    "2": "x3",
                    "3": "x4",
                }
            }
        })
