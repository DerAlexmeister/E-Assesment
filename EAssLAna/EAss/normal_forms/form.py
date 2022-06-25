from django import forms
from parsec import ParseError
from . import normal_form as nf

from .parser import disjunctive_normal_form

class NormalForm(forms.Form):
    guess = forms.CharField(label_suffix=" = ")

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._question = question
        guess = self.fields['guess']
        guess.label = question.function.result_name

    def clean_guess(self):
        value = self.cleaned_data['guess']
        try:
            parser = disjunctive_normal_form(self._question.function.variables)
            normal_form = parser.parse(value)
            return nf.Guess(self._question, normal_form)

        except ParseError as e:
            raise forms.ValidationError(str(e))
