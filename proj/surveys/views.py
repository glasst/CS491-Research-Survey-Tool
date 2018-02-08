from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from .models import User, Survey, Question, Response, QuestionForm

def index(request):
	num_users = User.objects.all().count()
	num_surveys = Survey.objects.all().count()

	#create and return an html page as a response
	return render(
		request,
		'index.html',
		context={'num_users':num_users, 'num_surveys':num_surveys},
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
			nextpage += QUESTIONPAGES[request.POST.get('question_type')]
			form.save() #save to DB
			return HttpResponseRedirect(nextpage)
	else:
		form = QuestionForm()
		#return HttpResponseRedirect('')
	
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
		form = QuestionForm()
		#return HttpResponseRedirect('/surveys/newquestion')

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
		#return HttpResponseRedirect('/surveys/newquestion')

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
		#return HttpResponseRedirect('/surveys/newquestion')

	return render(
		request,
		'checkbox.html',
		context={'form':form},
	)

