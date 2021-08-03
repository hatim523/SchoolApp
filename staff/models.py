from django.contrib.auth.models import User
from django.db import models


class StaffAttendanceRecord(models.Model):
    day = models.DateField()
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(blank=True, null=True)
