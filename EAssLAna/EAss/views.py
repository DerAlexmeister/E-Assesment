from email import message
from django.shortcuts import render

from .models import BinaryStatement
from .forms import BinaryAnswerForm

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
    