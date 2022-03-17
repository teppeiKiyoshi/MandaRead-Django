from django.shortcuts import render
from django.views.generic import ListView
from .models import Dictionary

#################### Imports for User Logging ####################
from adminmode.models import UserLog
import datetime

#################### Dictionary View ####################
class DictionaryList(ListView):
    model = Dictionary
    template_name = "dictionary/dictionary.html"
    context_object_name = 'words'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        #Insert log to database
        user_log = UserLog()
        user_log.log_by = request.user.username
        user_log.action = "opened the dictionary"
        user_log.date_time_logged = datetime.datetime.now()
        user_log.save() 
        return super().dispatch(request, *args, **kwargs)