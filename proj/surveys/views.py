from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import User, Survey, Question, Response, SurveyForm, QuestionForm, MCQuestionForm, TEQuestionForm, CBQuestionForm, TakeSurveyForm
from django.db.models import Q

#experimental
#from django.contrib.formtools.wizard.views import SessionWizardView

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

	#create and return an html page as a response
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

#class SurveyWizard(SessionWizardView):
#	def done(self, form_list, form_dict, **kwargs):
#		surveystep = form_list['SurveyForm']
#		survey_data = self.get_cleaned_data_for_step(surveystep)



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
	#usrs = User.objects.all()
	#usr = NULL
	#for u in usrs:
	#	if usr.fields['username'] == creator:
	#		usr = u
	#surveys = Survey.objects.filter(creator_Id = u)

	#usr = User.objects.filter(username = creator)
	#surveys = Survey.objects.all()
	#for s in surveys:
	#	surveyslist.append(s)

	if request.method == 'POST':
		form = TakeSurveyForm(request.POST, user=request.user)
		if form.is_valid():
			request.session['survey_to_take'] = form.cleaned_data.get('survey_to_take')
			#return HttpResponseRedirect('/surveys/survey-completion', surveyid=request.POST['survey_to_take'])
			return HttpResponseRedirect('/surveys/survey-completion')
	else:
		form = TakeSurveyForm(user=request.user)
	return render(
		request,
		'takesurvey.html',
		{'form':form}
	)


#def surveycompletion(request, surveyid):
def surveycompletion(request):
	#NEED SURVEY ID
	surveyid = request.session.get('survey_to_take')
	questions = Question.objects.filter(question_survey_Id = surveyid)

	return render (
		request,
		'survey-completion.html',
		{'surveyid':surveyid, 'questions':questions}
	)

