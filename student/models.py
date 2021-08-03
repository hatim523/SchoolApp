from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from teacher.models import Standard


class Enrollment(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    student = models.ForeignKey(User, limit_choices_to={'extendeduser__type': 'Student'}, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(default=timezone.now)
    enrolled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_by')
