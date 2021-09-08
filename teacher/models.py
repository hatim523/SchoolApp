import datetime

from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=200, primary_key=True)


class Standard(models.Model):   # Stores classes
    class_name = models.CharField(max_length=200, primary_key=True)
    teacher = models.ManyToManyField(User, limit_choices_to={'extendeduser__type': 'Teacher'})
    subjects = models.ManyToManyField(Subject)


class AttendanceRecord(models.Model):
    day = models.DateField()
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    present = models.BooleanField(blank=True, null=True)
