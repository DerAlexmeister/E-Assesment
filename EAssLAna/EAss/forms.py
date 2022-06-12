from django import forms

class BinaryAnswerForm(forms.Form):
    Question = forms.CharField(max_length=1024)
    Answer = forms.IntegerField()


class ClozeForm(forms.Form):
    def __init__(self, num_gaps: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gaps = []
        for i in range(num_gaps):
            field_name = f"gap_{i}"
            gap = forms.CharField()
            self.gaps.append(gap)
            self.fields[field_name] = gap
