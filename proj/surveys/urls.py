from django.urls import path
from . import views

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
]
