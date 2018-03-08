from django.urls import path
from . import views
from django.conf import settings

app_name = 'login'

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('create/', views.create, name='create'),
]
