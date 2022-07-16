import json

from django.http.response import HttpResponse

from django.shortcuts import redirect, render

from typing import Dict

from .construction import minimalByConstruction
from .karnaugh import fromTruthTable, to_json, from_json
from ..normal_forms.normal_form import TruthTable

COLORS = frozenset({"red", "blue", "green"})


class Karnaugh:
    pass



def coloring(request):
    cat = request.GET.get('t', '')

    if request.method == 'POST':
        data = json.loads(request.body)

        karnaugh = from_json(data["problem"])

        return render(request, 'mapcoloring.html', {
            "karnaugh": to_json(karnaugh)
        })

    else:
        variables = ["a", "b", "c", "d"]
        function = minimalByConstruction(variables, 2).evaluate()
        table = TruthTable.create(variables, "f", function)

        karnaugh = fromTruthTable(table)
        return render(request, 'mapcoloring.html', {
            "karnaugh": to_json(karnaugh)
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
