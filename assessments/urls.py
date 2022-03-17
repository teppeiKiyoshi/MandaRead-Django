from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssessmentsListView.as_view(), name='mandaread-assessments')
]
