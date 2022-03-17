from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from lessonbank.models import LessonBank
from django.urls import reverse_lazy
from landing.forms import UserUpdateForm, ProfileUpdateForm

#Imports for user logging
from adminmode.models import UserLog
import datetime

#################### Profile Management Views ####################

@login_required
def updateProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            #Insert log to database
            user_log = UserLog()
            user_log.log_by = request.user.username
            user_log.action = "updated his/her account"
            user_log.date_time_logged = datetime.datetime.now()
            user_log.save()

            messages.success(
                request, f'Success. Your profile has been updated!')
            return redirect('mandaread-edit-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'mandaread/update-profile.html', context)


@login_required
def updatePass(request):
    return render(request, 'mandaread/update-pass.html')


@login_required
def deleteAccount(request):
    return render(request, 'mandaread/delete-acc-prompt.html')


@login_required
def accountDelete(request):
    try:
        u = User.objects.get(id=request.user.id)
        u.delete()

        #Insert log to database
        user_log = UserLog()
        user_log.log_by = request.user.username
        user_log.action = "deleted his/her own account"
        user_log.date_time_logged = datetime.datetime.now()
        user_log.save()

        messages.warning(
            request, f'Your account has been deleted. It\'s sad to see you leave.')
    except User.DoesNotExist:
        messages.error(request, f'This user does not exist')

    return redirect('landing-login')


#################### Class Based Views ####################

class Home(LoginRequiredMixin, TemplateView):
    template_name = 'mandaread/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user)

        #Gettiing total read lessons of user
        lessons_read = LessonBank.objects.filter(read_by=user).count()
        all_lessons = LessonBank.objects.all().count()

        #Getting user's percentage
        percentage = str(round((lessons_read / all_lessons) * 100))
        
        context['lesson_percentage'] = percentage
        return context

class NewPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    def form_valid(self, form):
        #Insert log to database
        user_log = UserLog()
        user_log.log_by = self.request.user.username
        user_log.action = "changed his/her password"
        user_log.date_time_logged = datetime.datetime.now()
        user_log.save()
        return super().form_valid(form)

    form_class = PasswordChangeForm
    success_message = "Your password was updated successfully!"
    success_url = reverse_lazy('mandaread-edit-profile')