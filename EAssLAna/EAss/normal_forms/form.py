from django import forms
from parsec import ParseError

from .parser import disjunctive_normal_form, conjunctive_normal_form
from .normal_form import DISJUNCTION, CONJUNCTION, Guess


PARSERS = {
    CONJUNCTION: conjunctive_normal_form,
    DISJUNCTION: disjunctive_normal_form,
}


class NormalForm(forms.Form):
    guess = forms.CharField(label_suffix=" = ", required=False)

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._question = question
        guess = self.fields['guess']
        guess.label = question.function.result_name

    def clean_guess(self):
        value = self.cleaned_data['guess']
        try:
            parser = PARSERS[self._question.normal_form](self._question.function.variables)
            normal_form = parser.parse_strict(value)
            return Guess(self._question, normal_form)

        except ParseError as e:
            raise forms.ValidationError(str(e))
