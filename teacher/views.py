import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from accounts.helpers import exception_msg
from student.enroll_student import EnrollStudent
from student.helpers import not_enrolled_students
from teacher.attendance_helper import MarkStudentAttendance
from teacher.helpers import get_classes_taught_by_teacher


@login_required(login_url='/')
def index(request):
    context = {
        "classes": get_classes_taught_by_teacher(request.user),
    }
    return render(request, "teacher/index.html", context)


@login_required(login_url='/')
@require_GET
def get_not_enrolled_students(request):
    try:
        student_list = []
        for student in not_enrolled_students():
            student_list.append({
                "name": student.get_full_name(),
                "id": student.id,
                "email": student.email,
            })

        return JsonResponse({"status": True, "student_list": student_list})
    except Exception as e:
        exception_msg("get_not_enrolled_students", e)
        return JsonResponse({"status": False, "msg": "Something went wrong while getting student information."})


@login_required(login_url='/')
@require_POST
def enroll_student(request):
    try:
        standard_name = request.POST['standard']
        student_id = request.POST['student_id']

        enrollment_helper = EnrollStudent(request.user, standard_name=standard_name)
        enrollment_helper.enroll_student(student_id)
        return JsonResponse({"status": True})
    except Exception as e:
        exception_msg("enroll_student", e)
        return JsonResponse({"status": False, "msg": "Something went wrong while enrolling student. "
                                                     "Please try again."})


@login_required(login_url='/')
@require_POST
def view_enrolled_students(request):
    try:
        standard_name = request.POST['standard']

        enrollment_helper = EnrollStudent(request.user, standard_name=standard_name)
        enrolled_students = enrollment_helper.get_enrolled_students()

        return JsonResponse({"status": True, "enrolled_students": enrolled_students})
    except Exception as e:
        exception_msg("view_enrolled_students", e)
        return JsonResponse({"status": False, "msg": "Something went wrong while fetching enrolled students. "
                                                     "Please try again."})


@login_required(login_url='/')
@require_POST
def get_attendance(request):
    try:
        standard_name = request.POST['standard']
        date = request.POST['date']

        attendance_helper = MarkStudentAttendance(request.user, standard_name, date)
        return JsonResponse({"status": True, "records": attendance_helper.get_attendance()})
    except Exception as e:
        exception_msg("get_attendance", e)
        return JsonResponse({"status": False, "msg": "Something went wrong while fetching attendance records. "
                                                     "Please try again."})


@login_required(login_url='/')
@require_POST
def save_student_attendance(request):
    try:
        records = json.loads(request.POST['records'])
        standard_name = request.POST['standard']
        date = request.POST['date']

        attendance_helper = MarkStudentAttendance(request.user, standard_name, date)
        attendance_helper.save_attendance(records)

        return JsonResponse({"status": True})
    except Exception as e:
        exception_msg("save_student_attendance", e)
        return JsonResponse({"status": False, "msg": "Could not save attendance. Please try again."})