from calendar import monthrange
from typing import List

from django.contrib.auth.models import User

from student.models import Enrollment
from teacher.models import Standard


def is_student_enrolled_in_a_class(student: User) -> bool:
    return Enrollment.objects.filter(student=student).exists()


def not_enrolled_students() -> List[User]:
    return [student for student in User.objects.filter(extendeduser__type='Student') if not is_student_enrolled_in_a_class(student)]


def enrolled_students(standard_obj: Standard):
    return Enrollment.objects.filter(standard=standard_obj)


def get_student_class(user: User) -> Standard:
    query = Enrollment.objects.filter(student=user)
    if query.exists():
        return query[0].standard


def get_number_of_days_in_month(month, year):
    return monthrange(year, month)[1]
