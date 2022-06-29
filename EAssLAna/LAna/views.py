from django.shortcuts import render
from django.shortcuts import redirect

def index(request):
    try:
        return render(request, 'laindex.html')
    except Exception as error:
        print(error)
    return redirect('lahomeview')
