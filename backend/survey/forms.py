from django import forms


class AnswerChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

        if question:
            choices = question.choice_list.all()
            if choices.exists():
                self.fields['selected_choice'] = forms.ChoiceField(
                    label=question.text,
                    choices=[(choice.id, choice.text) for choice in choices],
                    widget=forms.RadioSelect(),
                    required=True
                )
            else:
                self.fields['selected_choice'] = forms.CharField(
                    label=question.text,
                    required=True,
                    widget=forms.TextInput()
                )
