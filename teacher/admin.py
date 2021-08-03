from django.contrib import admin

from teacher.models import Standard, Subject, AttendanceRecord

admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(AttendanceRecord)