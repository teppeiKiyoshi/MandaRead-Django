from django.urls import path, include
from . import views

urlpatterns = [
    # Home
    path('', views.AdminHome.as_view(), name='admin-home'),
    path('users/', views.AdminManageUsers.as_view(), name='admin-users'),
    path('users/edit/<int:pk>/', views.AdminEditUser.as_view(), name='admin-edit-user'),
    path('users/delete/<int:pk>/', views.AdminDeleteUser.as_view(), name='admin-delete-user'),

    # Reports
    path('reports/<str:report>/<str:filter>/', views.AdminReports.as_view(), name='admin-reports'),

    # Lessons
    path('lessons/', views.AdminLessons.as_view(), name='admin-lessons'),
    path('lessons/<int:pk>/', views.AdminLesson.as_view(), name='admin-lesson'),
    path('lessons/new/', views.AdminCreateLesson.as_view(), name='admin-create-lesson'),
    path('lessons/<int:pk>/update/', views.AdminUpdateLesson.as_view(), name='admin-update-lesson'),
    path('lessons/<int:pk>/delete/', views.AdminDeleteLesson.as_view(), name='admin-delete-lesson'),

    #Dictionary
    path('dictionary/', views.AdminDictionary.as_view(), name='admin-dict'),
    path('dictionary/createword/', views.AdminCreateDictionary.as_view(), name='admin-create-dict'),
    path('dictionary/editword/<int:pk>/', views.AdminUpdateDictionary.as_view(), name='admin-update-dict'),
    path('dictionary/deleteword/<int:pk>/', views.AdminDeleteDictionary.as_view(), name='admin-delete-dict'),

    #Assessments
    path('assessments/', views.AdminAssessments.as_view(), name='admin-assessments'),
    path('assessments/<int:pk>/', views.AdminAssessmentDetail.as_view(), name='admin-assessment'),
    path('assessments/<int:pk>/create/', views.AdminCreateItemView.as_view(), name='admin-assessment-create'),
    path('assessments/updateitem/<int:pk>/', views.AdminUpdateItemView.as_view(), name='admin-assessment-update'),
    path('assessments/deleteitem/<int:pk>/', views.AdminDeleteItemView.as_view(), name='admin-assessment-delete')
]
