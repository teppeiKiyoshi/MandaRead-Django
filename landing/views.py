from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
import datetime

#################### Imports for User Logging ####################
from adminmode.models import UserLog

#################### Register View ####################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome aboard, {username}! Your account has been created. Log In to get started.')
            
            #Insert log to database
            user_log = UserLog()
            user_log.log_by = username
            user_log.action = "registered an account"
            user_log.date_time_logged = datetime.datetime.now()
            user_log.save()

            return redirect('landing-login')
    else:
        form = UserRegisterForm()

    return render(request, 'landing/register.html', {'form': form})