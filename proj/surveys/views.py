<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
=======
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
from django.contrib.auth.models import User
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, Response, SurveyForm, QuestionForm, \
    MCQuestionForm, TEQuestionForm, CBQuestionForm, TakeSurveyForm
from django.urls import reverse

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

<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b

def home(request):
    num_users = User.objects.all().count()
    num_surveys = Survey.objects.all().count()
    creator = User.objects.get(username=request.user.username)
    survey_list = Survey.objects.filter(creator_Id=creator)

    if request.method == 'POST':
        # form = SurveyForm(request.POST or None, initial={'creator_Id':creator,})
        form = SurveyForm(request.POST)
        # form.fields['creator_Id'] = creator

        # usr = form.set_creator_foreign_key(creator)

        if form.is_valid():
            # creator = request.user
            # form.set_creator_foreign_key(creator)

            # form.cleaned_data['creator_Id'] = creator
            n = form.save()

            # bbb = form.save(commit=False)
            # bbb.creator_Id = creator
            # bbb.save()

            #return render(request, 'newquestion.html', {'surveyID': survey.survey_Id})
            #return render(request, 'newquestion.html', {'newquestion': })
            return HttpResponseRedirect('edit/?id=' + str(n.pk))
=======
def index(request):
    num_users = User.objects.all().count()
    num_surveys = Survey.objects.all().count()
    creator = User.objects.get(username=request.user.username)
    survey_list = Survey.objects.filter(creator_Id=creator)

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
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
    else:
        form = SurveyForm()

    return render(
        request,
<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
        'home.html',
        context={'form': form, 'num_users': num_users, 'num_surveys': num_surveys, 'userID': creator},
=======
        'index.html',
        context={'form':form, 'num_users':num_users, 'num_surveys':num_surveys, 'userID':creator},
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
    )


### VIEWS FOR SURVEY MAKING ###

def editsurvey(request):
    s = None
    if 'id' in request.GET: request.session['survey'] = request.GET['id']
    if 'survey' in request.session:
        try:
            sid = UUID(request.session['survey'], version=4)
            s = Survey.objects.get(survey_Id=sid)
<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
        except:
            return HttpResponseRedirect('/surveys')
=======
        except: return HttpResponseRedirect('/surveys')
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions

    if not s: return HttpResponseRedirect('/surveys')

    if request.method == 'POST':
        if 'add' in request.POST and request.POST['add']:
            typ = request.POST['type']
<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
            try:
                s = Survey.objects.get(survey_Id=request.session['survey'])
            except:
                return HttpResponseRedirect('/surveys')
            if typ == 'MC':
                q = MCQuestion(question_survey_Id=s, question_text=request.POST['add'], option_1=request.POST['op1'],
                               option_2=request.POST['op2'])
=======
            try: s = Survey.objects.get(survey_Id=request.session['survey'])
            except: return HttpResponseRedirect('/surveys')
            if typ == 'MC':
                q = MCQuestion(question_survey_Id=s, question_text=request.POST['add'], option_1=request.POST['op1'], option_2=request.POST['op2'])
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
                q.save()
        elif 'remove' in request.POST:
            MCQuestion.objects.get(question_Id=request.POST['remove']).delete()

    return render(
        request,
        'edit.html',
<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
        context={'survey': request.session['survey'],
                 'mcquestions': MCQuestion.objects.filter(question_survey_Id=s.survey_Id)},
    )




=======
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
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions

def multiplechoice(request):
    if request.method == 'POST':
        form = MCQuestionForm(request.POST)
        if form.is_valid():
            form.save()  # save to DB
            return HttpResponseRedirect('/surveys/newquestion')
    else:
        form = MCQuestionForm()

<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
    return render(
        request,
        'multiplechoice.html',
        context={'form': form},
    )

=======
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
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions

def textentry(request):
    if request.method == 'POST':
        form = TEQuestionForm(request.POST)
        if form.is_valid():
            form.save()  # save to DB
            return HttpResponseRedirect('/surveys/newquestion')
    else:
        form = TEQuestionForm()

<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
    return render(
        request,
        'textentry.html',
        context={'form': form},
    )


def checkbox(request):
    if request.method == 'POST':
        form = CBQuestionForm(request.POST)
        if form.is_valid():
            form.save()  # save to DB
            return HttpResponseRedirect('/surveys/newquestion')
    else:
        form = CBQuestionForm()
=======
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
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions

    return render(
        request,
        'checkbox.html',
        context={'form': form},
    )


### VIEWS FOR SURVEY TAKING ###
def takesurvey(request):
<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
=======

>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
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
<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
        {'form': form}
=======
        {'form':form}
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
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

<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
    return render(
        request,
        'survey-completion.html',
        {'surveyid': surveyid, 'mclist': mclist, 'telist': telist, 'cblist': cblist}
    )


# prints list of all survey objects
def index(request):
    user_surveys = Survey.objects.filter(creator_Id=request.user)

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():
            survey = form.save()
            return redirect(reverse('surveys:detail', args=(survey.survey_Id,)))

    else:
        form = SurveyForm()

    return render(request, 'surveys/index.html', {'user_surveys': user_surveys})


# add survey and go to its detail page
def add_survey(request, survey_Id):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save()
            return render(request, 'surveys/detail.html', {'survey': survey})
    return HttpResponseRedirect('surveys/home.html')


# page of specific survey listing its questions
def detail(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)
    return render(request, 'surveys/detail.html', {'survey': survey})

def add_question(request, survey_Id):
    QUESTIONPAGES = {
        'MC': 'multiplechoice.html',
        'TE': 'textentry.html',
        'CB': 'checkbox.html',
    }
    nextpage = '/surveys/'

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # owningsurvey = request.
            # set_survey_foreign_key(owningsurvey)
            # https://chriskief.com/2013/05/24/django-form-wizard-and-getting-data-from-previous-steps/
            # https://docs.djangoproject.com/en/1.7/ref/contrib/formtools/form-wizard/
            question = form.save(commit=False)
            question.set(question_survey_Id=survey_Id)

            nextpage += QUESTIONPAGES[request.POST.get('question_type')]
            question.save()  # save to DB
            #return HttpResponseRedirect(nextpage)
            return render(request, 'surveys/detail.html', {'survey': survey})
    else:
        form = QuestionForm()

    return render(request, 'surveys/add_question.html', {'survey': survey_Id})


def new_question(request, survey_Id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.set(question_survey_Id=survey_Id)
            nextpage += QUESTIONPAGES[request.POST.get('question_type')]
            question.save()  # save to DB
            return redirect(reverse('surveys:detail', args=(survey.survey_Id,)))
    else:
        form = QuestionForm()

    return render(request('add_question.html', context={ 'survey':survey.survey_Id, 'form':form }))


def delete_question(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)
    #question = None
    try:
        #question = request.POST.get('question')
        question = survey.question_set.get(question_Id=request.POST['question_Id'])
    except (KeyError, Question.DoesNotExist):
        return render(request, 'surveys/detail.html', {
            'question': question,
            'error_message': "You did not select a valid question",
        })
    else:
        question.delete()
    return render(request, 'surveys/detail.html', {'survey': survey})

'''
def add_survey(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)
    try:
        selected_question = survey.question_set.get(question_Id=request.POST['question'])
    except (KeyError, Question.DoesNotExist):
        return render(request, 'surveys/detail.html', {
            'question': question,
            'error_message': "You did not select a valid question",
        })
    else:
        selected_question.delete()

    return render(request, 'surveys/detail.html', {'survey': survey})
'''
=======
    return render (
        request,
        'survey-completion.html',
        {'surveyid':surveyid, 'mclist':mclist, 'telist':telist, 'cblist':cblist}
    )

# prints list of all survey objects
def survey_index(request):
    all_surveys = Survey.objects.all()
    return render(request, 'surveys/index.html', {'all_surveys': all_surveys})

'''
    html = ''

    for survey in all_surveys:
        url = str(survey.survey_Id) + '/'
        html += '<a href="' + url + '">' + str(survey.survey_Id) + '</a><br>'
    return HttpResponse(html)
'''

#prints survey id of specific survey
def survey_detail(request, survey_Id):
    #return HttpResponse("<h2>Survey ID: %s </h2>" % str(survey_Id))
    #survey = Survey.objects.filter(survey_Id=survey_Id).get()

    survey = get_object_or_404(Survey, survey_Id=survey_Id)
        
    return render(request, 'surveys/detail.html', {'survey': survey})
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
