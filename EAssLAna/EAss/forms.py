from wsgiref.validate import validator
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class BinaryAnswerForm(forms.Form):
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Answer = forms.IntegerField()

class OctaAnswerForm(forms.Form):
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
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

class SCAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Options_q = forms.ChoiceField(choices=[], label="Statements")

    def __init__(self, *args, **kwargs):
        try:
            super(SCAnswerForm, self).__init__(*args, **kwargs)
            if 'initial' in kwargs.keys():
                self.fields['Options_q'].choices = (kwargs['initial'])['Options']
        except Exception as error:
            print(error)

class MCAnswerForm(forms.Form):
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())
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
    NameID = forms.CharField(max_length=1024, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        try:
            super(TtAnswerForm, self).__init__(*args, **kwargs)
            if 'initial' in kwargs.keys():
                
                for x in ((kwargs['initial'])['Options']):
                    self.fields[x] = forms.TypedChoiceField(coerce=lambda x: x =='True', choices=((False, 'Wrong'), (True, 'Right')))
           
        except Exception as error:
            print(error)

class OpenAssemblerAnswerForm(forms.Form):

    Question = forms.CharField(max_length=16384, widget=forms.HiddenInput())
    CodeAnswer = forms.CharField(max_length=16384, label=False, widget=forms.Textarea(attrs={"rows":5, "cols":20}))

class GatesAnswerForm(forms.Form):
    
    Question = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Answer = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    Expectedcircuitfunction = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Answerircuitfunction = forms.CharField(max_length=1024)
    Imgpath = forms.CharField(max_length=1024, widget=forms.HiddenInput())
    Expectedanswer = forms.IntegerField(widget=forms.HiddenInput())