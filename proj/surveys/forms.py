from django.contrib.auth.models import User
from django import forms
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, ResponseTE

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', ]


# form class for Survey model
class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ['survey_Id', 'num_questions']
        widgets = {
            'creator_Id': forms.HiddenInput(),
        }

    #def set_creator_foreign_key(self, arg):
    #    usr = User.objects.get(username=arg)
    #    creator_Id = usr


# form class for Question model
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['question_Id', 'question_survey_Id', 'question_type', 'question_num']
        CHOICES = (('MC', 'multiplechoice'), ('TE', 'textentry'), ('CB', 'checkbox'),)
        widgets = {
            'question_survey_Id': forms.HiddenInput(),
            'question_type': forms.Select(choices=CHOICES),
            # 'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5,}),
        }


class MCQuestionForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        exclude = ['question_Id', 'question_survey_Id', 'question_type', 'question_num']
        widgets = {
            'question_survey_Id': forms.HiddenInput(),
            'question_Id': forms.HiddenInput(),
            'question_text': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'option_1': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_2': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_3': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_4': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_5': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
        }


class TEQuestionForm(forms.ModelForm):
    class Meta:
        model = TEQuestion
        exclude = ['question_Id', 'question_survey_Id', 'question_type', 'question_num']
        widgets = {
            'question_survey_Id': forms.HiddenInput(),
            'question_Id': forms.HiddenInput(),
            'question_text': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class CBQuestionForm(forms.ModelForm):
    class Meta:
        model = CBQuestion
        exclude = ['question_Id', 'question_survey_Id', 'question_type', 'question_num']
        widgets = {
            'question_survey_Id': forms.HiddenInput(),
            'question_Id': forms.HiddenInput(),
            'question_text': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'option_1': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_2': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_3': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_4': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_5': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
        }


class TakeSurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TakeSurveyForm, self).__init__(*args, **kwargs)
        self.fields['survey_to_take'] = forms.ModelChoiceField(
            queryset=Survey.objects.filter(creator_Id__username=self.user))
