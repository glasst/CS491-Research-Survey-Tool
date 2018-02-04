from django.shortcuts import render
#from django.http import HttpResponseRedirect

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

def multiplechoice(request):
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			form.save() #save to DB
			#return HttpResponseRedirect('/polls/thankyou')
	else:
		form = QuestionForm(request.POST)
	return render(
		request,
		'multiplechoice.html',
		context={'form':form},
	)
