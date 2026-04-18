import datetime
import random
import smtplib
import re
import json
import io
import requests as http

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from myapp.models import *


def welcome(request):
    return HttpResponse("hiiii")

def login1(request):
    return render(request,'login.html')
def login1post(request):
    name=request.POST['username']
    passwd=request.POST['password']
    data=authenticate(request,username=name,password=passwd)
    print(data)
    if data is not None:
        login(request, data)
        if data.is_superuser:
            return HttpResponse("<script>alert('Login successful');window.location='/Admin_home'</script>")
        elif data.groups.filter(name='staff').exists():
            request.session['stid'] = faculty.objects.get(LOGIN=request.user.id).id
            return HttpResponse("<script>alert('Welcome Faculty');window.location='/Faculty_home'</script>")
        elif data.groups.filter(name='student').exists():
            request.session['sid'] = student.objects.get(LOGIN=request.user.id).id
            return HttpResponse("<script>alert('Welcome Student');window.location='/student_home'</script>")
        
        return HttpResponse("<script>alert('Login successful');window.location='/Admin_home'</script>")
    else:
        return HttpResponse("<script>alert('Login failed')</script>")


def changepwd(request):
    return render(request, 'Admin/changepwd.html')

def changepwdpost(request):
    current=request.POST['cupasswd']
    new=request.POST['newpasswd']
    confirm=request.POST['confpasswd']

    check=check_password(current,request.user.password)
    if check:
      if new==confirm:
          user=request.user
          user.set_password(new)
          logout(request)
          user.save()
          return HttpResponse("<script>alert('Password changed succesfully')</script>")
      else:
          return HttpResponse("<script>alert('New and confirm passwords are not matching')</script>")
    else:
        return HttpResponse("<script>alert('current  password not matching')</script>")

def Admin_home(request):
    request.session['data1']=department.objects.all().count()
    request.session['data2']=faculty.objects.all().count()
    request.session['data3']=student.objects.all().count()
    request.session['data4']=events.objects.all().count()
    data5=faculty.objects.filter().order_by('-id')
    data6=subject.objects.filter().order_by('-id')
    data7=notifition.objects.filter().order_by('-id')
    data8=events.objects.filter().order_by('-id')
    return render(request,'Admin/admin_index.html',{'data5':data5,'data6':data6,'data7':data7,'data8':data8})


def Admin_add_dept(request):
    return render(request,'Admin/dept_add.html')

def deparmentaddpost(request):
    dptname=request.POST['dptname']
    obj=department()
    obj.department_name=dptname
    obj.save()
    return HttpResponse("<script>alert('Deparment added successfully');window.location='/Admin_view_dept'</script>")


def Admin_view_dept(request):
    data=department.objects.all()
    return render(request,'Admin/dept_view.html',{'data':data})

def Admin_edit_dept(request,id):
    data=department.objects.get(id=id)
    return render(request,'Admin/dept_edit.html',{'id':id,'data':data})

def departmenteditpost(request,id):
    dptname=request.POST['dptname']
    department.objects.filter(id=id).update(department_name=dptname)
    return HttpResponse("<script>alert('Deparment edited successfully');window.location='/Admin_view_dept'</script>")

def departmentdltpost(request,id):
    department.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Deparment deleted successfully');window.location='/Admin_view_dept'</script>")

def Admin_add_staff(request,id):
    data=department.objects.get(id=id)
    return render(request,'Admin/staff_add.html',{'id':id,'data':data})

def staffaddpost(request,id):
    name=request.POST['textfield']
    Designation=request.POST['textfield2']
    Number=request.POST['textfield3']
    propic = ""
    if 'fileField' in request.FILES:
        Profilepic = request.FILES['fileField']
        fs = FileSystemStorage()
        propic = fs.save(Profilepic.name, Profilepic)
        propic = fs.url(propic)
    else:
        # Use a default image if none provided
        propic = "/static/img/default.png"
    
    Email=request.POST['textfield5']
    pwd=str(random.randint(1111,9999))


    if User.objects.filter(username=Email).exists():
        return HttpResponse("<script>alert('Email already exists');history.back();window.location='/Admin_add_staff'</script>")
    else:
        auth_usr=User()
        auth_usr.username=Email
        auth_usr.password=make_password(pwd)
        print('password=',pwd)
        auth_usr.save()
        auth_usr.groups.add(Group.objects.get(name='staff'))
    obj=faculty()
    obj.name=name
    obj.DEPARTMENT_id=id
    obj.designation=Designation
    obj.number=Number
    obj.profile_picture=propic
    obj.email=Email
    obj.LOGIN=auth_usr
    obj.save()
    return HttpResponse("<script>alert('Staff added successfully');window.location='/Admin_view_staff'</script>")



def Admin_view_staff(request):
    data=faculty.objects.all()
    return render(request,'Admin/staff_view.html',{'data':data})

def Admin_edit_staff(request,id):
    data=faculty.objects.get(id=id)
    return render(request,'Admin/staff_edit.html',{'id':id,'data':data})

def staffeditpost(request,id):
    name = request.POST['textfield']
    Designation = request.POST['textfield2']
    Number = request.POST['textfield3']
    if 'fileField' in request.FILES:
        Profilepic = request.FILES['fileField']
        fs=FileSystemStorage()
        propic=fs.save(Profilepic.name,Profilepic)
        faculty.objects.filter(id=id).update(profile_picture=fs.url(propic))
    faculty.objects.filter(id=id).update(name=name,designation=Designation,number=Number)
    return HttpResponse("<script>alert('Staff edited successfully');window.location='/Admin_view_staff'</script>")



def staffdltpost(request,id):
    faculty.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Staff deleted successfully');window.location='/Admin_view_staff'</script>")

def staff_alloc(request, id):
    request.session['subid']=id
    data=faculty.objects.all()
    return render(request,'Admin/staff_alloc.html',{'data':data})

def allocate_sub(request,id):
    obj=subject_allocation()
    obj.FACULTY_id = id
    obj.SUBJECT_id = request.session['subid']
    obj.save()
    return HttpResponse("<script>alert('Allocated successfully');window.location='/Admin_view_staff'</script>")


def Admin_add_course(request,id):
    data=department.objects.get(id=id)
    return render(request,'Admin/course_add.html',{'id':id,'data':data})

def courseaddpost(request,id):
    course_name=request.POST['coursename']
    duration=request.POST['courseduration']
    obj=course()
    obj.course_name=course_name
    obj.duration=duration
    obj.DEPARTMENT_id=id
    obj.save()
    return HttpResponse("<script>alert('Course added successfully');window.location='/Admin_view_course'</script>")


def Admin_view_course(request):
    data=course.objects.all()
    return render(request,'Admin/course_view.html',{'data':data})

def Admin_edit_course(request,id):
    data=course.objects.get(id=id)
    return render(request,'Admin/course_edit.html',{'data':data,'id':id})

def courseeditpost(request,id):
    course_name = request.POST['coursename']
    duration = request.POST['courseduration']
    course.objects.filter(id=id).update(course_name=course_name,duration=duration)
    return HttpResponse("<script>alert('Course edited successfully');window.location='/Admin_view_course'</script>")

def Admin_delete_course(request,id):
    course.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Course deleted successfully');window.location='/Admin_view_course'</script>")

def Admin_add_subject(request,id):
    return render(request,'Admin/subject_add.html',{'id':id})

def subjectaddpost(request,id):
    subname=request.POST['coursename']
    semester=request.POST['courseduration']
    obj=subject()
    obj.subname=subname
    obj.semester=semester
    obj.COURSE_id=id
    obj.save()
    return HttpResponse("<script>alert('Subject added successfully');window.location='/Admin_view_subject'</script>")


def Admin_view_subject(request):
    data=subject.objects.all()
    return render(request,'Admin/subject_view.html',{'data':data})

def Admin_edit_subject(request,id):
    data=subject.objects.get(id=id)
    return render(request,'Admin/subject_edit.html',{'data':data,'id':id})

def subjecteditpost(request,id):
    subname = request.POST['coursename']
    semester = request.POST['courseduration']
    subject.objects.filter(id=id).update(subname=subname,semester=semester)
    return HttpResponse("<script>alert('Subject edited successfully');window.location='/Admin_view_subject'</script>")

def Admin_delete_subject(request,id):
    subject.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Subject deleted successfully');window.location='/Admin_view_subject'</script>")


def Admin_add_student(request,id):
    data=course.objects.get(id=id)
    return render(request,'Admin/student_add.html',{'id':id,'data':data})

def studentaddpost(request,id):
    name=request.POST['name']
    roll_no=request.POST['rollno']
    year=request.POST['year']
    semester=request.POST['textfield']
    number=request.POST['textfield2']
    email=request.POST['textfield3']
    pwd=str(random.randint(1111,9999))

    if User.objects.filter(username=email).exists():
         return HttpResponse("<script>alert('Email already exists');history.back();window.location='/Admin_add_student'</script>")

    auth_usr=User()
    auth_usr.username=email
    auth_usr.password=make_password(pwd)
    print(pwd)
    auth_usr.save()
    auth_usr.groups.add(Group.objects.get(name='Student'))

    obj=student()
    obj.name=name
    obj.roll_no=roll_no
    obj.year=year
    obj.semester=semester
    obj.number=number
    obj.email=email
    obj.LOGIN=auth_usr
    obj.COURSE_id=id
    obj.save()
    return HttpResponse("<script>alert('Student added');window.location='/Admin_view_student'</script>")



def Admin_view_student(request):
    data=student.objects.all()
    return render(request,'Admin/student_view.html',{'data':data})

def Admin_edit_student(request,id):
    data=student.objects.get(id=id)
    return render(request,'Admin/student_edit.html',{'id':id,'data':data})

def studenteditpost(request,id):
    name = request.POST['name']
    roll_no = request.POST['rollno']
    year = request.POST['year']
    semester = request.POST['textfield']
    number = request.POST['textfield2']
    student.objects.filter(id=id).update(name=name,roll_no=roll_no,year=year,semester=semester,number=number)
    return HttpResponse("<script>alert('Student edited successfully');window.location='/Admin_view_student'</script>")

def studentdltpost(request,id):
    student.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Student deleted successfully');window.location='/Admin_view_student'</script>")


def Admin_add_notification(request):
    return  render(request,'Admin/noti_add.html')

def notiaddpost(request):
    title=request.POST['textfield']
    message=request.POST['textfield2']
    date=request.POST['textfield3']
    obj=notifition()
    obj.title=title
    obj.message=message
    obj.date=date
    obj.save()
    return HttpResponse("<script>alert('Notification added successfully');window.location='/Admin_view_notification'</script>")



def Admin_view_notification(request):
    data = notifition.objects.all()
    return render(request,'Admin/noti_view.html',{'data':data})

def Admin_edit_notification(request,id):
    data = notifition.objects.get(id=id)
    return render(request,'Admin/noti_edit.html',{'data':data,'id':id})

def notieditpost(request,id):
    title = request.POST['textfield']
    message = request.POST['textfield2']
    date = request.POST['textfield3']
    notifition.objects.filter(id=id).update(title=title,message=message,date=date)
    return HttpResponse("<script>alert('Notification edited successfully');window.location='/Admin_view_notification'</script>")

def notidltpost(request,id):
    notifition.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Notification deleted successfully');window.location='/Admin_view_notification'</script>")


def Admin_view_complaint(request):
    data = complaint.objects.all()
    return render(request,'Admin/complaints_view.html',{'data':data})

def Admin_reply_complaint(request,id):
    data=complaint.objects.get(id=id)
    return render(request,'Admin/complaint_reply.html',{'data':data,'id':id})

def complaintreplypost(request,id):
    reply=request.POST['textfield']
    complaint.objects.filter(id=id).update(reply=reply,reply_date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    return HttpResponse("<script>alert('Replied successfully');window.location='/Admin_view_complaint'</script>")


def Admin_add_event(request):
    return render(request,'Admin/event_add.html')

def eventaddpost(request):
    title=request.POST['textfield']
    description=request.POST['textfield2']
    event_date=request.POST['textfield3']
    location=request.POST['textfield4']
    status=request.POST['textfield5']
    obj=events()
    obj.title=title
    obj.description=description
    obj.event_date=event_date
    obj.location=location
    obj.status=status
    obj.save()
    return HttpResponse("<script>alert('Event added successfully');window.location='/Admin_view_event'</script>")



def Admin_view_event(request):
    data=events.objects.all()
    return render(request,'Admin/event_view.html',{'data':data})

def Admin_edit_event(request,id):
    data=events.objects.get(id=id)
    return render(request,'Admin/event_edit.html',{'id':id,'data':data})

def eventeditpost(request,id):
    title = request.POST['textfield']
    description = request.POST['textfield2']
    event_date = request.POST['textfield3']
    location = request.POST['textfield4']
    status = request.POST['textfield5']
    events.objects.filter(id=id).update(title=title,description=description,event_date=event_date,location=location,status=status)
    return HttpResponse("<script>alert('Events edited successfully');window.location='/Admin_view_event'</script>")

def eventdlt(request,id):
    events.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Event deleted successfully');window.location='/Admin_view_event'</script>")


def Admin_prize_events(request,id):
    return render(request,'Admin/event_prize.html',{'id':id})

def eventprizepost(request,id):
    result=request.POST['select']
    print(id)
    event_participation.objects.filter(id=id).update(result=result,status='published')

    return HttpResponse("<script>alert('Result published successfully');window.location='/prize_view'</script>")

def prize_view(request):
    data=event_participation.objects.filter(~Q(status="pending"))
    return render(request,'Admin/prize_view.html',{'data':data})


def Admin_view_participants(request, id):
    data = event_participation.objects.filter(status='pending' )
    request.session['eid']=id
    return render(request,'Admin/participants_view.html',{'data':data,'id':id})

def Faculty_home(request):
    return render(request,'Faculty/facultyindex.html')

def Faculty_alloc_subject(request):
    data=subject_allocation.objects.filter(FACULTY_id=request.session['stid'])
    return render(request,'Faculty/subject_alloc.html',{'data':data})

def Faculty_add_material(request,id):
    data=subject_allocation.objects.get(id=id)
    return render(request,'Faculty/material_add.html',{'data':data,'id':id})

def materialaddpost(request,id):
    title=request.POST['textfield']
    if 'fileField' in request.FILES:
        file=request.FILES['fileField']
        fs=FileSystemStorage()
        fl=fs.save(file.name,file)
        fl_url = fs.url(fl)
    else:
        fl_url = "" # Set empty or default
    obj=material()
    obj.SUBJECT_ALLOCATION_id=id
    obj.title=title
    obj.file=fl_url
    obj.date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    obj.save()
    return HttpResponse("<script>alert('Material added successfully');window.location='/Faculty_view_material'</script>")

def Faculty_view_material(request):
    data=material.objects.filter(SUBJECT_ALLOCATION__FACULTY_id=request.session['stid'])
    return render(request,'Faculty/material_view.html',{'data':data})

def Faculty_edit_material(request,id):
    data=material.objects.get(id=id)
    return render(request,'Faculty/material_edit.html',{'data':data,'id':id})

def materialeditpost(request,id):
    title=request.POST['textfield']
    if 'fileField' in request.FILES:
        file=request.FILES['fileField']
        fs=FileSystemStorage()
        fl=fs.save(file.name,file)
        material.objects.filter(id=id).update(file=fs.url(fl))
    material.objects.filter(id=id).update(title=title)
    return HttpResponse("<script>alert('Material edited successfully');window.location='/Faculty_view_material'</script>")

def materialdlt(request,id):
    material.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Material deleted successfully');window.location='/Faculty_view_material'</script>")


def Faculty_add_assignment(request,id):
    data=subject_allocation.objects.get(id=id)
    return render(request,'Faculty/assignment_add.html',{'data':data,'id':id})

def assignmentaddpost(request,id):
    title=request.POST['textfield']
    description=request.POST['textfield2']
    submission_date=request.POST['textfield3']
    obj=assignment()
    obj.SUBJECT_ALLOCATION_id=id
    obj.title=title
    obj.description=description
    obj.date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    obj.submission_date=submission_date
    obj.save()
    return HttpResponse("<script>alert('Assignment added successfully');window.location='/Faculty_view_assignment'</script>")


def Faculty_view_assignment(request):
    data=assignment.objects.filter(SUBJECT_ALLOCATION__FACULTY_id=request.session['stid'])
    return render(request,'Faculty/assignment_view.html',{'data':data})

def Faculty_edit_assignment(request,id):
    data=assignment.objects.get(id=id)
    return render(request,'Faculty/Assignment_edit.html',{'data':data,'id':id})

def assignmenteditpost(request,id):
    title=request.POST['textfield']
    description=request.POST['textfield2']
    submission_date=request.POST['textfield3']
    assignment.objects.filter(id=id).update(title=title,description=description,submission_date=submission_date)
    return HttpResponse("<script>alert('Assignment edited successfully');window.location='/Faculty_view_assignment'</script>")

def assignmentdlt(request,id):
    assignment.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Assignment deleted successfully');window.location='/Faculty_view_assignment'</script>")


def Faculty_view_notification(request):
    data=notifition.objects.all()
    return render(request,'Faculty/noti_view.html',{'data':data})

def Faculty_view_event(request):
    data=events.objects.all()
    return render(request,'Faculty/event_view.html',{'data':data})

def Faculty_view_participants(request):
    data = event_participation.objects.all()
    return render(request, 'Faculty/participant_view.html', {'data': data})

def Faculty_result_event(request):
    data = event_participation.objects.filter(~Q(status='pending'))
    return render(request,'Faculty/events_results.html',{'data':data})

def Faculty_view_feedback(request):
    data=feedback.objects.all()
    return render(request,'Faculty/feedback_view.html',{'data':data})

def Faculty_add_attendance(request, id):
    alloc_obj=subject_allocation.objects.get(id=id)
    data=student.objects.filter(semester=alloc_obj.SUBJECT.semester, COURSE=alloc_obj.SUBJECT.COURSE)
    return render(request,'Faculty/attendance.html', {'data':data, 'id':id})

def attendanceaddpost(request, id):
    present_stud_list=request.POST.getlist('Attendance')
    alloc_obj=subject_allocation.objects.get(id=id)
    data=student.objects.filter(semester=alloc_obj.SUBJECT.semester, COURSE=alloc_obj.SUBJECT.COURSE)
    all_studs=[]
    for i in data:
        all_studs.append(i.id)
    for stud_id in all_studs:
        if str(stud_id) in present_stud_list:
            stat="Present"
        else:
            stat="Absent"
        data2=attendance.objects.filter(SUBJECT_ALLOCATION_id=id, STUDENT_id=stud_id, date=datetime.datetime.now().date())
        if data2.exists():
            obj = data2[0]
            obj.status = stat
            obj.save()
        else:
            obj=attendance()
            obj.date=datetime.datetime.now().date()
            obj.status=stat
            obj.STUDENT_id=stud_id
            obj.SUBJECT_ALLOCATION_id=id
            obj.save()
    return HttpResponse("<script>alert('Attendance Added Successfully');window.location='/faculty_view_attendance'</script>")

def faculty_view_attendance(request):
    data=attendance.objects.filter(SUBJECT_ALLOCATION__FACULTY_id=request.session['stid'],date=datetime.datetime.now().date())
    return render(request, 'Faculty/attendance_view.html', {'data': data})

def attendancedlt(request,id):
    attendance.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Attendance deleted successfully');window.location='/faculty_view_attendance'</script>")


def faculty_view_intstud(request,id):
    request.session['subid'] = id

    alloc_obj = subject_allocation.objects.get(id=id)
    data = student.objects.filter(semester=alloc_obj.SUBJECT.semester, COURSE=alloc_obj.SUBJECT.COURSE)
    return render(request,'Faculty/int_stud_view.html',{'data':data,'id':id,"alloc_obj":alloc_obj})

def Faculty_add_intmark(request,id):
    data=subject_allocation.objects.filter(SUBJECT_id=id)
    return render(request,'Faculty/intmarks_add.html',{'data':data,'id':id})

def intmarkaddpost(request,id):
    max_marks=request.POST['textfield']
    marks=request.POST['textfield2']
    obj=internal_marks()
    obj.STUDENT_id=id
    obj.SUBJECT_ALLOCATION_id=request.session['subid']
    obj.marks=marks
    obj.max_marks=max_marks
    obj.save()
    return HttpResponse("<script>alert('Internal Mark Added Successfully');window.location='/Faculty_view_intmark'</script>")



def Faculty_view_intmark(request):
    data=internal_marks.objects.filter(SUBJECT_ALLOCATION__FACULTY_id=request.session['stid'])
    return render(request,'Faculty/intmarks_view.html',{'data':data})

def Faculty_edit_intmark(request,id):
    data=internal_marks.objects.get(id=id)
    return render(request,'Faculty/intmarks_edit.html',{'data':data,'id':id})

def intmarkeditpost(request,id):
    max_marks=request.POST['textfield']
    marks=request.POST['textfield2']
    internal_marks.objects.filter(id=id).update(max_marks=max_marks,marks=marks)
    return HttpResponse("<script>alert('Internal Mark edited successfully');window.location='/Faculty_view_intmark'</script>")


def intmarkdlt(request,id):
    internal_marks.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Internal Mark deleted successfully');window.location='/Faculty_view_intmark'</script>")

def changepwdf(request):
    return render(request, 'Faculty/changepwd.html')

def changepwdfpost(request):
    current=request.POST['cupasswd']
    new=request.POST['newpasswd']
    confirm=request.POST['confpasswd']

    check=check_password(current,request.user.password)
    if check:
      if new==confirm:
          user=request.user
          user.set_password(new)
          logout(request)
          user.save()
          return HttpResponse("<script>alert('Password changed succesfully')</script>")
      else:
          return HttpResponse("<script>alert('New and confirm passwords are not matching')</script>")
    else:
        return HttpResponse("<script>alert('current  password not matching')</script>")






def userlogin(request):
    username=request.POST['username']
    passwd=request.POST['pwd']
    data = authenticate(request, username=username, password=passwd)

    print(data)
    if data is not None:
        login(request, data)
        if data.groups.filter(name__iexact='student').exists():
            data1=internal_marks.objects.filter(STUDENT__LOGIN=request.user.id).count()
            data2=attendance.objects.filter(STUDENT__LOGIN=request.user.id).count()
            data3=assignment.objects.filter().count()
            sid = student.objects.get(LOGIN_id=request.user.id).id
            return JsonResponse({"status":'success','sid':str(sid),'lid':request.user.id,'data1':data1,'data2':data2,'data3':data3})

    return JsonResponse({'status':'ok'})

def usr_view_profile(request):
    sid=request.POST['sid']
    data=student.objects.filter(id=sid)
    ar=[]
    for i in data:
        ar.append({'id':i.id,'name':i.name,'rollno':i.roll_no,'course':i.COURSE.course_name,'year':i.year,'semester':i.semester,'number':i.number,'email':i.email})
    return JsonResponse({'status':'ok','data':ar})

def usr_view_subject(request):
    data=subject.objects.filter()
    ar=[]
    for i in data:
        ar.append({'id':i.id,'subname':i.subname,'semester':i.semester,'course':i.COURSE.course_name})
    return JsonResponse({'status': 'ok', 'data': ar})

def add_previous_notes(request):
    id=request.POST['sid']
    title=request.POST['title']
    price=request.POST['price']
    fl_url = ""
    if 'file' in request.FILES:
        file=request.FILES['file']
        fs=FileSystemStorage()
        fl=fs.save(file.name,file)
        fl_url = fs.url(fl)
    
    subid=request.POST['subid']
    print(id)
    print(subid)
    obj=previous_notes()
    obj.date = datetime.datetime.now().date()
    obj.title=title
    obj.price=price
    obj.file=fs.url(file)
    obj.SUBJECT_id=subid
    obj.STUDENT_id=id
    obj.save()
    return JsonResponse({'status':'ok'})

def ai_lecture_notes(request):
    return JsonResponse({'status':'ok'})

# def chatbot(request):
#     return JsonResponse({'status':'ok'})

def dlt_previous_notes(request):
    id=request.POST['id']
    previous_notes.objects.filter(id=id).delete()
    return JsonResponse({'status':'ok'})

def edit_previous_notes(request):
    id = request.POST['id']
    title = request.POST['title']
    price = request.POST['price']


    if 'file' in request.FILES:
        file = request.FILES['file']
        fs = FileSystemStorage()
        file = fs.save(file.name, file)
        previous_notes.objects.filter(id=id).update(file=fs.url(file))
    previous_notes.objects.filter(id=id).update(title=title,date=datetime.datetime.now().date(),price=price)
    return JsonResponse({'status':'ok'})
#
# def group_chat(request):
#     return JsonResponse({'status': 'ok'})\


def make_payments(request):
    id=request.POST['id']
    note_request.objects.filter(id=id).update(status='paid', payment_date=datetime.datetime.now().date())
    return JsonResponse({'status': 'ok'})


def register_events(request):
    sid=request.POST['sid']
    id=request.POST['id']
    obj=event_participation()
    obj.EVENT_id=id
    obj.STUDENT_id=sid
    obj.status='pending'
    obj.result='pending'
    obj.save()
    return JsonResponse({'status': 'ok'})


def sent_compliants(request):
    id=request.POST['sid']
    comp=request.POST['complaint']
    print(id,comp)
    obj=complaint()
    obj.STUDENT_id=id
    obj.complaint=comp
    obj.complaint_date = datetime.datetime.now().date()
    obj.reply='pending'
    obj.reply_date='pending'
    obj.save()
    return JsonResponse({'status': 'ok'})

def sent_feedback(request):
    id=request.POST['fid']
    feed=request.POST['feedback']
    std=request.POST['sid']
    obj=feedback()
    obj.FACULTY_id=id
    obj.STUDENT_id=std
    obj.feedbacks=feed
    obj.feedback_date = datetime.datetime.now().date()
    obj.save()
    return JsonResponse({'status': 'ok'})

def student_home(request):
    return JsonResponse({'status': 'ok'})

def verify_request_notes(request):
    sid=request.POST['sid']
    data=note_request.objects.filter(~Q(STUDENT_id=sid),status='pending')
    ar=[]
    for i in data:
        ar.append({'id':i.id,'date':i.date,'status':i.status,'paymentdate':i.payment_date,'title':i.PREVIOUS_NOTES.title,'stdname':i.STUDENT.name})
    return JsonResponse({'status': 'ok','data':ar})

def accept_request(request):
    id=request.POST['id']
    note_request.objects.filter(id=id).update(status='accept')
    return JsonResponse({'status': 'accept'})

def reject_request(request):
    id=request.POST['id']
    note_request.objects.filter(id=id).update(status='reject')
    return JsonResponse({'status': 'reject'})


def view_approved_request(request):
    sid=request.POST['sid']
    data=note_request.objects.filter(status='accept',STUDENT_id=sid)
    ar=[]
    for i in data:
        ar.append({'id':i.id,'date':i.date,'status':i.status,'paymentdate':i.payment_date,'title':i.PREVIOUS_NOTES.title,'price':i.PREVIOUS_NOTES.price})
    return JsonResponse({'status': 'ok','data':ar})

def view_assignments(request):
    data=assignment.objects.all()
    ar=[]
    for i in data:
        ar.append({'id':i.id,'subject':i.SUBJECT_ALLOCATION.SUBJECT.subname,'title':i.title,'description':i.description,'date':i.date,'submission_date':i.submission_date})
    return JsonResponse({'status': 'ok','data':ar})


def view_attendance(request):
    id=request.POST['id']
    print(id)
    data=attendance.objects.filter(STUDENT_id=id)
    ar=[]
    for i in data:
        ar.append({'id':i.id,'student':i.STUDENT.name,'rollno':i.STUDENT.roll_no,'subject':i.SUBJECT_ALLOCATION.SUBJECT.subname,'date':i.date,'status':i.status})
    return JsonResponse({'status': 'ok','data':ar})

def view_faculty(request):
    data=faculty.objects.all()
    ar=[]
    for i in data:
        ar.append({'id':i.id,'name':i.name,'department':i.DEPARTMENT.department_name,'designation':i.designation,'number':i.number,'profile_pic':i.profile_picture,'email':i.email})
    return JsonResponse({'status':'ok','data':ar})

def view_events(request):
    data=events.objects.all()
    ar=[]
    for i in data:
        ar.append({'id':i.id,'title':i.title,'description':i.description,'event_date':i.event_date,'location':i.location,'status':i.status})
    return JsonResponse({'status': 'ok','data':ar})


def view_intmarks(request):
    id=request.POST['id']
    print(id)
    data=internal_marks.objects.filter(STUDENT_id=id)
    ar=[]
    for i in data:
        ar.append({'id':i.id,'student':i.STUDENT.name,'subject':i.SUBJECT_ALLOCATION.SUBJECT.subname,'marks':i.marks,'max_marks':i.max_marks})
    return JsonResponse({'status': 'ok','data':ar})


def view_materials(request):
    data=material.objects.all()
    ar=[]
    for i in data:
        ar.append({'id':i.id,'subject':i.SUBJECT_ALLOCATION.SUBJECT.subname,'title':i.title,'file':i.file,'date':i.date})
    return JsonResponse({'status': 'ok','data':ar})


def view_my_previous_notes(request):
    sid=request.POST['sid']
    data=previous_notes.objects.filter(STUDENT_id=sid)
    ar=[]
    for i in data:
        ar.append({'id':i.id,'date':i.date,'title':i.title,'file':i.file,'price':i.price,'subject':i.SUBJECT.subname,'student':i.STUDENT.name})
    return JsonResponse({'status': 'ok','data':ar})

def view_notifications(request):
    data=notifition.objects.all()
    ar=[]
    for i in data:
        ar.append({'id':i.id,'title':i.title,'message':i.message,'date':i.date})
    return JsonResponse({'status': 'ok','data':ar})

def view_ordered_previousnotes(request):
    sid=request.POST['sid']
    data=note_request.objects.filter(STUDENT_id=sid,status='paid')
    print(data)
    ar=[]
    for i in data:
        ar.append({'id':i.id,'date':i.date,'status':i.status,'payment_date':i.payment_date,'title':i.PREVIOUS_NOTES.title,'name':i.PREVIOUS_NOTES.SUBJECT.subname,'file':i.PREVIOUS_NOTES.file,'price':i.PREVIOUS_NOTES.price,'student':i.PREVIOUS_NOTES.STUDENT.name})

    return JsonResponse({'status': 'ok','data':ar})

def view_others_previousnotes(request):
    sid=request.POST['sid']
    data = previous_notes.objects.filter(~Q(STUDENT_id=sid))
    ar = []
    for i in data:
        ar.append({'id': i.id, 'date': i.date, 'title': i.title, 'file': i.file, 'price': i.price, 'subject': i.SUBJECT.subname, 'student': i.STUDENT.name,'sub_id':i.SUBJECT.id})

    return JsonResponse({'status': 'ok', 'data': ar})

def view_replies(request):
    data=complaint.objects.filter(~Q(reply="pending"))
    ar=[]
    for i in data:
        ar.append({'reply':i.reply,'reply_date':i.reply_date})
    return JsonResponse({'status': 'ok','data':ar})


def view_request_notes(request):
    sid=request.POST['sid']
    data = note_request.objects.filter(~Q(STUDENT_id=sid))
    ar=[]
    for i in data:
        ar.append({'id':i.id,'date':i.date,'status':i.status,'payment_date':i.payment_date,'title':i.PREVIOUS_NOTES.title,'student':i.STUDENT.name})
    return JsonResponse({'status': 'ok', 'data': ar})

def view_event_results(request):
    data=event_participation.objects.filter(~Q(status="pending"))
    ar=[]
    for i in data:
        ar.append({'id':i.id,'event':i.EVENT.title,'student':i.STUDENT.name,'status':i.status,'result':i.result})
    return JsonResponse({'status': 'ok','data':ar})

def send_request_for_notes(request):
    sid=request.POST['sid']
    pnid=request.POST['pnid']
    obj=note_request()
    obj.PREVIOUS_NOTES_id=pnid
    obj.STUDENT_id=sid
    obj.status='pending'
    obj.date=datetime.date.today()
    obj.save()
    return JsonResponse({'status':'ok'})




############### forgot flutter ###################




def forgotemail(request):
    import random
    import smtplib
    email = request.POST['email']
    print(email)
    data = User.objects.filter(username=email)
    print(data)
    if data.exists():
        otp = str(random.randint(000000, 999999))
        print(otp)
        # *✨ Python Email Codeimport smtplib*

        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # ✅ Gmail credentials (use App Password, not real password)
        try:
            sender_email = "collegeedura@gmail.com"
            receiver_email = "receiver_email@gmail.com"  # change to actual recipient
            app_password = "dwrl lyix enwb lcan"
            # Setup SMTP
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)

            # Create the email
            msg = MIMEMultipart("alternative")
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = "🔑 Forgot Password "

            # Plain text (backup)
            # text = f"""
            # Hello,

            # Your password for Smart Donation Website is: {pwd}

            # Please keep it safe and do not share it with anyone.
            # """

            # HTML (attractive)
            html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Password Reset OTP</title>
                </head>
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                            line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">

                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                        <h1 style="color: white; margin: 0; font-size: 28px;">
                            🔐 Smart Donation
                        </h1>
                    </div>

                    <div style="background-color: #f9f9f9; padding: 40px 30px; border-radius: 0 0 10px 10px; 
                                border: 1px solid #eaeaea;">

                        <h2 style="color: #2d3748; margin-top: 0;">Password Reset Request</h2>

                        <p style="color: #4a5568; font-size: 16px;">
                            Hello,
                        </p>

                        <p style="color: #4a5568; font-size: 16px;">
                            You requested to reset your password. Use the OTP below to proceed:
                        </p>

                        <div style="background: white; border-radius: 8px; padding: 20px; 
                                    text-align: center; margin: 30px 0; border: 2px dashed #cbd5e0;">
                            <div style="font-size: 32px; font-weight: bold; letter-spacing: 10px; 
                                        color: #2c7be5; margin: 10px 0;">
                                {otp}
                            </div>
                            <div style="font-size: 14px; color: #718096; margin-top: 10px;">
                                (Valid for 10 minutes)
                            </div>
                        </div>

                        <p style="color: #4a5568; font-size: 16px;">
                            Enter this code on the password reset page to complete the process.
                        </p>

                        <div style="background-color: #fef3c7; border-left: 4px solid #d97706; 
                                    padding: 15px; margin: 25px 0; border-radius: 4px;">
                            <p style="color: #92400e; margin: 0; font-size: 14px;">
                                ⚠️ <strong>Security tip:</strong> Never share this OTP with anyone. 
                                Our team will never ask for your password or OTP.
                            </p>
                        </div>

                        <p style="color: #718096; font-size: 14px;">
                            If you didn't request this password reset, please ignore this email or 
                            contact our support team if you have concerns.
                        </p>

                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">

                        <p style="text-align: center; color: #a0aec0; font-size: 12px;">
                            This is an automated email from Smart Donation System.<br>
                            © {datetime.datetime.now().year} Smart Donation. All rights reserved.
                        </p>

                    </div>
                </body>
                </html>
                """

            # Attach both versions
            # msg.attach(MIMEText(text, "plain"))
            msg.attach(MIMEText(html, "html"))

            # Send email
            server.send_message(msg)
            print("✅ Email sent successfully!", otp)

            # Close connection
            server.quit()

        except Exception as e:
            print("❌ Error loading email credentials:", e)
            return JsonResponse({'status': "ok", 'otpp': otp})

        return JsonResponse({'status': 'ok', 'otpp': otp})
    return JsonResponse({'status': "not found"})


def forgotpass(request):
    email = request.POST['email']
    npass = request.POST['password']
    cpass = request.POST['confirmpassword']
    print(email, npass, cpass)
    if npass == cpass:
        User.objects.filter(username=email).update(password=make_password(npass))
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'})



################ forgot web ##########################


def forgotpassword(request):
    return render(request,"forgotpassword.html")
def forgotpasswordbuttonclick(request):
    email = request.POST['textfield']
    if User.objects.filter(username=email).exists():
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        # ✅ Gmail credentials (use App Password, not real password)
        sender_email = "collegeedura@gmail.com"
        receiver_email = email  # change to actual recipient
        app_password = "dwrl lyix enwb lcan"  # App Password from Google
        pwd = str(random.randint(1100,9999))  # Example password to send
        request.session['otp'] = pwd
        request.session['email'] = email

        # Setup SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        # Create the email
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Your OTP"

        # Plain text (backup)
        # text = f"""
        # Hello,

        # Your password for Smart Donation Website is: {pwd}

        # Please keep it safe and do not share it with anyone.
        # """

        # HTML (attractive)
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color:#2c7be5;">Wastemanagement</h2>
            <p>Hello,</p>
            <p>Your OTP is:</p>
            <p style="padding:10px; background:#f4f4f4; 
                      border:1px solid #ddd; 
                      display:inline-block;
                      font-size:18px;
                      font-weight:bold;
                      color:#2c7be5;">
              {pwd}
            </p>
            <p>Please keep it safe and do not share it with anyone.</p>
            <hr>
            <small style="color:gray;">This is an automated email from Wastemanagement System.</small>
          </body>
        </html>
        """

        # Attach both versions
        # msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        # Send email
        server.send_message(msg)
        print("✅ Email sent successfully!")

        # Close connection
        server.quit()
        return HttpResponse("<script>window.location='/otp'</script>")
    else:
        return HttpResponse("<script>alert('Email not found');window.location='/forgotpassword'</script>")


def otp(request):
    return render(request,"otp.html")
def otpbuttonclick(request):
    otp  = request.POST["textfield"]
    if otp == str(request.session['otp']):
        return HttpResponse("<script>window.location='/forgotpswdpswed'</script>")
    else:
        return HttpResponse("<script>alert('incorrect otp');window.location='/otp'</script>")

def forgotpswdpswed(request):
    return render(request,"forgotpswdpswed.html")
def forgotpswdpswedbuttonclick(request):
    np = request.POST["password"]
    User.objects.filter(username=request.session['email']).update(password=make_password(np))
    return HttpResponse("<script>alert('password has been changed');window.location='/' </script>")


def user_sendchat(request):
    lid=request.POST['lid']
    g = request.POST['GROUP_id']


    # print(FROM_id, TOID_id,"Lk")
    print(lid)
    msg=request.POST['message']

    from  datetime import datetime


    c=group_chat()
    c.GROUP_MEMBER_id = g
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})

def user_viewchat(request):
    lid=request.POST['lid']
    # print(to_id)
    g = request.POST['GROUP_id']
    g=group_member.objects.get(id=g).GROUP
    l=[]
    data=group_chat.objects.filter(GROUP_MEMBER__GROUP=g).order_by('id')

    print(data)

    for res in data:
        if lid == str(res.GROUP_MEMBER.LOGIN_id):
            l.append({'id':res.id,'msg':"Me"+"\n"+res.message,'date':res.date,"type":"me"})
        else:
            l.append({'id':res.id,'msg':str(res.GROUP_MEMBER.LOGIN.username)+"\n"+res.message,'date':res.date,"type":"others"})




    return JsonResponse({'status':"ok",'data':l})


def view_group(request):
    lid=request.POST['lid']
    data=group_member.objects.filter(LOGIN_id=lid)
    ar = []
    for i in data:
        ar.append({'id':i.id,'grpname':i.GROUP.group_name,'profile':i.GROUP.image,'createdon':i.GROUP.created_on})
    return JsonResponse({'status': 'ok','data':ar})


# Install: pip install google-generativeai
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
import google.generativeai as genai


def single_question_chatbot(msg):
    # Configure with your API key
    genai.configure(api_key="AIzaSyBc-QemZ2IMv_6sHW1iYMBJvzPmtEB0WZk")

    # Try different model names in order
    model_names_to_try = [
        'gemini-1.5-pro',  # Most likely to work
        'gemini-1.5-pro-latest',
        'gemini-pro',  # Original (might work in some regions)
        'models/gemini-pro',  # Full path format
        'models/gemini-2.0-flash',
    ]

    response = None

    for model_name in model_names_to_try:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Give brief, short and accurate response to this query in the format of paragraph with less than 1000 characters" +msg)
            break  # Exit loop if successful
        except Exception as e:
            print(f"Failed with {model_name}: {str(e)[:100]}")
            continue

    if response is None:
        # Last resort: List available models
        print("\nListing all available models in your region:")
        available_models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
                print(f"  - {model.name}")

        if available_models:
            # Try the first available model
            try:
                model = genai.GenerativeModel(available_models[0])
                response = model.generate_content(msg)
            except Exception as e:
                return f"Error with available model: {str(e)}"
        else:
            return "No available models found with generateContent support"

    resp = response.text
    if len(resp) > 4950 :
        lst=resp.split("\n")
        for i in lst:
            print("******** ")
            print(i)
        lst_new=lst[:7]
        lst="".join(lst_new)
        print(lst)
        resp=lst
    print(resp)
    resp=resp.replace("*", "")
    return resp


#######     chatbot
def user_sendchatbot(request):
    sid=request.POST['sid']
    print(sid)
    msg=request.POST['message']

    from  datetime import datetime

    c=chatbot()
    c.message=msg
    c.date=datetime.now().strftime("%d-%m-%Y %H:%M")
    c.type="student"
    c.STUDENT_id=sid
    c.save()

    chat_resp=single_question_chatbot(msg)
    c = chatbot()
    c.message = chat_resp
    c.date = datetime.now().strftime("%d-%m-%Y %H:%M")
    c.type = "chatbot"
    c.STUDENT_id = sid
    c.save()

    return JsonResponse({'status':"ok"})

def user_viewchatbot(request):
    sid=request.POST['sid']
    l=[]
    data=chatbot.objects.filter(STUDENT_id=sid).order_by('id')
    print(data)
    for res in data:
        if res.type == "student":
            l.append({'id':res.id,'msg':"Me"+"\n"+res.message,'date':res.date,"type":"me"})
        else:
            l.append({'id':res.id,'msg':"Bot\n"+res.message,'date':res.date,"type":"bot"})
    return JsonResponse({'status':"ok",'data':l})






# def user_sendchat(request):
#     FROM_id=request.POST['from_id']
#
#     msg=request.POST['message']
#
#     # from  datetime import datetime
#     c=Chat()
#     c.USER_id=FROM_id
#     c.message=msg
#     c.type='user'
#     c.date=datetime.now()
#     c.save()
#
#     message = msg
#
#     import google.generativeai as genai
#
#     # Configure with your API key
#     genai.configure(api_key="AIzaSyAduEHNgfrIKbihOtLOAUJf9NsoXsw7MW0")  # Replace with your actual key
#
#
#     # for m in genai.list_models():
#     #     print(m.name, "→", m.supported_generation_methods)
#
#     # Initialize the model (using the correct flash model)
#     model = genai.GenerativeModel('models/gemini-2.5-flash-lite')  # ✅ Current fastest model
#     # Generate response with chatbot personality
#     response = model.generate_content(
#         f"""You are a friendly chat bot. Respond to the user's message with warmth and support.
#
#         User: {message}
#
#         Provide a conversational response that:
#         - Shows empathy and understanding
#         - Uses bullet points when helpful for clarity
#         - Keeps responses under 3 sentences unless more detail is needed
#         - Maintains a supportive, professional tone""",
#         generation_config={
#             "temperature": 0.7,
#             "max_output_tokens": 500
#         }
#     )
#     print("\nGemini:", response.text, "\n")
#
#     c = Chat()
#     c.USER_id= FROM_id
#     c.message = response.text
#     c.type = "AI"
#     c.date = datetime.now()
#     c.save()
#
#     return JsonResponse({'status':"ok"})
#
#
# def user_viewchat(request):
#     from_id=request.POST['from_id']
#
#
#     l=[]
#     data=Chat.objects.filter(USER_id=from_id).order_by('id')
#     for res in data:
#         l.append({'id':res.id,'from':res.USER.id,'msg':res.message,'date':res.date,'type':res.type})
#
#
#
#     return JsonResponse({'status':"ok",'data':l})


# ==================== TEXT AUTO-CORRECTION ====================

def correct_text(text):
    """
    Apply auto-correction to text including:
    - Spell checking and correction
    - Grammar fixes
    - Punctuation normalization
    - Capitalization fixes
    """
    try:
        # Try using language_tool_python for comprehensive correction
        from language_tool_python import LanguageTool
        
        tool = LanguageTool('en-US')
        matches = tool.check(text)
        
        # Apply corrections
        corrected = text
        for match in reversed(matches):  # Reverse to maintain position accuracy
            if match.replacements:
                # Use first suggestion
                replacement = match.replacements[0]
                corrected = corrected[:match.offset] + replacement + corrected[match.offset + match.length:]
        
        return corrected
    except:
        # Fallback to basic correction
        return apply_basic_correction(text)


def apply_basic_correction(text):
    """
    Apply basic text corrections including:
    - Common typo fixes
    - Spacing normalization
    - Capitalization
    """
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Fix spacing around punctuation
    text = re.sub(r'\s+([.!?,;:])', r'\1', text)
    text = re.sub(r'([.!?])\s+', r'\1 ', text)
    
    # Capitalize first letter of sentences
    sentences = text.split('. ')
    corrected_sentences = []
    for i, sentence in enumerate(sentences):
        if sentence.strip():
            # Capitalize first letter
            sentence = sentence.strip()
            sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            corrected_sentences.append(sentence)
    
    text = '. '.join(corrected_sentences)
    
    # Ensure sentence ends with period if it's not already
    if text and not text[-1] in '.!?':
        text += '.'
    
    # Common typo corrections dictionary
    corrections = {
        r'\bwoudl\b': 'would',
        r'\bshoudl\b': 'should',
        r'\bcoudl\b': 'could',
        r'\bdidnt\b': "didn't",
        r'\bwasnt\b': "wasn't",
        r'\bisnt\b': "isn't",
        r'\barent\b': "aren't",
        r'\bwont\b': "won't",
        r'\bcant\b': "can't",
        r'\bhavent\b': "haven't",
        r'\bhasnt\b': "hasn't",
        r'\brecieved\b': 'received',
        r'\boccured\b': 'occurred',
        r'\boccassion\b': 'occasion',
        r'\bneccessary\b': 'necessary',
        r'\bseperate\b': 'separate',
        r'\bthrough\b': 'through',
        r'\bwiht\b': 'with',
        r'\bwhcih\b': 'which',
        r'\bteh\b': 'the',
        r'\band\s+and\b': 'and',
        r'\bthe\s+the\b': 'the',
    }
    
    for typo, correction in corrections.items():
        text = re.sub(typo, correction, text, flags=re.IGNORECASE)
    
    return text


def correct_and_summarize(text, num_bullets=5):
    """
    Correct text and then summarize it
    Returns both corrected text and summary
    """
    # First correct the text
    corrected_text = correct_text(text)
    
    # Then summarize
    bullets = summarize_as_bullets(corrected_text, num_bullets)
    
    return {
        'original': text,
        'corrected': corrected_text,
        'bullets': bullets
    }


# ==================== TEXT SUMMARIZATION ENDPOINTS ====================

def summarize_text(request):
    """
    API endpoint to summarize text using multiple methods
    POST parameters:
    - text: Text to summarize (required)
    - method: 'quick' (fast Dart-based) or 'ai' (AI-based) - default 'quick'
    - correct: Apply auto-correction before summarizing (default True)
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '').strip()
            method = data.get('method', 'quick')
            apply_correction = data.get('correct', True)
            
            if not text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Text cannot be empty'
                }, status=400)
            
            if len(text) < 50:
                return JsonResponse({
                    'status': 'ok',
                    'summary': text,
                    'message': 'Text too short to summarize'
                })
            
            # Apply correction if requested
            if apply_correction:
                text = correct_text(text)
            
            if method == 'ai':
                summary = summarize_with_ai(text)
            else:
                summary = summarize_extractive(text)
            
            return JsonResponse({
                'status': 'ok',
                'summary': summary,
                'method': method,
                'corrected': apply_correction,
                'original_length': len(text.split()),
                'summary_length': len(summary.split()) if summary else 0
            })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method is allowed'
    }, status=405)


def summarize_bullets(request):
    """
    API endpoint to summarize text as bullet points
    POST parameters:
    - text: Text to summarize (required)
    - num_bullets: Number of bullet points to generate (default 5)
    - method: 'quick' (fast) or 'ai' (AI-based) - default 'quick'
    - correct: Apply auto-correction before summarizing (default True)
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '').strip()
            num_bullets = data.get('num_bullets', 5)
            method = data.get('method', 'quick')
            apply_correction = data.get('correct', True)
            
            if not text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Text cannot be empty'
                }, status=400)
            
            if len(text) < 50:
                return JsonResponse({
                    'status': 'ok',
                    'bullets': [text],
                    'count': 1,
                    'message': 'Text too short to summarize'
                })
            
            # Apply correction if requested
            if apply_correction:
                text = correct_text(text)
            
            if method == 'ai':
                bullets = summarize_as_bullets_ai(text, num_bullets)
            else:
                bullets = summarize_as_bullets(text, num_bullets)


            print("HIIIIIIIII",{
                'status': 'ok',
                'success': True,
                'bullets': bullets,
                'count': len(bullets),
                'method': method,
                'corrected': apply_correction
            })
            
            return JsonResponse({
                'status': 'ok',
                'success': True,
                'bullets': bullets,
                'count': len(bullets),
                'method': method,
                'corrected': apply_correction
            })
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method is allowed'
    }, status=405)


def summarize_extractive(text):
    """
    Simple extractive summarization using sentence extraction
    """
    import re
    
    if not text or len(text) < 50:
        return text
    
    # Clean text
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    if len(clean_text) < 100:
        return clean_text
    
    # Split into sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', clean_text)]
    sentences = [s for s in sentences if s and len(s) > 10]
    
    if not sentences:
        return clean_text[:200] + '...'
    
    # Select important sentences
    summary = []
    
    # Add first sentence
    if sentences:
        summary.append(sentences[0])
    
    # Add middle sentence
    if len(sentences) > 3:
        mid = len(sentences) // 2
        if sentences[mid] not in summary:
            summary.append(sentences[mid])
    
    # Add last sentence
    if len(sentences) > 1 and sentences[-1] not in summary:
        summary.append(sentences[-1])
    
    # Add a few more sentences
    for i in range(1, len(sentences)):
        if len(summary) >= 5:
            break
        s = sentences[i]
        if (s not in summary and 
            15 < len(s) < 300 and
            'thank' not in s.lower() and
            'please' not in s.lower()):
            summary.append(s)
    
    return ' '.join(summary)


def summarize_as_bullets(text, num_bullets=5):
    """
    Summarize text and return as bullet points (extractive method)
    """
    import re
    
    if not text or len(text) < 50:
        return [text]
    
    # Clean text
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', clean_text)]
    sentences = [s for s in sentences if s and len(s) > 10]
    
    if not sentences:
        return [clean_text[:300]]
    
    # Select sentences
    selected = []
    
    # Add first
    if sentences:
        selected.append(sentences[0])
    
    # Add middle
    if len(sentences) > 3:
        mid = len(sentences) // 2
        if sentences[mid] not in selected:
            selected.append(sentences[mid])
    
    # Add last
    if len(sentences) > 1 and sentences[-1] not in selected:
        selected.append(sentences[-1])
    
    # Add more
    for i in range(1, len(sentences)):
        if len(selected) >= num_bullets:
            break
        s = sentences[i]
        if (s not in selected and 
            15 < len(s) < 300 and
            'thank' not in s.lower() and
            'please' not in s.lower()):
            selected.append(s)
    
    # Format as bullets
    bullets = [re.sub(r'[.!?]+$', '', s).strip() + '.' for s in selected]
    return bullets


def summarize_with_ai(text):
    """
    Use Google Gemini AI for advanced summarization
    """
    try:
        import google.generativeai as genai
        
        # Configure with your API key (set in environment or settings)
        import os
        from django.conf import settings
        
        api_key = getattr(settings, 'GEMINI_API_KEY', os.getenv('GEMINI_API_KEY'))
        if not api_key:
            # Fallback to hardcoded key (not recommended for production)
            api_key = "AIzaSyAduEHNgfrIKbihOtLOAUJf9NsoXsw7MW0"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash-lite')
        
        prompt = f"""Please provide a concise summary of the following text in 3-5 sentences. 
Focus on the main points and key concepts.

Text:
{text}

Summary:"""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 300
            }
        )
        
        return response.text.strip()
    
    except Exception as e:
        print(f"AI summarization error: {e}")
        # Fallback to extractive summarization
        return summarize_extractive(text)


def summarize_as_bullets_ai(text, num_bullets=5):
    """
    Use Google Gemini AI to generate bullet points
    """
    try:
        import google.generativeai as genai
        
        # Configure with your API key
        import os
        from django.conf import settings
        
        api_key = getattr(settings, 'GEMINI_API_KEY', os.getenv('GEMINI_API_KEY'))
        if not api_key:
            api_key = "AIzaSyAduEHNgfrIKbihOtLOAUJf9NsoXsw7MW0"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash-lite')
        
        prompt = f"""Please summarize the following text as {num_bullets} bullet points. 
Each bullet point should be one sentence and capture a key concept.
Format: Use bullet points (•).

Text:
{text}

Summary:"""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 500
            }
        )
        
        # Parse bullet points from response
        lines = response.text.strip().split('\n')
        bullets = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                # Remove bullet markers
                bullet_text = line.lstrip('•-* ').strip()
                if bullet_text:
                    bullets.append(bullet_text)
        
        if not bullets:
            # Fallback: split by newlines
            bullets = [line.strip() for line in lines if line.strip()]
        
        return bullets[:num_bullets]
    
    except Exception as e:
        print(f"AI bullet summarization error: {e}")
        # Fallback to extractive method
        return summarize_as_bullets(text, num_bullets)


# ==================== TEXT CORRECTION ENDPOINT ====================

def correct_extracted_text(request):
    """
    API endpoint to correct and optionally summarize extracted text
    POST parameters:
    - text: Text to correct (required)
    - summarize: Also generate summary (default False)
    - num_bullets: Number of bullet points if summarizing (default 5)
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '').strip()
            summarize = data.get('summarize', False)
            num_bullets = data.get('num_bullets', 5)
            
            if not text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Text cannot be empty'
                }, status=400)
            
            # Correct the text
            corrected = correct_text(text)
            
            result = {
                'status': 'ok',
                'original': text,
                'corrected': corrected,
                'changes_made': text != corrected
            }
            
            # Generate summary if requested
            if summarize:
                bullets = summarize_as_bullets(corrected, num_bullets)
                result['bullets'] = bullets
                result['summary_count'] = len(bullets)
            
            return JsonResponse(result)
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method is allowed'
    }, status=405)


# ==================== PDF EXTRACTION AND SUMMARIZATION ====================

def extract_pdf_text(pdf_bytes):
    """
    Extract text from PDF bytes using PyPDF2
    Returns: extracted text string
    """
    if PdfReader is None:
        return None
    
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_file)
        
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return None


def extract_text_from_bytes(data_bytes):
    """
    Fallback: Extract readable ASCII text from raw bytes
    Used when PDF library is not available
    """
    try:
        text_buffer = []
        for byte in data_bytes:
            # Extract printable ASCII and common symbols
            if (32 <= byte <= 126) or byte in [9, 10, 13]:
                text_buffer.append(chr(byte))
        
        text = ''.join(text_buffer)
        
        # Clean up common PDF artifacts
        text = re.sub(r'stream.*?endstream', ' ', text, flags=re.DOTALL)
        text = re.sub(r'<<.*?>>', ' ', text, flags=re.DOTALL)
        text = re.sub(r'/\w+\s+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    except Exception as e:
        print(f"Byte extraction error: {e}")
        return ""


def process_pdf_file(request):
    """
    API endpoint to process PDF file:
    1. Download PDF from URL/path
    2. Extract text from PDF
    3. Correct the text
    4. Generate summary with bullet points
    
    POST parameters (JSON):
    - file_url: Full URL or server path to PDF file (required)
      Example: http://192.168.29.230:8000/media/abstract_vzKUfpN.pdf
               or /media/abstract_vzKUfpN.pdf
    - num_bullets: Number of bullet points (default 5)
    - summarize: Generate summary (default True)
    - correct: Apply auto-correction (default True)
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            file_url = data.get('file_url', '').strip()
            
            if not file_url:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No file_url provided'
                }, status=400)
            
            # Get parameters
            num_bullets = data.get('num_bullets', 5)
            should_summarize = data.get('summarize', True)
            should_correct = data.get('correct', True)
            
            try:
                num_bullets = int(num_bullets)
            except (ValueError, TypeError):
                num_bullets = 5
            
            # Download PDF file
            print(f"Downloading PDF from: {file_url}")
            
            # If file_url is a relative path, make it absolute
            if file_url.startswith('/'):
                # Get the base URL from request
                base_url = request.build_absolute_uri('/').rstrip('/')
                file_url = base_url + file_url
            
            # Download the PDF
            response = http.get(file_url, timeout=30)
            
            if response.status_code != 200:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Failed to download PDF: {response.status_code}'
                }, status=400)
            
            pdf_bytes = response.content
            
            if not pdf_bytes or len(pdf_bytes) == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Downloaded file is empty'
                }, status=400)
            
            print(f"PDF downloaded, size: {len(pdf_bytes)} bytes")
            
            # Extract text from PDF
            extracted_text = extract_pdf_text(pdf_bytes)
            
            # Fallback to byte extraction if PyPDF2 fails
            if not extracted_text:
                print("PyPDF2 extraction failed, using fallback byte extraction")
                extracted_text = extract_text_from_bytes(pdf_bytes)
            
            if not extracted_text or len(extracted_text.strip()) == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Could not extract text from PDF. File may be image-based or corrupted.'
                }, status=400)
            
            # Correct text if requested
            corrected_text = extracted_text
            corrections_made = False
            if should_correct:
                corrected_text = correct_text(extracted_text)
                corrections_made = corrected_text != extracted_text
            
            result = {
                'status': 'ok',
                'extracted_text': extracted_text,
                'corrected_text': corrected_text,
                'corrections_made': corrections_made,
                'text_length': len(corrected_text.split()),
                'file_url': file_url,
            }
            
            # Generate summary if requested
            if should_summarize:
                bullets = summarize_as_bullets(corrected_text, num_bullets)
                result['bullets'] = bullets
                result['bullet_count'] = len(bullets)
                result['summary'] = True
            else:
                result['summary'] = False
            
            print(f"PDF processed successfully")
            print(f"Extracted {len(corrected_text.split())} words")
            
            return JsonResponse(result)
        
        except Exception as e:
            print(f"Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'status': 'error',
                'message': f'Error processing PDF: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method is allowed'
    }, status=405)
