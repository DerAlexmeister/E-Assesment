from django import forms

class BinaryAnswerForm(forms.Form):
    Question = forms.CharField(max_length=1024)
    Answer = forms.IntegerField()


class ClozeForm(forms.Form):
    cloze_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, num_gaps: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(num_gaps):
            field_name = ClozeForm.get_gap_key(i)
            self.fields[field_name] = forms.CharField()

    @staticmethod
    def get_gap_key(index: int) -> str:
        return str(index)

class MCAnswerForm(forms.Form):
    Categorie = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Options_q = forms.MultipleChoiceField(choices=[], label="Statements")

    def __init__(self, *args, **kwargs):
        try:
            super(MCAnswerForm, self).__init__(*args, **kwargs)
            if 'initial' in kwargs.keys():
                self.fields['Options_q'].choices = (kwargs['initial'])['Options']
        except Exception as error:
            print(error)


class TtAnswerForm(forms.Form):
    

    def __init__(self, *args, **kwargs):
        try:
            super(TtAnswerForm, self).__init__(*args, **kwargs)
           
        except Exception as error:
            print(error)


