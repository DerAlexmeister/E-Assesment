from django import forms
from parsec import ParseError

from .parser import disjunctive_normal_form

class NormalForm(forms.Form):
    guess = forms.CharField(label="Function")

    def __init__(self, variables, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parser = disjunctive_normal_form(variables)

    def clean_guess(self):
        value = self.cleaned_data['guess']
        try:
            return NormalForm(self._parser.parse_strict(value))
        except ParseError as e:
            raise forms.ValidationError(str(e))
