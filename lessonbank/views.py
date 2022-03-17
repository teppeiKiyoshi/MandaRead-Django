from distutils.log import debug
from importlib.metadata import requires
from urllib import request
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import LessonBank, LessonAssessment
from dictionary.models import Dictionary
from django.contrib.auth.models import User
from django.db.models import Q
from django import forms
from django.http import JsonResponse
import random

#################### Imports for User Logging ####################
from adminmode.models import UserLog, AchievementLog
import datetime


#################### Lesson Views ####################
class LessonsListView(ListView):
    model = LessonBank
    template_name = 'lessonbank/lessonlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_list_1'] = LessonBank.objects.filter(hsk=1)
        context['lesson_list_2'] = LessonBank.objects.filter(hsk=2)
        return context

class LessonListDetailView(DetailView):
    model = LessonBank
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user)
        pk = self.kwargs['pk']

        # Add User to "read_by" field of the lesson
        lesson_obj = LessonBank.objects.get(pk=pk)

        if not user in lesson_obj.read_by.all():
            lesson_obj.read_by.add(user)

            #Getting total read lessons of user
            lessons_read = LessonBank.objects.filter(read_by=user).count()
            all_lessons = LessonBank.objects.all().count()

            #If user achieved an achievement
            percentage = round((lessons_read / all_lessons) * 100)

            achievement = AchievementLog()

            if percentage >= 25:
                if user.profile.lessons_25 != True:
                    user.profile.lessons_25 = True  
                    achievement.achieved_by = user
                    achievement.date_time_achieved = datetime.datetime.now()
                    achievement.achievement = "Wheat of Prosperity"
                    achievement.save() 
                    user.save()
            if percentage >= 50:
                if user.profile.lessons_50 != True:
                    user.profile.lessons_50 = True
                    achievement.achieved_by = user
                    achievement.date_time_achieved = datetime.datetime.now()
                    achievement.achievement = "Terracota Helmet"
                    achievement.save() 
                    user.save()
            if percentage == 100:
                if user.profile.lessons_100 != True:
                    user.profile.lessons_100 = True
                    achievement.achieved_by = user
                    achievement.date_time_achieved = datetime.datetime.now()
                    achievement.achievement = "Golden Konghou"
                    achievement.save() 
                    user.save()
        else:
            pass
            

        context['lesson_list_1'] = LessonBank.objects.filter(hsk=1)
        context['lesson_list_2'] = LessonBank.objects.filter(hsk=2)

        context['lesson_items'] = Dictionary.objects.filter(from_lesson=lesson_obj)

        #Insert log to database
        user_log = UserLog()
        user_log.log_by = self.request.user.username
        user_log.action = "read lesson " + "\"HSK-" + str(lesson_obj.hsk) + ": " + lesson_obj.title + "\""
        user_log.date_time_logged = datetime.datetime.now()
        user_log.save() 

        return context

#################### Assessment ####################
class LessonAssessmentView(ListView, forms.Form):
    model = LessonAssessment
    template_name = 'lessonbank/lesson_assessment.html'
    context_object_name = 'assessment_items'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['lesson'] = LessonBank.objects.get(id=pk)
        return context

    # Get questions
    def get_queryset(self):
        pk = self.kwargs['pk']
        current_lesson = LessonBank.objects.get(id=pk)
        hsk = current_lesson.hsk

        if hsk == 1:
            return LessonAssessment.objects.filter(~Q(appearances_in_tests__hsk=2) & Q(appearances_in_tests=current_lesson)).order_by('?')[:10]
        elif hsk == 2:
            # Will get questions of the lesson, and its corresponding lesson in HSK1 (QUERIED USING TITLE)
            queryset_to_list = list(LessonAssessment.objects.filter(Q(appearances_in_tests__title__contains=current_lesson.title)).distinct()[:10])
            random.shuffle(queryset_to_list)
            return queryset_to_list



#################### Mocktest ####################
class MockTestView(ListView):
    model = LessonAssessment
    template_name = 'lessonbank/mocktest.html'
    context_object_name = 'assessment_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hsk'] = self.kwargs['hsk']
        return context

    def get_queryset(self):
        hsk = self.kwargs['hsk'];

        if hsk == 1:
            questions = LessonAssessment.objects.filter(~Q(appearances_in_tests__hsk=2)).order_by('?')[:80]
        elif hsk == 2:
            questions = LessonAssessment.objects.all().order_by('?')[:80]

        return questions



#################### AJAX requests if exam submitted ####################
def assessmentTook(request):
    #Insert log to database
    user_log = UserLog()
    user_log.log_by = request.user.username
    user_log.action = "took an assessment"
    user_log.date_time_logged = datetime.datetime.now()
    user_log.save() 

    return JsonResponse({}, status = 200)

def mockTook(request):
    #Insert log to database
    user_log = UserLog()
    user_log.log_by = request.user.username
    user_log.action = "took a mock test"
    user_log.date_time_logged = datetime.datetime.now()
    user_log.save() 

    return JsonResponse({}, status = 200)

def assessmentPerfected(request):
    user = request.user

    #Insert log to database
    user_log = UserLog()
    user_log.log_by = request.user.username
    user_log.action = "took an assessment"
    user_log.date_time_logged = datetime.datetime.now()
    user_log.save() 

    #Log the achievement
    if user.profile.assessment_perfected == False:
        achievement_log = AchievementLog()
        achievement_log.achieved_by = user
        achievement_log.achievement = "Lù Antlers"
        achievement_log.date_time_achieved = datetime.datetime.now()
        achievement_log.save()

    user.profile.assessment_perfected = True
    user.save()

    return JsonResponse({}, status = 200)

def mockPerfected(request):
    user = request.user

    #Insert log to database
    user_log = UserLog()
    user_log.log_by = request.user.username
    user_log.action = "took a mock test"
    user_log.date_time_logged = datetime.datetime.now()
    user_log.save() 

    #Log the achievement
    if not user.profile.mock_perfected:
        achievement_log = AchievementLog()
        achievement_log.achieved_by = user
        achievement_log.achievement = "Lost Coin of Shihuangdi"
        achievement_log.date_time_achieved = datetime.datetime.now()
        achievement_log.save()

    user.profile.mock_perfected = True
    user.save()

    return JsonResponse({}, status = 200)