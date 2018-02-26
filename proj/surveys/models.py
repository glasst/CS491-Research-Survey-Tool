from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
import uuid


import json
from uuid import UUID
from json import JSONEncoder

class UUIDEncoder(json.JSONEncoder):
        def default(self, obj):
                if isinstance(obj, UUID):
                        # if the obj is uuid, we simply return the value of uuid
                        return obj.hex
                return json.JSONEncoder.default(self, obj)

'''
class User(models.Model):
        user_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
        username = models.CharField(max_length=45)
        #username = models.CharField(primary_key=True, max_length=45)
        email = models.CharField(max_length=255)
        password = models.CharField(max_length=32)
        create_time = models.DateTimeField(auto_now=True)
        first_name = models.CharField(max_length=45)
        last_name = models.CharField(max_length=45)
        role = models.CharField(max_length=1)
'''

class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        role = models.CharField(max_length=1)
        
        def __str__(self):
                u = self.user
                return 'Username: %s, Name: %s %s' % (u.username, u.first_name, u.last_name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
        if created:
                Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Survey(models.Model):
	survey_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
	creator_Id = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=100, null=True)

	def __str__(self):
                return 'Survey ID: %s, Title: %s, %s' % (self.survey_Id, self.title, self.creator_Id.profile)

class Question(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
	question_survey_Id = models.ForeignKey(Survey, on_delete=models.CASCADE)
	question_type = models.CharField(max_length=20)
	#question_text = models.CharField(max_length=400, default="Add question text")
	#option_1 = models.CharField(max_length=100, default=None, blank=True, null=True)
	#option_2 = models.CharField(max_length=100, default=None, blank=True, null=True)
	#option_3 = models.CharField(max_length=100, default=None, blank=True, null=True)
	#option_4 = models.CharField(max_length=100, default=None, blank=True, null=True)
	#option_5 = models.CharField(max_length=100, default=None, blank=True, null=True)

	def __str__(self):
                return 'Question ID: %s, %s' % (self.question_Id, self.question_survey_Id)

class MCQuestion(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	question_survey_Id = models.ForeignKey(Survey, on_delete=models.PROTECT, null=True)
	question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
	question_text = models.CharField(max_length=400)
	option_1 = models.CharField(max_length=100)
	option_2 = models.CharField(max_length=100)
	option_3 = models.CharField(max_length=100)
	option_4 = models.CharField(max_length=100)
	option_5 = models.CharField(max_length=100)
class TEQuestion(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
	question_text = models.CharField(max_length=400)
class CBQuestion(models.Model):
	question_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
	question_text = models.CharField(max_length=400)
	option_1 = models.CharField(max_length=100)
	option_2 = models.CharField(max_length=100)
	option_3 = models.CharField(max_length=100)
	option_4 = models.CharField(max_length=100)
	option_5 = models.CharField(max_length=100)

class Response(models.Model):
	response_Id = models.UUIDField(primary_key=True, default=uuid.UUID(int=uuid.uuid4().int))
	response_question_Id = models.ForeignKey(Question, on_delete=models.PROTECT)
	#response_question_type = models.ForeignKey(Questions, on_delete=models.PROTECT)
	response_survey_Id 	= models.ForeignKey(Survey, on_delete=models.PROTECT)
	response_user_Id = models.ForeignKey(User, on_delete=models.PROTECT)
	response_text = models.CharField(max_length=400)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username',]

#form class for Survey model
class SurveyForm(forms.ModelForm):
	class Meta:
		model = Survey
		fields = '__all__'
		#fields = ['survey_Id',]
		widgets = {
			'survey_Id': forms.HiddenInput(),
			#'creator_Id': forms.HiddenInput(),
		}
	def set_creator_foreign_key(self, arg):
		# https://docs.djangoproject.com/en/2.0/topics/db/queries/
		#srvy = Survey.objects.get(pk=1)
		usr = User.objects.get(username=arg)
		creator_Id = usr


#form class for Question model
class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = '__all__'
		CHOICES = (('MC', 'multiplechoice'), ('TE', 'textentry'), ('CB', 'checkbox'),)
		widgets = {
			'question_Id': forms.HiddenInput(),
			'question_type': forms.Select(choices = CHOICES),
			#'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5,}),
		}
		#def clean_question_type(self):
		#    data = self.cleaned_data['question_type']
		#    return data
		#def set_survey_foreign_key(self, arg):
		#	question_survey_Id=arg


class MCQuestionForm(forms.ModelForm):
	class Meta:
		model = MCQuestion
		fields= '__all__'
		widgets = {
			'question_Id': forms.HiddenInput(),
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
			'question_Id': forms.HiddenInput(),
			'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5}),
		}
class CBQuestionForm(forms.ModelForm):
	class Meta:
		model = CBQuestion
		fields= '__all__'
		widgets = {
			'question_Id': forms.HiddenInput(),
			'question_text': forms.Textarea(attrs={'cols':50, 'rows': 5}),
			'option_1': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_2': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_3': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_4': forms.Textarea(attrs={'cols':10, 'rows': 2}),
			'option_5': forms.Textarea(attrs={'cols':10, 'rows': 2}),
		}


class TakeSurveyForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(TakeSurveyForm, self).__init__(*args, **kwargs)
		self.fields['survey_to_take'] = forms.ModelChoiceField(queryset=Survey.objects.filter(creator_Id__username=self.user))
