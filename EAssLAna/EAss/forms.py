from django import forms

class BinaryAnswerForm(forms.Form):
    Question = forms.CharField(max_length=1024)
    Answer = forms.IntegerField()