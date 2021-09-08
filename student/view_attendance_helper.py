import datetime

from django.contrib.auth.models import User

from staff.models import StaffAttendanceRecord
from student.helpers import get_number_of_days_in_month
from teacher.models import AttendanceRecord, Standard


class ViewAttendance:
    def __init__(self, user: User, date: str, standard: str = None):
        self.user = user
        self.date = datetime.datetime.strptime(date, "%Y-%m")
        self.standard = standard
        
    def get_attendance_for_date(self):
        days = [i for i in range(1, get_number_of_days_in_month(self.date.month, self.date.year) + 1)]

        if self.user.extendeduser.type == 'Student':
            saved_records = self._load_student_attendance_records()
        elif self.user.extendeduser.type == 'Staff':
            saved_records = self._load_staff_attendance_records()
        else:
            raise Exception("Expected Student or Staff type.")

        record = []
        for day in days:
            details = {
                "date": datetime.datetime(year=self.date.year, month=self.date.month, day=day).strftime("%d-%b-%Y")
            }
            is_present = "NA"
            if saved_records.filter(day__day=day).exists():
                if saved_records.filter(day__day=day)[0].present is True:
                    is_present = "Present"
                elif saved_records.filter(day__day=day)[0].present is False:
                    is_present = "Absent"

            details["status"] = is_present
                
            record.append(details)
        return record

    def _load_student_attendance_records(self):
        return AttendanceRecord.objects.filter(standard__class_name=self.standard, student=self.user,
                                        day__year=self.date.year, day__month=self.date.month)

    def _load_staff_attendance_records(self):
        return StaffAttendanceRecord.objects.filter(staff=self.user, day__year=self.date.year,
                                                    day__month=self.date.month)

