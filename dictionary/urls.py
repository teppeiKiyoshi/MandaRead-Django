from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.DictionaryList.as_view(), name='mandaread-dict'),
]
