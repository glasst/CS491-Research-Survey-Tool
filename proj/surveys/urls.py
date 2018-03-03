from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    # ex: /surveys/
    path('', views.home, name='home'),

    # ex: /surveys/newquestion/
    #path('newquestion/', views.newquestion, name='newquestion'),
    path('takesurvey/', views.takesurvey, name='takesurvey'),
    path('survey-completion/', views.surveycompletion, name='survey-completion'),

    path('edit/<uuid:survey_Id>/', views.editsurvey, name='editsurvey'),

    # ex: /surveys/multiplechoice.html
    path('edit/<uuid:survey_Id>/multiplechoice', views.multiplechoice, name='multiplechoice'),
    path('edit/<uuid:survey_Id>/textentry', views.textentry, name='textentry'),
    path('edit/<uuid:survey_Id>/checkbox', views.checkbox, name='checkbox'),

    #/surveys/index
    path('index', views.index, name='index'),

    #Ex: /surveys/e06f103b-d6e3-4e77-9442-ef938b621276/
    path('<uuid:survey_Id>/', views.detail, name='detail'),

    path('<uuid:survey_Id>/delete_question/', views.delete_question, name='delete_question'),
    #path('<uuid:survey_Id>/add_question/', views.add_question, name='add_question'),
    path('<uuid:survey_Id>/new_question/', views.new_question, name='new_question'),
    path('<uuid:survey_Id>/delete_survey/', views.delete_survey, name='delete_survey'),

]
