from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, Response
from .forms import QuestionForm, MCQuestionForm, TEQuestionForm, CBQuestionForm, SurveyForm, TakeSurveyForm
from django.urls import reverse

import json
import uuid
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
    surveys = Survey.objects.filter(creator_Id=request.user.pk)
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
            s = form.save(commit=False)
            s.survey_Id = uuid.uuid4()
            s.save()

    else:
        form = SurveyForm(initial={'creator_Id': request.user.pk})

    return render(
        request,
        'home.html',
        context={'form': form, 'num_users': num_users, 'surveys': surveys, 'userID': creator})


### VIEWS FOR SURVEY MAKING ###

def editsurvey(request):
    s = None
    if 'id' in request.GET: request.session['survey'] = request.GET['id']
    if 'survey' in request.session:
        try:
            sid = request.session['survey']
            s = Survey.objects.get(survey_Id=sid)
        except:
            return HttpResponseRedirect('/surveys')

    if not s: return HttpResponseRedirect('/surveys')

    if request.method == 'POST' and 'remove' in request.POST:
        MCQuestion.objects.get(question_Id=request.POST['remove']).delete()
        #TEQuestion.objects.get(question_Id=request.POST['remove']).delete()
        #CBQuestion.objects.get(question_Id=request.POST['remove']).delete()

    return render(
        request,
        'edit.html',
        context={
            'survey': s.title,
            'mcquestions': MCQuestion.objects.filter(question_survey_Id=s.survey_Id),
            #'tequestions': TEQuestion.objects.filter(question_survey_Id=s.survey_Id),
            #'cbquestions': CBQuestion.objects.filter(question_survey_Id=s.survey_Id),
        }
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
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.save()
            return HttpResponseRedirect('/surveys/edit')
    else:
        form = MCQuestionForm(initial={'question_survey_Id': request.session['survey']})

    return render(
        request,
        'multiplechoice.html',
        context={'form': form},
    )


def textentry(request):
    if request.method == 'POST':
        form = TEQuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.save()
            return HttpResponseRedirect('/surveys/edit')
    else:
        form = TEQuestionForm(initial={'question_survey_Id': request.session['survey']})

    return render(
        request,
        'textentry.html',
        context={'form': form},
    )


def checkbox(request):
    if request.method == 'POST':
        form = CBQuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.save()
            return HttpResponseRedirect('/surveys/edit')
    else:
        form = CBQuestionForm(initial={'question_survey_Id': request.session['survey']})

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

    return render(
        request,
        'survey-completion.html',
        {'surveyid': surveyid, 'allQ': questions, 'mclist': mclist, 'telist': telist, 'cblist': cblist}
    )


# prints list of all survey objects
def index(request):
    user_surveys = Survey.objects.filter(creator_Id=request.user)

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():
            survey = form.save(commit=False)
            survey.survey_Id = uuid.uuid4()
            survey.save()
            # return redirect(reverse('surveys:add_survey'))
            return redirect(reverse('surveys:detail', kwargs={'survey_Id': survey.survey_Id}))

    else:
        form = SurveyForm()

    return render(request, 'surveys/index.html', {'user_surveys': user_surveys})


# page of specific survey listing its questions
def detail(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            QUESTIONPAGES = {
                'MC': 'multiplechoice.html',
                'TE': 'textentry.html',
                'CB': 'checkbox.html',
            }
            nextpage = '/surveys/'

            question = form.save(commit=False)
            question.question_Id = uuid.uuid4()
            question.question_type = request.POST.get('question_type')
            # question.question_survey_Id = request.POST.get('question_survey_Id')
            type = request.POST.get('question_type')
            nextpage += QUESTIONPAGES[type]
            question.save()  # save to DB
            # return HttpResponseRedirect(nextpage)
            '''
            if type is 'MC':
                return redirect(reverse('surveys:multiplechoice', kwargs={'survey_Id': survey.survey_Id}))
            elif type is 'TE':
                return redirect(reverse('surveys:textentry', kwargs={'survey_Id': survey.survey_Id}))
            else:
                return redirect(reverse('surveys:checkbox', kwargs={'survey_Id': survey.survey_Id}))
                '''

        # else:
        #    print(form.errors, len(form.errors))
    else:
        form = QuestionForm()

    # return render(request, 'surveys/add_question.html', {'survey': survey_Id})
    return render(request, 'surveys/detail.html', {'survey': survey})


def add_question(request, survey_Id):
    QUESTIONPAGES = {
        'MC': 'multiplechoice.html',
        'TE': 'textentry.html',
        'CB': 'checkbox.html',
    }
    nextpage = '/surveys/'

    question_form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # owningsurvey = request.
            # set_survey_foreign_key(owningsurvey)
            # https://chriskief.com/2013/05/24/django-form-wizard-and-getting-data-from-previous-steps/
            # https://docs.djangoproject.com/en/1.7/ref/contrib/formtools/form-wizard/
            question = form.save(commit=False)
            question.question_Id = uuid.uuid4()
            question.question_survey_Id = survey_Id

            nextpage += QUESTIONPAGES[request.POST.get('question_type')]
            question.save()  # save to DB
            # return HttpResponseRedirect(nextpage)
            return redirect(reverse('surveys:detail', args=(survey.survey_Id)))
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

    return render(request('add_question.html', context={'survey': survey.survey_Id, 'form': form}))


def delete_question(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)
    # question = None
    try:
        # question = request.POST.get('question')
        question = survey.question_set.get(question_Id=request.POST['question_Id'])
    except (KeyError, Question.DoesNotExist):
        return render(request, 'surveys/detail.html', {
            'question': question,
            'error_message': "You did not select a valid question",
        })
    else:
        question.delete()
    return render(request, 'surveys/detail.html', {'survey': survey})


def delete_survey(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)
    survey.delete()
    user_surveys = Survey.objects.filter(creator_Id=request.user)
    return render(request, 'surveys/index.html', {'user_surveys': user_surveys})


'''
def multiplechoice(request, survey_Id):
    #return render(request('multiplechoice.html', context={'survey': survey.survey_Id, 'form': form}))
    return redirect(reverse('surveys:multiplechoice', args=(survey.survey_Id,)))

def textentry(request, survey_Id):
    return render(request('textentry.html', context={'survey': survey.survey_Id, 'form': form}))

def checkbox(request, survey_Id):
    return render(request('checkbox.html', context={'survey': survey.survey_Id, 'form': form}))
'''
