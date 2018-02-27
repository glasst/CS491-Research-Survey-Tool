from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, Response, SurveyForm, QuestionForm, MCQuestionForm, TEQuestionForm, CBQuestionForm, TakeSurveyForm

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
	creator = User.objects.get(username=request.user.username)
	survey_list = Survey.objects.filter(creator_Id=creator)

	if request.method == 'POST':
		#form = SurveyForm(request.POST or None, initial={'creator_Id':creator,})
		form = SurveyForm(user=request.user)
		#form.fields['creator_Id'] = creator

		#usr = form.set_creator_foreign_key(creator)

		if form.is_valid():
			form.save()

			return HttpResponseRedirect('newquestion/')
	else:
		form = SurveyForm(user=request.user)

	return render(
		request,
		'index.html',
		context={'form':form, 'num_users':num_users, 'num_surveys':num_surveys, 'userID':creator},
	)

### VIEWS FOR SURVEY MAKING ###

def editsurvey(request):
	s = None
	if 'id' in request.GET: request.session['survey'] = request.GET['id']
	if 'survey' in request.session:
		try:
			sid = UUID(request.session['survey'], version=4)
			s = Survey.objects.get(survey_Id=sid)
		except: return HttpResponseRedirect('/surveys')

	if not s: return HttpResponseRedirect('/surveys')

	if request.method == 'POST':
		if 'add' in request.POST and request.POST['add']:
			typ = request.POST['type']
			try: s = Survey.objects.get(survey_Id=request.session['survey'])
			except: return HttpResponseRedirect('/surveys')
			if typ == 'MC':
				q = MCQuestion(question_survey_Id=s, question_text=request.POST['add'], option_1=request.POST['op1'], option_2=request.POST['op2'])
				q.save()
		elif 'remove' in request.POST:
			MCQuestion.objects.get(question_Id=request.POST['remove']).delete()

	return render(
		request,
		'edit.html',
		context={'survey':request.session['survey'], 'mcquestions':MCQuestion.objects.filter(question_survey_Id=s.survey_Id)},
	)


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


'''def surveycompletion(request):
	surveyid = request.session.get('survey_to_take')
	questions = Question.objects.filter(question_survey_Id=surveyid)
	print(surveyid)
	mclist = []
	telist = []
	cblist = []

	# Still need to get cross-Question table querying
	for q in questions:
		qid = q.question_Id
		
		if q.question_type == 'MC':
			qq = MCQuestion.objects.filter(question_Id=qid)
			mclist.append(qq)

		if q.question_type == 'TE':
			qq = MCQuestion.objects.filter(question_Id=qid)
			telist.append(qq)

		if q.question_type == 'CB':
			qq = MCQuestion.objects.filter(question_Id=qid)
			cblist.append(qq)

	return render (
		request,
		'survey-completion.html',
		{'surveyid':surveyid, 'allQ':questions, 'mclist':mclist, 'telist':telist, 'cblist':cblist}
	)'''

def surveycompletion(request):
	surveyid = request.session.get('survey_to_take')
	questions = Question.objects.filter(question_survey_Id=surveyid)
	mcquestions = MCQuestion.objects.filter(question_survey_Id = surveyid)
	tequestions = TEQuestion.objects.filter(question_survey_Id=surveyid)
	print(surveyid)
	mclist = []
	telist = []
	cblist = []
	qlist = []
	# Still need to get cross-Question table querying
	for q in questions:
		qlist.append(q)
	for q in mcquestions:
		qlist.append(q)
	for q in tequestions:
		qlist.append(q)


	for q in qlist:
		print("questionID: ", end = "")
		print(q.question_Id, "\n" , q.question_type, end="")
		print("	question text: ", end = "") 
		print(q.question_text)
		

	return render (request,
		'survey-completion.html',
		{'surveyid':surveyid, 'allQ':qlist, 'mclist':mclist, 'telist':telist, 'cblist':cblist}
	)






