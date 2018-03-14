from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, ResponseTE
from .forms import QuestionForm, MCQuestionForm, TEQuestionForm, CBQuestionForm, SurveyForm, TakeSurveyForm
from .forms import ResponseTEForm, ResponseMCForm, ResponseCBForm
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django import forms

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
    return render(
        request,
        'home.html',
        context={})


@login_required
def index(request):
    num_users = User.objects.all().count()
    surveys = Survey.objects.filter(creator_Id=request.user.pk)
    creator = User.objects.get(username=request.user.username)
    survey_list = Survey.objects.filter(creator_Id=creator)
    form = SurveyForm(initial={'creator_Id': request.user.pk})

    if request.method == 'POST':
        if 'remove' in request.POST:
            try:
                s = Survey.objects.get(survey_Id=request.POST['remove'])
                print(s.title)
                s.delete()
            except:
                pass
        else:
            form = SurveyForm(request.POST)
            if form.is_valid():
                s = form.save(commit=False)
                s.survey_Id = uuid.uuid4()
                s.save()

    return render(
        request,
        'index.html',
        context={'form': form, 'num_users': num_users, 'surveys': surveys, 'userID': creator})

# No longer using any login view functions
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        # form2 = UserForm(request.POST) ###

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            # form2.fields['user_Id'] = request.user ### this gives username, not UUID
            login(request, user)
            return redirect(reverse('surveys:index'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


### VIEWS FOR SURVEY MAKING ###
@login_required
def editsurvey(request, survey_Id):
    #s = None
    #if 'id' in request.GET: request.session['survey'] = request.GET['id']
    #if 'survey' in request.session:
    if not survey_Id:
        #try:
            #sid = request.session['survey']
        #    s = Survey.objects.get(survey_Id=survey_Id)
        #except:
        return HttpResponseRedirect('/surveys')

    #else: return HttpResponseRedirect('/surveys')
    survey = get_object_or_404(Survey, survey_Id=survey_Id)
    if request.method == 'POST':
        if 'remove' in request.POST:
        # try:
        #     MCQuestion.objects.get(question_Id=request.POST['remove']).delete()
        # except:
        #     pass
            try:
            #TEQuestion.objects.get(question_Id=request.POST['remove']).delete()
            #question = get_object_or_404(Survey, survey_Id=survey_Id)
                question = Question.objects.get(question_Id=request.POST['remove'])
                survey.decrement_questions(question.question_num)
                survey.num_questions -= 1
                survey.save()
                question.delete()
            except:
                pass
        # try:
        #     CBQuestion.objects.get(question_Id=request.POST['remove']).delete()
        # except:
        #     pass

        elif 'reorder' in request.POST:
            s = request.POST.get('survey')
            q = request.POST.get('reorder')
            n = int(request.POST.get('new_index'))
            if s and q: reorder(s, q, n)

    return render(
        request,
        'edit.html',
        context={
            'survey_title': survey.title,
            'survey_Id': survey_Id,
            'questions': Question.objects.filter(question_survey_Id=survey_Id).order_by('question_num'),
            #'mcquestions': MCQuestion.objects.filter(question_survey_Id=survey_Id),
            #'tequestions': TEQuestion.objects.filter(question_survey_Id=survey_Id),
            #'cbquestions': CBQuestion.objects.filter(question_survey_Id=survey_Id),
        }
    )

def reorder(sid, qid, new):
    current = Question.objects.get(question_Id=qid)
    survey = Survey.objects.get(survey_Id=sid)
    questions = Question.objects.filter(question_survey_Id=survey.survey_Id)
    old = current.question_num
    if new < 1: new = 1
    if new > survey.num_questions: new = survey.num_questions
    if old == new: return
    elif old > new:
        for i in range(old - 1, new - 1, -1):
            #print("moving question " + str(i) + " to " + str(i + 1))
            cq = questions.filter(question_num=i)
            for q in cq:
                q.question_num += 1
                q.save()
    else:
        for i in range(old + 1, new + 1):
            #print("moving question " + str(i) + " to " + str(i + 1))
            cq = questions.filter(question_num=i)
            for q in cq:
                q.question_num -= 1
                q.save()
    current.question_num = new
    current.save()

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


@login_required
def multiplechoice(request, survey_Id):
    if request.method == 'POST':
        form = MCQuestionForm(request.POST)
        if form.is_valid():
            survey = get_object_or_404(Survey, survey_Id=survey_Id)
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.question_type = 'MC'
            q.question_survey_Id = survey
            survey.num_questions += 1
            q.question_num = survey.num_questions
            q.save()
            survey.save()
            return redirect(reverse('surveys:editsurvey', args=(survey.survey_Id,)))
    else:
        form = MCQuestionForm(initial={'question_survey_Id': survey_Id})

    return render(
        request,
        'multiplechoice.html',
        context={'form': form},
    )


@login_required
def textentry(request, survey_Id):
    if request.method == 'POST':
        form = TEQuestionForm(request.POST)
        if form.is_valid():
            survey = get_object_or_404(Survey, survey_Id=survey_Id)
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.question_type = 'TE'
            q.question_survey_Id = survey
            survey.num_questions = survey.num_questions + 1
            q.question_num = survey.num_questions
            q.save()
            survey.save()
            return redirect(reverse('surveys:editsurvey', args=(survey.survey_Id,)))

    else:
        form = TEQuestionForm(initial={'question_survey_Id': survey_Id})

    return render(
        request,
        'textentry.html',
        context={'form': form},
    )


@login_required
def checkbox(request, survey_Id):
    if request.method == 'POST':
        form = CBQuestionForm(request.POST)
        if form.is_valid():
            survey = get_object_or_404(Survey, survey_Id=survey_Id)
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.question_type = 'CB'
            q.question_survey_Id = survey
            survey.num_questions += 1
            q.question_num = survey.num_questions
            q.save()
            survey.save()
            return redirect(reverse('surveys:editsurvey', args=(survey.survey_Id,)))
    else:
        form = CBQuestionForm(initial={'question_survey_Id': survey_Id})

    return render(
        request,
        'checkbox.html',
        context={'form': form},
    )


### VIEWS FOR SURVEY TAKING ###
@login_required
def takesurvey(request):
    if request.method == 'POST':
        form = TakeSurveyForm(request.POST, user=request.user)
        if form.is_valid():
            request.session['survey_to_take'] = getattr(form.cleaned_data.get('survey_to_take'), 'survey_Id').hex
            #return surveycompletion(request, 1)
            return redirect(reverse('surveys:survey-completion', kwargs={'qnum':1}))
    else:
        form = TakeSurveyForm(user=request.user)
    return render(
        request,
        'takesurvey.html',
        {'form': form}
    )

def done(request):
    return render(request,'done.html')



@login_required
def surveycompletion(request, qnum):
    print(qnum, "!!!!!!")
    surveyid = request.session.get('survey_to_take')
    survey = Survey.objects.get(survey_Id=surveyid)
    questions = Question.objects.filter(question_survey_Id=surveyid)

    print(request)
    # Check if participant submitted a response
    q = Question.objects.filter(question_num = qnum, question_survey_Id=surveyid);
    if not q:
        return HttpResponseRedirect('/survey-completion/done')
    else:
        q = Question.objects.get(question_num = qnum, question_survey_Id=surveyid);
    if(request.method == 'POST'):
        print(q.question_num , "    ", q.question_type)
        if (q.question_type == 'MC'):
            print("MC!!   ", q.question_text)
            if request.method == 'POST':
                form = ResponseMCForm(request.POST)
                if form.is_valid():
                    print("test")
                    print(form.cleaned_data.get('response_text'))
                    f = form.save(commit = False)
                    f.response_user_Id = User.objects.get(username
                        = request.user.username)
                    f.response_survey_Id =  Survey.objects.get(survey_Id = surveyid)
                    f.response_question_Id = Question.objects.get(question_Id = q.question_Id)
                    f.save()
                else:
                    print("form not valid")

        elif (q.question_type == 'CB'):
            print("CB")
            if request.method == 'POST':
                form = ResponseCBForm(request.POST)
                if form.is_valid():
                    print(form.cleaned_data)
                    f = form.save(commit = False)
                    f.response_user_Id = User.objects.get(username
                        = request.user.username)
                    f.response_survey_Id = Survey.objects.get(survey_Id = surveyid)
                    f.response_question_Id = Question.objects.get(question_Id = q.question_Id)
                    f.save()

        else:
            print("TE")
            if request.method == 'POST':
                form = ResponseTEForm()
                if form.is_valid():
                    f = form.save(commit = False)
                    f.response_user_Id = User.objects.get(username
                        = request.user.username)
                    f.response_survey_Id =  Survey.objects.get(survey_Id = surveyid)
                    f.response_question_Id = Question.objects.get(question_Id = q.question_Id)
                    f.save()

        checkq = Question.objects.filter(question_survey_Id = surveyid, question_num = qnum+1)
        print("Reached checkq")
        # Check if there are more questions in survey
        if not checkq:
            return HttpResponseRedirect('/survey-completion/done')
        else:
            # Get next availabe question
            return redirect(reverse('surveys:survey-completion', kwargs={'qnum':qnum+1}))
    else:
        print("my question type is " + q.question_type)
        if q.question_type == 'MC':
            print("MC no post")
            options = q.get_options()
            print(options)
            form = ResponseMCForm(option_list=options)
            #print(form.response_text)
        elif q.question_type == 'CB':
            print("CB no post")
            options = q.get_options()
            print(options)
            form = ResponseCBForm(option_list=options)
        else:
            print("TE no post")
            form = ResponseTEForm()


    return render (request,
        'survey-completion2.html',{'form': form, "question": q, 'type':q.question_type})

'''
IN PROGRESS
def option(request, question_Id, type):
    if request.method == 'POST':
        form = Option(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            if(type == 'CB')
                question = get_object_or_404(CBQuestion, question_Id=question_Id)
            else:
                question = get_object_or_404(MCQuestion, question_Id=question_Id)
            option.mc_question_Id = question
            option.type_of_question = type
            option.option_Id = uuid.uuid4()
            q.save()
            return redirect(reverse('surveys:editsurvey', args=(survey.survey_Id,)))
    else:
        form = CBQuestionForm(initial={'question_survey_Id': survey_Id})

    return render(
        request,
        'checkbox.html',
        context={'form': form},
    )
'''
