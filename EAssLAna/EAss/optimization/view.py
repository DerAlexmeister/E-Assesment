import json
from sys import flags

from django.http.response import HttpResponse
from django.http import JsonResponse

from django.shortcuts import redirect, render

from typing import Dict

from .construction import minimalByConstruction
from .karnaugh import fromTruthTable, to_json, from_json, X, Y
from ..normal_forms.normal_form import TruthTable


COLORS = frozenset({"red", "blue", "green"})


def coversOnlyOnes(karnaugh, coloring) -> bool:
    for _, indices in coloring.items():
        for y, x in indices:
            if X[x] + Y[y] not in karnaugh.ones:
                return False
    return True

def allOnesCovered(karnaugh, coloring) -> bool:
    covered = set()
    for i, y in enumerate(Y):
        for j, x in enumerate(X):
            if x + y in karnaugh.ones:
                for indices in coloring.values():
                    if [i, j] in indices:
                        covered.add((i, j))

    return len(covered) == len(karnaugh.ones)

def isRectangle(coloring) -> bool:
    for indices in coloring.values():
        for (i, j) in indices:
            for z in [
                    (i + 1 % 4, j),
                    (abs(i - 1 % 4), j),
                    (i, j + 1 % 4),
                    (i, abs(j - 1 % 4)),
            ]:
                if z not in indices:
                    return False
    return True

def isPowerOfTwo(coloring) -> bool:
    pass

def isMinimal(coloring, minimum) -> bool:
    pass


def coloring(request):
    cat = request.GET.get('t', '')

    if request.method == 'POST':
        data = json.loads(request.body)

        karnaugh = from_json(data["problem"])
        coloring = data["coloring"]
        if not coversOnlyOnes(karnaugh, coloring):
            return HttpResponse("Cover only 1s!")
        if not allOnesCovered(karnaugh, coloring):
            return HttpResponse("Each 1 must be covered by at least one color!")
        #if not isRectangle(coloring):
        #    return HttpResponse("Each coloring must be a contiguous rectangle!")
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
