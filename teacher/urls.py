from django.urls import path

from . import views

app_name = "teacher"

urlpatterns = [
    path('', views.index, name='index'),
    path('get_not_enrolled_students', views.get_not_enrolled_students, name='get_not_enrolled_students'),
    path('enroll_student', views.enroll_student, name='enroll_student'),
    path('view_enrolled_students', views.view_enrolled_students, name='view_enrolled_students'),
    path('get_attendance', views.get_attendance, name='get_attendance'),
    path('save_attendance', views.save_student_attendance, name='save_attendance'),
]