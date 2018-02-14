from django.urls import path
from . import views

<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b
app_name = 'surveys'

urlpatterns = [
    # ex: /surveys/
    path('', views.home, name='home'),

    # ex: /surveys/newquestion/
    # path('newquestion/', views.newquestion, name='newquestion'),
=======
#app_name = 'surveys'

urlpatterns = [
    # ex: /surveys/
    path('', views.index, name='index'),

    # ex: /surveys/newquestion/
    path('newquestion/', views.newquestion, name='newquestion'),
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
    path('takesurvey/', views.takesurvey, name='takesurvey'),
    path('survey-completion/', views.surveycompletion, name='survey-completion'),

    path('edit/', views.editsurvey, name='editsurvey'),
<<<<<<< cef8a8edfff97ea5b8a2b81c5082380756be005b

    # ex: /surveys/multiplechoice.html
    path('multiplechoice.html', views.multiplechoice, name='multiplechoice'),
    path('textentry.html', views.textentry, name='textentry'),
    path('checkbox.html', views.checkbox, name='checkbox'),

    # /surveys/index
    path('index', views.index, name='index'),

    path('index/add_survey/', views.add_survey, name='add_survey'),

    # Ex: /surveys/e06f103b-d6e3-4e77-9442-ef938b621276/
    path('<uuid:survey_Id>/', views.detail, name='detail'),

    path('<uuid:survey_Id>/delete_question/', views.delete_question, name='delete_question'),
    path('<uuid:survey_Id>/add_question/', views.add_question, name='add_question'),
    # path('<uuid:survey_Id>/new_question/', views.new_question, name='new_question'),
=======

    # ex: /surveys/multiplechoice.html
    path('multiplechoice.html', views.multiplechoice, name='multiplechoice'),
    path('textentry.html', views.textentry, name='textentry'),
    path('checkbox.html', views.checkbox, name='checkbox'),

    #/surveys/index
    path('index', views.survey_index, name='survey_index'),

    #/surveys/e06f103b-d6e3-4e77-9442-ef938b621276/
    path('<uuid:survey_Id>/', views.survey_detail, name='survey')
>>>>>>> added alt survey index redirecting to individual survey pages listing uuid of questions
]
