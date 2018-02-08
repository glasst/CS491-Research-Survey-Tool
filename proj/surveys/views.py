from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import User, Survey, Question, Response, SurveyForm, QuestionForm

#experimental
#from django.contrib.formtools.wizard.views import SessionWizardView

# Create your views here.

def index(request):
	num_users = User.objects.all().count()
	num_surveys = Survey.objects.all().count()
	
	if request.method == 'POST':
		form = SurveyForm(request.POST)
		if form.is_valid():
			creator = request.user
			form.set_creator_foreign_key(creator)
			
			form.save()
			return HttpResponseRedirect('newquestion/')
	else:
		form = SurveyForm()

	#create and return an html page as a response
	return render(
		request,
		'index.html',
		context={'form':form, 'num_users':num_users, 'num_surveys':num_surveys},
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
		form = QuestionForm()

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
		form = QuestionForm()

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
		form = QuestionForm()

	return render(
		request,
		'checkbox.html',
		context={'form':form},
	)

