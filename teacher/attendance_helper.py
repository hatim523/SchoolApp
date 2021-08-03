import datetime
import json

from django.contrib.auth.models import User

from student.helpers import enrolled_students
from teacher.models import Standard, AttendanceRecord


class MarkStudentAttendance:
    def __init__(self, user: User, standard_name: str, attendance_date: str):
        if user.extendeduser.type != 'Teacher' and user.extendeduser.type != 'Admin':
            raise Exception("Class accessible only by Teachers or Admins")

        self.user = user
        self.standard_obj = Standard.objects.get(class_name=standard_name)
        self.attendance_date = datetime.datetime.strptime(attendance_date, "%Y-%m-%d")

        self.attendance_records = AttendanceRecord.objects.filter(day=self.attendance_date, standard=self.standard_obj)

    def get_attendance(self):
        enrolled = enrolled_students(self.standard_obj)
        attendance_records = []
        for enrollment in enrolled:
            attendance_records.append({"name": enrollment.student.get_full_name(),
                                       "id": enrollment.student.id,
                                       "present": "" if not self.attendance_records.filter(
                                           student=enrollment.student).exists() else \
                                           self.attendance_records.filter(student=enrollment.student)[0].present})
        return attendance_records

    def save_attendance(self, records: list):
        for record in records:
            try:
                record['present'] = json.loads(record['present'])
            except:
                pass
            is_present = None if record['present'] == '' else record['present']
            if self.attendance_records.filter(student_id=record['id']).exists():
                self.attendance_records.filter(student_id=record['id']).update(present=is_present)
            else:
                self.create_attendance_record(record['id'], is_present)

    def create_attendance_record(self, student, is_present):
        AttendanceRecord.objects.create(
            day=self.attendance_date,
            standard=self.standard_obj,
            student_id=student,
            present=is_present,
        )
