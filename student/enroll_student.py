from django.contrib.auth.models import User

from student.helpers import is_student_enrolled_in_a_class
from student.models import Enrollment
from teacher.models import Standard


class EnrollStudent:
    def __init__(self, user: User, standard_name: str = None, standard_obj: Standard = None):
        if user.extendeduser.type != 'Teacher' and user.extendeduser.type != 'Admin':
            raise Exception("Only Teachers and Admins are allowed to enroll students.")

        if standard_name is None and standard_obj is None:
            raise Exception("Standard name or object is required to instantiate enrollment class")

        if standard_obj is not None:
            self.standard_obj = standard_obj
        else:
            self.standard_obj = Standard.objects.get(class_name=standard_name)

        self.user = user

    def enroll_student(self, student_id: str):
        """
        Returns string containing error msg if enrollment failed...else returns None
        """
        student = User.objects.get(id=student_id)
        
        if student.extendeduser.type != 'Student':
            raise Exception("Only student types can be enrolled in a class")

        if is_student_enrolled_in_a_class(student):
            return f"{student.get_full_name()} is already enrolled in a class."

        Enrollment.objects.create(
            standard=self.standard_obj,
            student=student,
            enrolled_by=self.user,
        )
        return None
    
    def get_enrolled_students(self):
        enrollments = Enrollment.objects.filter(standard=self.standard_obj)
        enrollment_list = []
        for enrollment in enrollments:
            enrollment_list.append({
                "name": enrollment.student.get_full_name(),
                "enrolled_by": enrollment.enrolled_by.get_full_name(),
                "enrollment_date": enrollment.enrolled_on.strftime("%d-%b-%Y"),
            })
        return enrollment_list
