from django.http.response import HttpResponse

from django.shortcuts import render

from .. import models


def optimization(request):
    cat = request.GET.get('t', '')

    if request.method == 'POST':
        return HttpResponse("Test")
    else:
        return render(request, 'karnaught.html', {
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
