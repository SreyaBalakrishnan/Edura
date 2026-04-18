from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class department(models.Model):
    department_name=models.CharField(max_length=100)

class course(models.Model):
    course_name=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    DEPARTMENT=models.ForeignKey(department,on_delete=models.CASCADE)

class student(models.Model):
    name=models.CharField(max_length=100)
    roll_no=models.CharField(max_length=100)
    COURSE=models.ForeignKey(course,on_delete=models.CASCADE)
    year=models.CharField(max_length=100)
    semester=models.CharField(max_length=100)
    number=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)

class faculty(models.Model):
    name=models.CharField(max_length=100)
    DEPARTMENT = models.ForeignKey(department,on_delete=models.CASCADE)
    designation=models.CharField(max_length=100)
    number=models.CharField(max_length=100)
    profile_picture=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)

class subject(models.Model):
    subname = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    COURSE=models.ForeignKey(course,on_delete=models.CASCADE)

class subject_allocation(models.Model):
    FACULTY=models.ForeignKey(faculty,on_delete=models.CASCADE)
    SUBJECT=models.ForeignKey(subject,on_delete=models.CASCADE)

class material(models.Model):
    SUBJECT_ALLOCATION=models.ForeignKey(subject_allocation,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    file=models.CharField(max_length=100)
    date=models.CharField(max_length=100)

class assignment(models.Model):
    SUBJECT_ALLOCATION = models.ForeignKey(subject_allocation,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description= models.CharField(max_length=500)
    date= models.CharField(max_length=100)
    submission_date= models.CharField(max_length=100)

class events(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    event_date = models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class event_participation(models.Model):
    EVENT=models.ForeignKey(events,on_delete=models.CASCADE)
    STUDENT=models.ForeignKey(student,on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    result = models.CharField(max_length=100)

class complaint(models.Model):
    complaint= models.CharField(max_length=500)
    complaint_date= models.CharField(max_length=100)
    STUDENT=models.ForeignKey(student,on_delete=models.CASCADE)
    reply= models.CharField(max_length=100)
    reply_date= models.CharField(max_length=100)

class notifition(models.Model):
    title = models.CharField(max_length=100)
    message= models.CharField(max_length=500)
    date = models.CharField(max_length=100)

class chatbot(models.Model):
    date = models.CharField(max_length=100)
    message = models.CharField(max_length=5000)
    type = models.CharField(max_length=100)
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE)

class attendance(models.Model):
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE)
    SUBJECT_ALLOCATION = models.ForeignKey(subject_allocation, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class internal_marks(models.Model):
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE)
    SUBJECT_ALLOCATION = models.ForeignKey(subject_allocation, on_delete=models.CASCADE)
    marks = models.CharField(max_length=100)
    max_marks = models.CharField(max_length=100)

class feedback(models.Model):
    FACULTY = models.ForeignKey(faculty, on_delete=models.CASCADE)
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE)
    feedbacks = models.CharField(max_length=100)
    feedback_date = models.CharField(max_length=100)

class group(models.Model):
    group_name= models.CharField(max_length=100)
    image= models.CharField(max_length=100)
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on= models.CharField(max_length=100)

class group_member(models.Model):
    GROUP = models.ForeignKey(group, on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)

class group_chat(models.Model):
    date = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    GROUP_MEMBER = models.ForeignKey(group_member, on_delete=models.CASCADE)

class previous_notes(models.Model):
    date = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    file = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    SUBJECT = models.ForeignKey(subject, on_delete=models.CASCADE)
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE)

class note_request(models.Model):
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    payment_date = models.CharField(max_length=100)
    payment_amount = models.CharField(max_length=100)
    PREVIOUS_NOTES = models.ForeignKey(previous_notes, on_delete=models.CASCADE)
    STUDENT = models.ForeignKey(student, on_delete=models.CASCADE)


