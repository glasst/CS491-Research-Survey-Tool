from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    # ex: /surveys/
    path('', views.home, name='home'),

    # ex: /surveys/newquestion/

    path('newquestion/', views.newquestion, name='newquestion'),

    path('takesurvey/', views.takesurvey, name='takesurvey'),
    path('survey-completion/', views.surveycompletion, name='survey-completion'),

    path('edit/', views.editsurvey, name='editsurvey'),

    # ex: /surveys/multiplechoice.html
    path('multiplechoice.html', views.multiplechoice, name='multiplechoice'),
    path('textentry.html', views.textentry, name='textentry'),
    path('checkbox.html', views.checkbox, name='checkbox'),

    path('index', views.index, name='index'),
    path('index/add_survey/', views.add_survey, name='add_survey'),

    # Ex: /surveys/e06f103b-d6e3-4e77-9442-ef938b621276/

    path('<uuid:survey_Id>/delete_question/', views.delete_question, name='delete_question'),
    path('<uuid:survey_Id>/add_question/', views.add_question, name='add_question'),
    # path('<uuid:survey_Id>/new_question/', views.new_question, name='new_question'),


    path('<uuid:survey_Id>/', views.survey_detail, name='survey')

    path('<uuid:survey_Id>/deleteq/', views.deleteq, name='deleteq')

    path('<uuid:survey_Id>/delete_question/', views.delete_question, name='delete_question'),
    path('<uuid:survey_Id>/add_question/', views.add_question, name='add_question'),
    #path('<uuid:survey_Id>/new_question/', views.new_question, name='new_question'),
]