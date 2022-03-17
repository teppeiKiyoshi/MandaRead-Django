from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from .models import UserLog, AchievementLog
from django.views.generic import (
    TemplateView, 
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from lessonbank.models import LessonAssessment, LessonBank
from dictionary.models import Dictionary
from django.contrib import messages
from django.urls import reverse_lazy, reverse
import datetime


#################### Admin Home ####################

class AdminHome(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "adminmode/admin_home.html"

    def test_func(self):
        return self.request.user.is_superuser


class AdminManageUsers(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "adminmode/admin_users.html"
    context_object_name = "users"

    def test_func(self):
        return self.request.user.is_superuser


#################### Admin User Management ####################

class AdminEditUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = "adminmode/admin_edit_users.html"
    context_object_name = 'user'
    fields = ['is_staff', 'is_superuser', 'user_permissions', 'last_login']

    def get_success_url(self):
        pk = self.kwargs['pk']
        user = User.objects.get(pk=pk)
        messages.add_message(self.request, messages.SUCCESS, f"{user.username}'s account has been updated!")
        return reverse_lazy('admin-users')

    def test_func(self):
        return self.request.user.is_superuser


class AdminDeleteUser(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "adminmode/admin_delete_user.html"
    context_object_name = "user"

    def get_success_url(self):
        pk = self.kwargs['pk']
        user = User.objects.get(pk=pk)
        messages.add_message(self.request, messages.SUCCESS, f"{user.username}'s account has been terminated")
        return reverse_lazy('admin-users')

    def test_func(self):
        return self.request.user.is_superuser


#################### Report Generation ####################

class AdminReports(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "adminmode/admin_reports.html"
    context_object_name = "users"
    queryset = User.objects.all().order_by('-date_joined')

    def get_queryset(self):
        if self.request.method == 'GET' and ('start' in self.request.GET and 'end' in self.request.GET):
            start = datetime.datetime.strptime(self.request.GET['start'], "%Y-%m-%d")
            end = datetime.datetime.strptime(self.request.GET['end'], "%Y-%m-%d") + datetime.timedelta(days=1)
            return User.objects.all().filter(date_joined__range=[start, end]).order_by('-date_joined')
        else:
            return User.objects.all().order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.kwargs['filter']
        
        if self.request.method == 'GET' and ('start' in self.request.GET and 'end' in self.request.GET):
            start = datetime.datetime.strptime(self.request.GET['start'], "%Y-%m-%d")
            end = datetime.datetime.strptime(self.request.GET['end'], "%Y-%m-%d") + datetime.timedelta(days=1)
            context['date_start'] = start.strftime("%b %d")
            context['date_end'] = datetime.datetime.strptime(self.request.GET['end'], "%Y-%m-%d").strftime("%b %d")
            context['logs'] = UserLog.objects.all().filter(date_time_logged__range=[start, end]).order_by('-date_time_logged')
            context['admin_logs'] = LogEntry.objects.all().filter(action_time__range=[start, end]).order_by('-action_time')
            context['achievements'] = AchievementLog.objects.all().filter(date_time_achieved__range=[start, end]).order_by('achieved_by')
        else: 
            context['logs'] = UserLog.objects.all().order_by('-date_time_logged')
            context['admin_logs'] = LogEntry.objects.all().order_by('-action_time')
            context['achievements'] = AchievementLog.objects.all().order_by('achieved_by')

        return context

    def test_func(self):
        return self.request.user.is_superuser


#################### Admin Lesson Management ####################

class AdminLessons(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LessonBank
    template_name = "adminmode/admin_lessons.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_list_1'] = LessonBank.objects.filter(hsk=1)
        context['lesson_list_2'] = LessonBank.objects.filter(hsk=2)
        return context

    def test_func(self):
        return self.request.user.is_superuser


class AdminLesson(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = LessonBank
    template_name = "adminmode/admin_lesson_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        
        lesson_obj = LessonBank.objects.get(pk=pk)
        context['lesson_items'] = Dictionary.objects.filter(from_lesson=lesson_obj)
        context['lesson_list_1'] = LessonBank.objects.filter(hsk=1)
        context['lesson_list_2'] = LessonBank.objects.filter(hsk=2)
        return context

    def test_func(self):
        return self.request.user.is_superuser

class AdminCreateLesson(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = LessonBank
    fields = ['hsk', 'title', 'description']
    template_name = "adminmode/lessonbank_form.html"
    success_message = "The lesson was successfully created!"
    success_url = reverse_lazy('admin-lessons')

    def test_func(self):
        return self.request.user.is_superuser


class AdminUpdateLesson(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = LessonBank
    fields = ['hsk', 'title', 'description', 'enable_table']
    template_name = "adminmode/lessonbank_form.html"
    success_message = "The lesson was successfully updated!"

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('admin-lesson', kwargs={'pk': pk})

    def test_func(self):
        return self.request.user.is_superuser


class AdminDeleteLesson(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = LessonBank
    template_name = "adminmode/lessonbank_confirm_delete.html"

    def get_success_url(self):
        pk = self.kwargs['pk']
        lesson = LessonBank.objects.get(pk=pk)
        messages.add_message(self.request, messages.SUCCESS, f"Lesson '{lesson.title}' was successfully deleted!")
        return reverse_lazy('admin-lessons')

    def test_func(self):
        return self.request.user.is_superuser



#################### Admin Dictionary Management ####################

class AdminDictionary(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, ListView):
    model = Dictionary
    template_name = "adminmode/admin_dictionary.html"
    context_object_name = 'words'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['current_page'] = self.request.GET.get('page', 1)
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.is_superuser


class AdminCreateDictionary(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Dictionary
    fields = ['from_lesson', 'hanzi', 'pinyin', 'definition', 'part_of_speech', 'example', 'translation']
    template_name = "adminmode/dictionary_form.html"
    success_message = "The word has been successfully added!"
    success_url = reverse_lazy('admin-dict')

    def test_func(self):
        return self.request.user.is_superuser


class AdminUpdateDictionary(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Dictionary
    fields = ['from_lesson', 'hanzi', 'pinyin', 'definition', 'part_of_speech', 'example', 'translation']
    template_name = "adminmode/dictionary_form.html"
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        word = Dictionary.objects.get(pk=pk)
        messages.add_message(self.request, messages.SUCCESS, f"Word '{word.hanzi}' -- '{word.pinyin}' was updated successfully!")
        
        #Go to paginated page
        if self.request.GET.get('next'):
            return f"/admin/dictionary?page={self.request.GET.get('next', 1)}"
        else:
            return "admin/dictionary"

    def test_func(self):
        return self.request.user.is_superuser



class AdminDeleteDictionary(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Dictionary
    template_name = "adminmode/dictionary_confirm_delete.html"

    def get_success_url(self):
        pk = self.kwargs['pk']
        word = Dictionary.objects.get(pk=pk)
        messages.add_message(self.request, messages.SUCCESS, f"Word '{word.hanzi}' -- '{word.pinyin}' was deleted successfully!")
        return reverse_lazy('admin-dict')

    def test_func(self):
        return self.request.user.is_superuser



#################### Admin Assessment Management ####################

class AdminAssessments(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, ListView):
    model = LessonBank
    template_name = "adminmode/admin_assessments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_list_1'] = LessonBank.objects.filter(hsk=1)
        context['lesson_list_2'] = LessonBank.objects.filter(hsk=2)
        return context

    def test_func(self):
        return self.request.user.is_superuser


class AdminAssessmentDetail(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, ListView):
    model = LessonAssessment
    template_name = "adminmode/admin_assessment_detail.html"
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        lesson_object = LessonBank.objects.get(pk=pk)
        return LessonAssessment.objects.filter(appearances_in_tests=lesson_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['lesson_object'] = LessonBank.objects.get(pk=pk)
        context['current_page'] = self.request.GET.get('page', 1)
        return context

    def test_func(self):
        return self.request.user.is_superuser



class AdminCreateItemView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = LessonAssessment
    template_name = "adminmode/assessment_form.html"
    fields = ['question_type', 'question', 'choices', 'answer', 'appearances_in_tests']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['lesson_object'] = LessonBank.objects.get(pk=pk)
        return context

    def get_initial(self):
        pk = self.kwargs['pk']
        appearances_in_tests = LessonBank.objects.get(pk=pk)
        return {
            'appearances_in_tests': appearances_in_tests
        }

    def get_success_url(self):
        pk = self.kwargs['pk']
        messages.add_message(self.request, messages.SUCCESS, "Question has been successfully added!")
        return reverse('admin-assessment', kwargs={'pk':pk})
    

    def test_func(self):
        return self.request.user.is_superuser



class AdminUpdateItemView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model=LessonAssessment
    template_name = "adminmode/assessment_form.html"
    fields = ['question_type', 'question', 'choices', 'answer', 'appearances_in_tests']

    def get_success_url(self):
        pk = self.kwargs['pk']
        lesson = LessonAssessment.objects.get(pk=pk).appearances_in_tests.all()[0].pk
        messages.add_message(self.request, messages.SUCCESS, "Question has been successfully updated!")

        #Go to paginated page
        if self.request.GET.get('next'):
            return f"/admin/assessments/{lesson}/?page={self.request.GET.get('next', 1)}"
        else:
            return f"/admin/assessments/{lesson}/"

    def test_func(self):
        return self.request.user.is_superuser



class AdminDeleteItemView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = LessonAssessment
    template_name = "adminmode/question_confirm_delete.html"

    def get_success_url(self):
        pk = self.kwargs['pk']
        lesson = LessonAssessment.objects.get(pk=pk).appearances_in_tests.all()[0].pk
        messages.add_message(self.request, messages.SUCCESS, f"Question was deleted successfully!")
        return f'/admin/assessments/{lesson}'
    
    def test_func(self):
        return self.request.user.is_superuser