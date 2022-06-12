from django.http.response import HttpResponse
from django.shortcuts import render

from .models import BinaryStatement, ClozeModel, Cloze, Gap
from .forms import BinaryAnswerForm, ClozeForm

from random import randint

def generateExample(request):
    try:
        pass
    except Exception:
        pass
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

            print(binex, binex.Length)
            
            expression = randint(5, binex.Length)
            expression = format(expression, "b")
            answerform = BinaryAnswerForm(initial={'Question': expression})
        return render(request, 'binaryrandexample.html', {'binarycode': expression, "Form": answerform})
    except Exception as error:
        print(error)
        return render(request, 'multiplechoiceexample.html')


def clozeText(request):
    cloze
    cloze = Cloze("Alphabet", [
        Gap("A, ", ", ", {"B"}),
        Gap("C, ", ", E", {"D"}),
    ])
    if request.method == 'POST':
        gaps = [request.POST[f"gap_{i}"] for i in range(len(request.POST)-1)]

        maximal = len(cloze.gaps)
        count = 0

        for guess, solution in zip(gaps, cloze.gaps):
            if guess in solution.solutions:
                count += 1

        return HttpResponse(f"{count} of {maximal} are correct.")
    else:
        #cloze = ClozeModel\
        #    .objects\
        #    .first()\
        #    .to_cloze()

        cloze_form = ClozeForm(len(cloze.gaps))
        cloze_items = []

        for gap, form in zip(cloze.gaps, cloze_form.visible_fields()):
            cloze_items.extend([
                gap.preceeding_text,
                form,
                gap.succeeding_text,
            ])

        return render(request, 'cloze_text.html',  {
            'cloze_items': cloze_items,
        })
