from django.contrib.auth.models import User
from django import forms
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, ResponseTE, ResponseMC, ResponseCB, Option

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
        exclude = ['question_num', 'question_type']
        CHOICES = (('MC', 'multiplechoice'), ('TE', 'textentry'), ('CB', 'checkbox'),)
        widgets = {
            'question_survey_Id': forms.HiddenInput(),
            'question_Id': forms.HiddenInput(),
            'question_type': forms.Select(choices=CHOICES),
            # 'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5,}),
        }


class MCQuestionForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        exclude = ['question_num', 'question_Id', 'question_survey_Id', 'question_type']
        widgets = {
            'question_title': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
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
        exclude = ['question_num', 'question_Id', 'question_survey_Id', 'question_type']
        widgets = {
            'question_title': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'question_text': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class CBQuestionForm(forms.ModelForm):
    class Meta:
        model = CBQuestion
        exclude = ['question_num', 'question_Id', 'question_survey_Id', 'question_type']
        widgets = {
            'question_title': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
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


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        exclude = ['option_Id', 'option_num', 'type_of_question']
        widgets = {
            'mc_question_Id': forms.HiddenInput(),
            'cb_question_Id': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
        }

class ResponseTEForm(forms.ModelForm):
    class Meta:
        model = ResponseTE
        exclude = ['response_Id', 'response_question_Id', 'response_survey_Id', 'response_user_Id']
        widgets = {
            'response_Id': forms.HiddenInput(),
            'response_question_Id': forms.HiddenInput(),
            'response_survey_Id': forms.HiddenInput(),
            'response_user_Id': forms.HiddenInput(),
            'response_text': forms.Textarea(attrs={'cols': 50, 'rows':3}),
        }

FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)


class ResponseCBForm(forms.ModelForm):
    class Meta:
        model = ResponseCB
        exclude = ['response_Id', 'response_question_Id', 'response_survey_Id', 'response_user_Id']
        widgets = {
          'response_Id': forms.HiddenInput(),
          'response_question_Id': forms.HiddenInput(),
          'response_survey_Id': forms.HiddenInput(),
          'response_user_Id': forms.HiddenInput(),
          'options': forms.CheckboxSelectMultiple(choices=[])
        }

    def __init__(self, *args, **kwargs):
        super(ResponseCBForm, self).__init__(*args, **kwargs)
        if 'option_list' in kwargs:
            self.fields['options'].choices = kwargs['option_list']
        # choices = (form.instance.option_1,
#                                                                    form.instance.option_2,
#                                                                    form.instance.option_3,
#                                                                    form.instance.option_4,
#                                                                    form.instance.option_5,)


class ResponseMCForm(forms.ModelForm):
    options = forms.CheckboxSelectMultiple(choices=[("None", "None")])
    class Meta:
        model = ResponseMC
        exclude = ['response_Id', 'response_question_Id', 'response_survey_Id', 'response_user_Id']
        widgets = {
            'response_Id': forms.HiddenInput(),
            'response_question_Id': forms.HiddenInput(),
            'response_survey_Id': forms.HiddenInput(),
            'response_user_Id': forms.HiddenInput(),
            #'options': forms.CheckboxSelectMultiple(choices = [])
        }

    def __init__(self, *args, **kwargs):
        option_list = kwargs.pop('option_list', None)
        super(ResponseMCForm, self).__init__(*args, **kwargs)
        if 'option_list' is not None:
            self.fields['options'].widget = forms.CheckboxSelectMultiple(choices=option_list)