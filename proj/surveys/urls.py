from django.urls import path
from . import views

#app_name = 'surveys'

urlpatterns = [
    # ex: /surveys/
    path('', views.index, name='index'),

    # ex: /surveys/newquestion/
    path('newquestion/', views.newquestion, name='newquestion'),
    path('takesurvey/', views.takesurvey, name='takesurvey'),
    path('survey-completion/', views.surveycompletion, name='survey-completion'),

    path('edit/', views.editsurvey, name='editsurvey'),

    # ex: /surveys/multiplechoice.html
    path('multiplechoice.html', views.multiplechoice, name='multiplechoice'),
    path('textentry.html', views.textentry, name='textentry'),
    path('checkbox.html', views.checkbox, name='checkbox'),

    #/surveys/index
    path('index', views.survey_index, name='survey_index'),

    #/surveys/e06f103b-d6e3-4e77-9442-ef938b621276/
    path('<uuid:survey_Id>/', views.survey_detail, name='survey'),

    #delete question
    #/surveys/e06f103b-d6e3-4e77-9442-ef938b621276/
    path('<uuid:survey_Id>/deleteq/', views.deleteq, name='deleteq')
]
