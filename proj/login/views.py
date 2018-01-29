from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def index(request):
    template = loader.get_template('login/index.html')
    context = {}
    return HttpResponse(template.render(context, request));

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    template = loader.get_template('registration/profile.html')
    context = {}
    return HttpResponse(template.render(context, request));

@login_required
def create(request):
    # add new survey to database
    return redirect('edit')

@login_required
def edit(request):
    survey = 'existing survey'
    return render(request, 'edit.html', {'survey': survey})
