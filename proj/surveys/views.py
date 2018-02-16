from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
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
            form.save()

            # bbb = form.save(commit=False)
            # bbb.creator_Id = creator
            # bbb.save()

            #return render(request, 'newquestion.html', {'surveyID': survey.survey_Id})
            #return render(request, 'newquestion.html', {'newquestion': })
            return HttpResponseRedirect('newquestion/')
    else:
        form = SurveyForm()

    return render(
        request,
        'home.html',
        context={'form': form, 'num_users': num_users, 'num_surveys': num_surveys, 'userID': creator},
    )


### VIEWS FOR SURVEY MAKING ###

def editsurvey(request):
    s = None
    if 'id' in request.GET: request.session['survey'] = request.GET['id']
    if 'survey' in request.session:
        try:
            sid = UUID(request.session['survey'], version=4)
            s = Survey.objects.get(survey_Id=sid)
        except:
            return HttpResponseRedirect('/surveys')

    if not s: return HttpResponseRedirect('/surveys')

    if request.method == 'POST':
        if 'add' in request.POST and request.POST['add']:
            typ = request.POST['type']
            try:
                s = Survey.objects.get(survey_Id=request.session['survey'])
            except:
                return HttpResponseRedirect('/surveys')
            if typ == 'MC':
                q = MCQuestion(question_survey_Id=s, question_text=request.POST['add'], option_1=request.POST['op1'],
                               option_2=request.POST['op2'])
                q.save()
        elif 'remove' in request.POST:
            MCQuestion.objects.get(question_Id=request.POST['remove']).delete()

    return render(
        request,
        'edit.html',
        context={'survey': request.session['survey'],
                 'mcquestions': MCQuestion.objects.filter(question_survey_Id=s.survey_Id)},
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
            # owningsurvey = request.
            # set_survey_foreign_key(owningsurvey)
            # https://chriskief.com/2013/05/24/django-form-wizard-and-getting-data-from-previous-steps/
            # https://docs.djangoproject.com/en/1.7/ref/contrib/formtools/form-wizard/

            nextpage += QUESTIONPAGES[request.POST.get('question_type')]
            form.save()  # save to DB
            return HttpResponseRedirect(nextpage)
    else:
        form = QuestionForm()

    return render(
        request,
        'newquestion.html',
        context={'form': form},
    )


def multiplechoice(request):
    if request.method == 'POST':
        form = MCQuestionForm(request.POST)
        if form.is_valid():
            form.save()  # save to DB
            return HttpResponseRedirect('/surveys/newquestion')
    else:
        form = MCQuestionForm()

    return render(
        request,
        'multiplechoice.html',
        context={'form': form},
    )


def textentry(request):
    if request.method == 'POST':
        form = TEQuestionForm(request.POST)
        if form.is_valid():
            form.save()  # save to DB
            return HttpResponseRedirect('/surveys/newquestion')
    else:
        form = TEQuestionForm()

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

    return render(
        request,
        'checkbox.html',
        context={'form': form},
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
        {'form': form}
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

    return render(
        request,
        'survey-completion.html',
        {'surveyid': surveyid, 'mclist': mclist, 'telist': telist, 'cblist': cblist}
    )


# prints list of all survey objects
def index(request):
    all_surveys = Survey.objects.all()

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():
            survey = form.save()
            #return HttpResponseRedirect('newquestion/')
            #add_survey(request, survey.survey_Id)
            #return HttpResponseRedirect(detail, survey_Id=survey.pk)
            #all_surveys = Survey.objects.all()
            return redirect(reverse('surveys:detail', args=(survey.survey_Id,)))
            #return render(request, 'surveys/add_survey.html', {'survey': survey})

    else:
        form = SurveyForm()

    return render(request, 'surveys/index.html', {'all_surveys': all_surveys})


# prints list of all survey objects
def add_survey(request, survey_Id):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save()
            return render(request, 'surveys/detail.html', {'survey': survey})
    return HttpResponseRedirect('surveys/home.html')
'''
    html = ''
    for survey in all_surveys:
        url = str(survey.survey_Id) + '/'
        html += '<a href="' + url + '">' + str(survey.survey_Id) + '</a><br>'
    return HttpResponse(html)
'''


# prints survey id of specific survey
def detail(request, survey_Id):
    # return HttpResponse("<h2>Survey ID: %s </h2>" % str(survey_Id))
    # survey = Survey.objects.filter(survey_Id=survey_Id).get()

    survey = get_object_or_404(Survey, survey_Id=survey_Id)

    return render(request, 'surveys/detail.html', {'survey': survey})


def delete_question(request, survey_Id):
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