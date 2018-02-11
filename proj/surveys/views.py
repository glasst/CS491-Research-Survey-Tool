from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import User, Survey, Question, MCQuestion, TEQuestion, CBQuestion, Response, SurveyForm, QuestionForm, MCQuestionForm, TEQuestionForm, CBQuestionForm, TakeSurveyForm

import json
from uuid import UUID
from json import JSONEncoder

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


# Create your views here.

def index(request):

	num_users = User.objects.all().count()
	num_surveys = Survey.objects.all().count()

	creator = request.user
	
	if request.method == 'POST':
		#form = SurveyForm(request.POST or None, initial={'creator_Id':creator,})
		form = SurveyForm(request.POST)
		#form.fields['creator_Id'] = creator

		#usr = form.set_creator_foreign_key(creator)

		if form.is_valid():
			#creator = request.user
			#form.set_creator_foreign_key(creator)
			
			#form.cleaned_data['creator_Id'] = creator
			form.save()	

			#bbb = form.save(commit=False)
			#bbb.creator_Id = creator
			#bbb.save()

			return HttpResponseRedirect('newquestion/')
	else:
		form = SurveyForm()

	return render(
		request,
		'index.html',
		context={'form':form, 'num_users':num_users, 'num_surveys':num_surveys, 'userID':creator},
	)

### VIEWS FOR SURVEY MAKING ###
def newquestion(request):
	QUESTIONPAGES = {
		'MC': 'multiplechoice.html', 
		'TE': 'textentry.html', 
		'CB': 'checkbox.html',
	}
	nextpage = '/surveys/'

	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			#owningsurvey = request.
			#set_survey_foreign_key(owningsurvey)
			#https://chriskief.com/2013/05/24/django-form-wizard-and-getting-data-from-previous-steps/
			#https://docs.djangoproject.com/en/1.7/ref/contrib/formtools/form-wizard/

			nextpage += QUESTIONPAGES[request.POST.get('question_type')]
			form.save() #save to DB
			return HttpResponseRedirect(nextpage)
	else:
		form = QuestionForm()
	
	return render(
		request,
		'newquestion.html',
		context={'form':form},
	)


def multiplechoice(request):
	if request.method == 'POST':
		form = MCQuestionForm(request.POST)
		if form.is_valid():
			
			form.save() #save to DB
			return HttpResponseRedirect('/surveys/newquestion')
	else:
		form = MCQuestionForm()

	return render(
		request,
		'multiplechoice.html',
		context={'form':form},
	)


def textentry(request):
	if request.method == 'POST':
		form = TEQuestionForm(request.POST)
		if form.is_valid():
			
			form.save() #save to DB
			return HttpResponseRedirect('/surveys/newquestion')
	else:
		form = TEQuestionForm()

	return render(
		request,
		'textentry.html',
		context={'form':form},
	)


def checkbox(request):
	if request.method == 'POST':
		form = CBQuestionForm(request.POST)
		if form.is_valid():
			
			form.save() #save to DB
			return HttpResponseRedirect('/surveys/newquestion')
	else:
		form = CBQuestionForm()

	return render(
		request,
		'checkbox.html',
		context={'form':form},
	)



### VIEWS FOR SURVEY TAKING ###
def takesurvey(request):
	creator = request.user

	if request.method == 'POST':
		form = TakeSurveyForm(request.POST, user=request.user)
		if form.is_valid():
			request.session['survey_to_take'] = getattr(form.cleaned_data.get('survey_to_take'), 'survey_Id').hex
			return HttpResponseRedirect('/surveys/survey-completion')
	else:
		form = TakeSurveyForm(user=request.user)
	return render(
		request,
		'takesurvey.html',
		{'form':form}
	)


def surveycompletion(request):
	surveyid = request.session.get('survey_to_take')
	questions = Question.objects.filter(question_survey_Id=surveyid)

	mclist = []
	telist = []
	cblist = []

	# Still need to get cross-Question table querying
	for q in questions:
		if q.question_type == 'MC':
			qq = MCQuestion.objects.filter(question_Id=q.question_Id)
			mclist.append(qq)

		if q.question_type == 'TE':
			qq = MCQuestion.objects.filter(question_Id=q.question_Id)
			telist.append(qq)

		if q.question_type == 'CB':
			qq = MCQuestion.objects.filter(question_Id=q.question_Id)
			cblist.append(qq)

	return render (
		request,
		'survey-completion.html',
		{'surveyid':surveyid, 'mclist':mclist, 'telist':telist, 'cblist':cblist}
	)

