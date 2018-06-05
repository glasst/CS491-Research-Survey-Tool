from django.contrib.auth.models import User
from django import forms
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, DDQuestion, ResponseTE, ResponseMC, ResponseCB, ResponseDD, ResponseLK, Option, LKQuestion


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
        CHOICES = (('MC', 'multiplechoice'), ('TE', 'textentry'), ('CB', 'checkbox'), ('DD', 'dropdown'))
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
            'question_text': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'option_1': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_2': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_3': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_4': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_5': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
        }


class DDQuestionForm(forms.ModelForm):
    class Meta:
        model = DDQuestion
        exclude = ['question_num', 'question_Id', 'question_survey_Id', 'question_type']
        widgets = {
            'question_text': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'option_1': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_2': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_3': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_4': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
            'option_5': forms.Textarea(attrs={'cols': 10, 'rows': 2}),
        }


class LKQuestionForm(forms.ModelForm):
    class Meta:
        model = LKQuestion
        exclude = ['question_num', 'question_Id', 'question_survey_Id', 'question_type', "option_1", "option_2",
                   "option_3", "option_4", "option_5"]
        widgets = {
            'question_text': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'scale': forms.RadioSelect(choices=('4', '5'))
        }


class TEQuestionForm(forms.ModelForm):
    class Meta:
        model = TEQuestion
        exclude = ['question_num', 'question_Id', 'question_survey_Id', 'question_type']
        widgets = {
            'question_text': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


class CBQuestionForm(forms.ModelForm):
    class Meta:
        model = CBQuestion
        exclude = ['question_num', 'question_Id', 'question_survey_Id', 'question_type']
        widgets = {
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
        self.fields['survey_Id'] = forms.ModelChoiceField(
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


# temp override to stop validation error when checking that selected option choice matches choices in form
class ChoiceFieldNoValidation(forms.ChoiceField):
    def valid_value(self, value):
        """Check to see if the provided value is a valid choice."""
        text_value = str(value)
        for k, v in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if value == k2 or text_value == str(k2):
                        return True
            else:
                if value == k or text_value == str(k):
                    return True
        #return False
        return True


class ResponseCBForm(forms.ModelForm):
    options = ChoiceFieldNoValidation(choices=(('None', 'none'),),
                                widget=forms.CheckboxSelectMultiple())

    # def __init__(self, *args, **kwargs):
    #     question = kwargs.pop('question', None)
    #     super(ResponseCBForm, self).__init__(*args, **kwargs)
    #     self.fields['options'].widget.choices = question.get_options()

    class Meta:
        model = ResponseCB
        exclude = ['response_Id', 'response_question_Id', 'response_survey_Id', 'response_user_Id', 'response_text']
        widgets = {
          'response_Id': forms.HiddenInput(),
          'response_question_Id': forms.HiddenInput(),
          'response_survey_Id': forms.HiddenInput(),
          'response_user_Id': forms.HiddenInput(),
          'response_text': forms.HiddenInput(),
          'options': forms.CheckboxSelectMultiple(choices=[])
        }

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(ResponseCBForm, self).__init__(*args, **kwargs)
        self.fields['options'].widget.choices = question.get_options()


class ResponseMCForm(forms.ModelForm):
    options = ChoiceFieldNoValidation(choices=(('None', 'none'),),
                                widget=forms.RadioSelect)

    class Meta:
        model = ResponseMC
        exclude = ['response_Id', 'response_question_Id', 'response_survey_Id', 'response_user_Id', 'response_text']
        widgets = {
            'response_Id': forms.HiddenInput(),
            'response_question_Id': forms.HiddenInput(),
            'response_survey_Id': forms.HiddenInput(),
            'response_user_Id': forms.HiddenInput(),
            'response_text': forms.HiddenInput(),
            'options': forms.CheckboxSelectMultiple(choices=FAVORITE_COLORS_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(ResponseMCForm, self).__init__(*args, **kwargs)
        self.fields['options'].widget.choices = question.get_options()


class ResponseLKForm(forms.ModelForm):
    options = ChoiceFieldNoValidation(choices=(('None', 'none'),),
                                widget=forms.RadioSelect())

    class Meta:
        model = ResponseLK
        exclude = ['response_Id', 'response_question_Id', 'response_survey_Id', 'response_user_Id', 'response_text']
        widgets = {
            'response_Id': forms.HiddenInput(),
            'response_question_Id': forms.HiddenInput(),
            'response_survey_Id': forms.HiddenInput(),
            'response_user_Id': forms.HiddenInput(),
            'response_text': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(ResponseLKForm, self).__init__(*args, **kwargs)
        self.fields['options'].widget.choices = question.get_options()
        self.fields['options'].widget.attrs.update(display = 'inline-block')


class ResponseDDForm(forms.ModelForm):
    options = ChoiceFieldNoValidation(choices=(('None', 'none'),),
                                widget=forms.Select)

    class Meta:
        model = ResponseDD
        exclude = ['response_Id', 'response_question_Id', 'response_survey_Id', 'response_user_Id', 'response_text']
        widgets = {
            'response_Id': forms.HiddenInput(),
            'response_question_Id': forms.HiddenInput(),
            'response_survey_Id': forms.HiddenInput(),
            'response_user_Id': forms.HiddenInput(),
            'response_text': forms.HiddenInput(),
            'options': forms.Select(choices=FAVORITE_COLORS_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(ResponseDDForm, self).__init__(*args, **kwargs)
        self.fields['options'].widget.choices = question.get_options()

    #def add_choices(self):
    #    self.fields['options'].widget.choices = self.instance.get_choices()
