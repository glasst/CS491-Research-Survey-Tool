from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
]
