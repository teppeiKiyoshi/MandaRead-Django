from django.contrib import admin
from mandaread import views as mandaread_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    #Original admin site
    path('admin-overridden/', admin.site.urls),

    #Custom admin site
    path('admin/', include('adminmode.urls')),

    #Apps
    path('', include('landing.urls')),
    path('home/', include('mandaread.urls')),
    path('lessons/', include('lessonbank.urls')),
    path('dictionary/', include('dictionary.urls')),
    path('assessments/', include('assessments.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

