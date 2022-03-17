from django.views.generic import ListView
from lessonbank.models import LessonBank

#################### Assessments List View ####################
class AssessmentsListView(ListView):
    template_name = "assessments/assessment_list.html"
    model = LessonBank

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_list_1'] = LessonBank.objects.filter(hsk=1)
        context['lesson_list_2'] = LessonBank.objects.filter(hsk=2)
        return context