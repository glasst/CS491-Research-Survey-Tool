from django.db import models
from django import forms
import uuid


class User(models.Model):
        user_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
        username = models.CharField(max_length=45)
        email = models.CharField(max_length=255)
        password = models.CharField(max_length=32)
        create_time = models.DateTimeField(auto_now=True)
        first_name = models.CharField(max_length=45)
        last_name = models.CharField(max_length=45)
        role = models.CharField(max_length=1)

class Survey(models.Model):
	survey_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	creator_Id = models.ForeignKey(User, on_delete=models.PROTECT)

class Question(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	question_survey_Id = models.ForeignKey(Survey, on_delete=models.PROTECT)
	question_type = models.CharField(max_length=20)
	question_text = models.CharField(max_length=400)

class MCQuestion(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	question_text = models.CharField(max_length=400)
	option_1 = models.CharField(max_length=100)
	option_2 = models.CharField(max_length=100)
	option_3 = models.CharField(max_length=100)
	option_4 = models.CharField(max_length=100)
	option_5 = models.CharField(max_length=100)
class TEQuestion(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	question_text = models.CharField(max_length=400)
class CBQuestion(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	question_text = models.CharField(max_length=400)
	option_1 = models.CharField(max_length=100)
	option_2 = models.CharField(max_length=100)
	option_3 = models.CharField(max_length=100)
	option_4 = models.CharField(max_length=100)
	option_5 = models.CharField(max_length=100)

class Response(models.Model):
	response_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	response_question_Id = models.ForeignKey(Question, on_delete=models.PROTECT)
	#response_question_type = models.ForeignKey(Questions, on_delete=models.PROTECT)
	response_survey_Id 	= models.ForeignKey(Survey, on_delete=models.PROTECT)
	response_user_Id = models.ForeignKey(User, on_delete=models.PROTECT)
	response_text = models.CharField(max_length=400)


#create a form class for Questions model
class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		#exclude = ['question_Id', 'question_survey_Id']
		fields = '__all__'
		CHOICES = (('MC', 'multiplechoice'), ('TE', 'textentry'), ('CB', 'checkbox'),)
		widgets = {
			'question_type': forms.Select(choices = CHOICES),
			'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5}),
		}
		def clean_question_type(self):
		    data = self.cleaned_data['question_type']
		    return data


class MCQuestionForm(forms.ModelForm):
	class Meta:
		model = MCQuestion
		fields= '__all__'
		widgets = {
			'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5}),
			'option_1': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_2': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_3': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_4': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_5': forms.Textarea(attrs={'cols':10, 'rows': 2}),
		}
class TEQuestionForm(forms.ModelForm):
	class Meta:
		model = TEQuestion
		fields= '__all__'
		widgets = {
			'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5}),
		}
class CBQuestionForm(forms.ModelForm):
	class Meta:
		model = CBQuestion
		fields= '__all__'
		widgets = {
			'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5}),
			'option_1': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_2': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_3': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_4': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_5': forms.Textarea(attrs={'cols':10, 'rows': 2}),
		}
			

