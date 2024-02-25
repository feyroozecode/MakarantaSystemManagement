from .models import Student
import datetime 

def generate_student_number():
        last_student = Student.objects.all().order_by('id').last()
        if not last_student:
            return 'M-' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + '000'
        student_id = last_student.id
        student_int = int(student_id[9:13])
        new_student_int = student_int + 1
        new_student_id = 'M-' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(new_student_int).zfill(4)
        
        return new_student_id
