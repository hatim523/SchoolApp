from django.contrib.auth.models import User
from django.db.models import QuerySet

from teacher.models import Standard


def get_classes_taught_by_teacher(user: User) -> QuerySet:
    return Standard.objects.filter(teacher=user)