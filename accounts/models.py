from django.contrib.auth.models import User
from django.db import models


user_types = (
    ('Teacher', 'Teacher'),
    ('Student', 'Student'),
    ('Staff', 'Staff'),
    ('Admin', 'Admin'),
)


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(choices=user_types, max_length=50)
