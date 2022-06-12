from django.http.response import HttpResponse
from django.shortcuts import render

from . import cloze as c

from .models import BinaryStatement, Cloze, QAWSet
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
    if request.method == 'POST':
        cloze_id = request.POST['cloze_id']
        qaw = QAWSet.objects.get(id=cloze_id)

        cloze = c.from_model(qaw)

        gaps = [
            request.POST[ClozeForm.get_gap_key(i)]
            for i in range(len(cloze.gaps))
        ]

        maximal = len(cloze.gaps)
        count = 0

        for guess, solution in zip(gaps, cloze.gaps):
            if guess in solution.solutions:
                count += 1

        return HttpResponse(f"{count} of {maximal} are correct.")
    else:
        qaw = Cloze.objects\
             .first()\
             .qaw
        cloze = c.from_model(qaw)

        cloze_form = ClozeForm(
            len(cloze.gaps),
            initial={
                'cloze_id': qaw.id,
            },
        )

        cloze_items = []

        for i, gap in enumerate(cloze.gaps):
            cloze_items.extend([
                gap.preceeding_text,
                cloze_form[ClozeForm.get_gap_key(i)],
                gap.succeeding_text,
            ])

        return render(request, 'cloze_text.html',  {
            'cloze_items': cloze_items,
            'form': cloze_form,
        })
