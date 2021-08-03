from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from accounts.helpers import exception_msg
from student.helpers import get_student_class
from student.view_attendance_helper import ViewAttendance


@login_required(login_url='/')
@require_GET
def index(request):
    student_class = get_student_class(request.user)
    context = {
        "standard": student_class
    }
    return render(request, "student/index.html", context)


@login_required(login_url='/')
@require_POST
def view_attendance(request):
    try:
        date = request.POST["date"]
        standard = request.POST["standard"]

        view_helper = ViewAttendance(request.user, date, standard)
        records = view_helper.get_attendance_for_date()

        return JsonResponse({"status": True, "records": records})
    except Exception as e:
        exception_msg("view_attendance", e)
        return JsonResponse({"status": False, "msg": "Something went wrong while getting records. Please try again."})
