from django.urls import path
from . import views

urlpatterns = [
	# ex: /polls/
	path('', views.index, name='index'),

	# ex: /polls/multiplechoice/
	path('multiplechoice/', views.multiplechoice, name='multiplechoice'),
]
