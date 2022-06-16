from django import forms

class BinaryAnswerForm(forms.Form):
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Answer = forms.IntegerField()

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