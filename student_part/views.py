from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from parent_part.models import *
from parent_part.forms import *
from sub_part.models import *
from sub_part.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from sub_part.views import get_week_dates
from sub_part.decorators import *

def signup(request):
  return render(request,'Auth/SignUp.html')

@login_required
@user_type_required('Student')
def student_dashboard(request):
    record=Studentprofileupdate.objects.all().first()
    student=StudentAdmission.objects.get(id=request.student.id)
    records=Timeline.objects.all()
    reason=DisableReason.objects.all()
    form=TimelineForm()
    if request.method=='POST':
        form=TimelineForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/student_dashboard')
        else:
            print(form.errors)
    context={
        'form':form,'records':records,'student_dashboard':'active',
        'record':record,'student':student,'reason':reason
            }
    return render(request,'Student_part/student_dashboard.html',context)
@login_required
@user_type_required('Student')
def fees_parent(request):
    toady_date=datetime.now().date()
    records=StudentAdmission.objects.get(id=request.student.id)

    fees_records=FeesAssign.objects.filter(student_id=request.student.id)
    # fees_discount=FeesTypeDiscount.objects.all()
    fees_discount=DiscountAssign.objects.filter(student=request.student.id)
    paid_record=StudentFess.objects.filter(student=request.student.id)

    context={
        'records':records,'fees_records':fees_records,'toady_date':toady_date,'fees_discount':fees_discount,
        'paid_record':paid_record,'fees_parent':'active'
    }
    return render(request,'Student_part/fees_parent.html',context)

@login_required
@user_type_required('Student')
def hostel_room(request):
    records=StudentAdmission.objects.get(id=request.student.id)
    context={
       'hostel_room':'active','record':records
            }
    return render(request,'Student_part/hostel_room.html',context)

@login_required
@user_type_required('Student')
def transport_routes(request):
    records=AssignVehicle.objects.all()
    record=StudentAdmission.objects.get(id=request.student.id)
    context={
       'records':records,'transport_routes':'active','record':record
            }
    return render(request,'Student_part/transport_routes.html',context)

@login_required
@user_type_required('Student')
def books(request):
    recordss =AddBook.objects.all()
    record=LibrayMember.objects.filter(student=request.student.id).last()
    records=IssueBook.objects.filter(member=record)
    context={
        'records':records,'books':'active','record':record
            }
    return render(request,'Student_part/books.html',context)


@login_required
@user_type_required('Student')
def books_issued(request):
    record=LibrayMember.objects.filter(student=request.student.id).last()
    records=IssueBook.objects.filter(member=record)
    context={
        'books_issued':'active','records':records
            }
    return render(request,'Student_part/books_issued.html',context)

@login_required
@user_type_required('Student')
def teacher_reviews(request):
    student_obj=StudentAdmission.objects.get(id=request.student.id)
    rating=TeacherRating.objects.filter(student=student_obj)
    rating_staff=[data.staff.id for data in rating]
    assign_teacher=AssignClassTeacher.objects.filter(Class=student_obj.Class,section=student_obj.section).last()
    records=assign_teacher.class_teacher.all()
    if request.method=='POST':
        TeacherRating.objects.get_or_create(
            student=student_obj,
            Class=student_obj.Class,
            section=student_obj.section,
            assign_teacher=assign_teacher,
            staff_id=request.POST.get('teacher_id'),
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment'),
        )
        return redirect('teacher_reviews_student')
    context={
        'teacher_reviews':'active','records':records,'rating_staff':rating_staff,'rating':rating
    }
    return render(request,'Student_part/teacher_reviews.html',context)

@login_required
@user_type_required('Student')
def notice_board(request):
    record=noticeBoard.objects.all()
    context={
        'notice_board':'active','record':record
            }
    return render(request,'Student_part/notice_board.html',context)

@login_required
@user_type_required('Student')
def notice_board_view(request):
    records=noticeBoard.objects.all()
    context={
        'records':records,'notice_board_view':'active'
            }
    return render(request,'Student_part/notice_board_view.html',context)

@login_required
@user_type_required('Student')
def attendance(request):
    records=StudentAttendance.objects.all()
    record=StudentAttendance.objects.filter(student__first_name__icontains=1)
    context={
        'records':records,'attendance':'active','record':record
            }
    return render(request,'Student_part/attendance.html',context)

@login_required
@user_type_required('Student')
def apply_leave(request):
    class_records=Class.objects.all()
    section_records=Section.objects.all()
    records=Addleave.objects.filter(student=request.student.id)
    student=StudentAdmission.objects.get(id=request.student.id)
    form=AddleaveParentForm(initial={'Class':student.Class,'section':student.section,'student':student.id})
    if request.method=='POST':
        form=AddleaveParentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/parent/apply_leave_parent')
        else:
            print(form.errors)
    context={
        'form':form,'records':records,'apply_leave':'active','class_records':class_records,'section_records':section_records
            }
    return render(request,'Student_part/apply_leave.html',context)

@login_required
@user_type_required('Student')
def apply_leave_edit(request,pk):
    records=Addleave.objects.filter(student=request.student.id)
    record=Addleave.objects.get(id=pk)
    form=AddleaveParentForm(instance=record)
    if request.method=='POST':
        form=AddleaveParentForm(request.POST,instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/student/apply_leave')
    context={
        'form':form,'records':records,'apply_leave':'active'
            }
    return render(request,'Student_part/apply_leave_edit.html',context)

@login_required
@user_type_required('Student')
def apply_leave_delete(request,pk):
    Addleave.objects.get(id=pk).delete()
    return HttpResponseRedirect('/parent/apply_leave_parent')

@login_required
@user_type_required('Student')
def online_exam(request):
    context={
        'online_exam':'active'
    }
    return render(request,'Student_part/online_exam.html',context)

@login_required
@user_type_required('Student')
def homework(request):
    records=AssingHomeWork.objects.filter(student=request.student.id)
    if request.method=='POST':
        obj=records.get(id=request.POST.get('id'))
        obj.message=request.POST.get('message')
        obj.document=request.FILES.get('document')
        obj.save()
        return redirect('homework')
    context={
        'records':records,'homework':'active'
            }
    return render(request,'Student_part/homework.html',context)


@login_required
@user_type_required('Student')
def homework_view(request,pk):
    records=AddHomeWork.objects.all()
    record=AddHomeWork.objects.get(id=pk)
    # print('form',form)
    context={
        'record':record,'records':records,'homework':'active'
            }
    return render(request,'Student_part/homework_view.html',context)

# Download center

@login_required
@user_type_required('Student')
def assignment_list(request):
    student = StudentAdmission.objects.get(id=request.student.id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='assignments')
    records2=UploadContent.objects.filter(Class_id__isnull=True)
    records=records1 | records2
    context={
        'assignment_list':'active','records':records
    }
    return render(request,'Student_part/assignment_list.html',context)

@login_required
@user_type_required('Student')
def study_material(request):
    student = StudentAdmission.objects.get(id=request.student.id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='study_material')
    records2=UploadContent.objects.filter(Class_id__isnull=True)
    records=records1 | records2
    context={
         'study_material':'active','records':records,
    }
    return render(request,'Student_part/study_material.html',context)


@login_required
@user_type_required('Student')
def syllabus(request):
    student = StudentAdmission.objects.get(id=request.student.id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='syllabus')
    records2=UploadContent.objects.filter(Class_id__isnull=True)
    records=records1 | records2
    context={
         'syllabus':'active','records':records,
    }
    return render(request,'Student_part/syllabus.html',context)


@login_required
@user_type_required('Student')
def other_download_list(request):
    student = StudentAdmission.objects.get(id=request.student.id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='other_download')
    records2=UploadContent.objects.filter(Class_id__isnull=True)
    records=records1 | records2
    context={
         'other_download_list':'active','records':records,
    }
    return render(request,'Student_part/other_download_list.html',context)


@login_required
@user_type_required('Student')
def exam_schedule(request):
    records=ExamStudent.objects.filter(student=request.student.id)
    context={
        'records':records,'exam_schedule':'active'
            }
    return render(request,'Student_part/exam_schedule.html',context)

@login_required
@user_type_required('Student')
def exams_view(request,pk):
    records=AddExamSubject.objects.filter(exam=pk)

    context={
        'records':records,'exam_schedule':'active'
            }
    return render(request,'Student_part/exams_view.html',context)

@login_required
@user_type_required('Student')
def exam_result(request):
    records=ExamStudent.objects.filter(student=request.student.id)
    context={
        'records':records,'exam_result':'active'
            }
    return render(request,'Student_part/exam_result.html',context)


@login_required
@user_type_required('Student')
def exam_result_view(request,pk):
    records=EntryMarks.objects.filter(exam=pk)

    context={
        'records':records,'exam_result':'active'
            }
    return render(request,'Student_part/exam_result_view.html',context)


@login_required
@user_type_required('Student')
def class_timetable(request):
    student=StudentAdmission.objects.get(id=request.student.id)
    TimeTable_records=TimeTable.objects.filter(Class=student.Class,section=student.section,session=request.Session)

    context={
        'TimeTable_records':TimeTable_records,'class_timetable':'active'
            }
    return render(request,'Student_part/class_timetable.html',context)


@login_required
@user_type_required('Student')
def lesson_plan(request):
    student=StudentAdmission.objects.get(id=request.student.id)
    TimeTable_records=TimeTable.objects.filter(Class=student.Class,section=student.section,session=request.Session)
    if request.method=='POST':
        week=request.POST.get('week_days')
        week_split=week.split('-')
        year = int(week_split[0])
        week_number = int(week_split[1][1:])
        dates_in_week = get_week_dates(year, week_number)
        TimeTable_records=TimeTable.objects.filter(Class=student.Class,section=student.section,session=request.Session)
        week_days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        Monday=[]
        Tuesday=[]
        Wednesday=[]
        Thursday=[]
        Friday=[]
        Saturday=[]
        Sunday=[]
        week_no=0
        for days in week_days:

            time_table_record=TimeTable_records.filter(day = days)
            for data in time_table_record:
                lesson_plan=LessonPlan.objects.filter(time_table=data,date=dates_in_week[week_no].date()).last()
                if week_no == 0:
                    if lesson_plan:
                        Monday.append(['Edit',lesson_plan])
                elif week_no==1:
                    if lesson_plan:
                        Tuesday.append(['Edit',lesson_plan])
                elif week_no==2:
                    if lesson_plan:
                        Wednesday.append(['Edit',lesson_plan])
                elif week_no==3:
                    if lesson_plan:
                        Thursday.append(['Edit',lesson_plan])
                elif week_no==4:
                    if lesson_plan:
                        Friday.append(['Edit',lesson_plan])
                elif week_no==5:
                    if lesson_plan:
                        Saturday.append(['Edit',lesson_plan])
                elif week_no==6:
                    if lesson_plan:
                        Sunday.append(['Edit',lesson_plan])
            week_no+=1
        print(Monday,Tuesday)
        context={
            'lesson_plan_student':'active','Monday':Monday,'Tuesday':Tuesday,'Wednesday':Wednesday,'Thursday':Thursday,'Friday':Friday,'Saturday':Saturday,'Sunday':Sunday,
            'dates_in_week':dates_in_week,'week':week
                }
        return render(request,'Student_part/lesson_plan.html',context)
    context={
        'lesson_plan_student':'active'
            }
    return render(request,'Student_part/lesson_plan.html',context)


@login_required
@user_type_required('Student')
def syllabus_status(request):
    student=StudentAdmission.objects.get(id=request.student.id)
    classs=student.Class
    section=student.section
    subject=SubjectGroup.objects.filter(Class=student.Class,section=student.section).last()
    records=[]
    chart_percent=[]
    for sub in subject.subject.all():
        subj={}
        lesson_records=Lesson.objects.filter(Class_id=classs,section_id=section,subject=sub.id)
        record=[]
        total=0
        percent=1
        for data in lesson_records:
            dict={}
            topic_records=topic.objects.filter(lesson_name=data.id)
            if topic_records.count() > 0 :
                percentage=int(topic_records.filter(status="complete").count() * 100 / topic_records.count())
                percent*=percentage/100
                total+=1
                dict['percentage']=f'{percentage}% Complete'
            else:
                dict['percentage']='No Status'
            dict['lesson']=data
            dict['topic']=topic_records
            record.append(dict)
        if total > 0:
            chart_percent.append([percent*100,sub.subject_name])
            subj['percentage']=f'{percent*100}% Complete'
        else:
            chart_percent.append([0,sub.subject_name])
            subj['percentage']='0% Complete'
        subj['subject']=sub
        subj['record']=record
        records.append(subj)
    context={
        'syllabus_status_student':'active','records':records,'chart_percent':chart_percent
    }
    return render(request, 'Student_part/syllabus_status.html', context)


@login_required
@user_type_required('Student')
def online_class(request):
    records = OnlineClass.objects.all()

    if request.method == 'POST':
        form = OnlineClassForm(request.POST)
        if form.is_valid():
            form.save()
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return redirect('/online_class')  # Redirect to a view showing the list of all online classes
    else:
        form = OnlineClassForm()

    context = {
        'records': records,
        'form': form,
        'online_class':'active'
    }

    return render(request, 'Student_part/online_class.html', context)

@login_required
@user_type_required('Student')
def online_class_feedback(request,pk):
        records=Studentmeetingnote.objects.all()
        form=StudentmeetingnoteForm ()
        record=OnlineClass.objects.get(id=pk)
        if request.method=='POST':
            form=StudentmeetingnoteForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/student/online_class')

        context={
            'form':form,'records':records,'online_class':'active','record':record,
                }
        return render(request,'Student_part/online_class_feedback.html',context)

@login_required
@user_type_required('Student')
def student_meeting_view(request,pk):
        records=Studentmeetingnote.objects.all()
        form=StudentmeetingnoteForm ()
        record=OnlineClass.objects.get(id=pk)


        context={
            'form':form,'records':records,'staff_meeting':'active','record':record,
                }
        return render(request,'Student_part/student_meeting_view.html',context)


@login_required
@user_type_required('Student')
def chat_index(request):
    staff_records=AddStaff.objects.all()
    student_records=StudentAdmission.objects.all()
    contact_record = AddContact.objects.filter(user=request.user)
    records=[]
    for data in contact_record:
        dict={}
        count=ContanctMessage.objects.filter(status='sended',contact=data).count()
        dict['obj']=data
        dict['unread_count']=count
        records.append(dict)

    context={
        'staff_records':staff_records,'student_records':student_records,'contact_record':contact_record,'records':records
            }
    return render(request,'Chat/chat_index_student.html',context)

@login_required
@user_type_required('Student')
def save_contact(request):
    usertype= request.POST.get('usertype')
    user_id= request.POST.get('user_id')
    if usertype == 'Staff':
        staff_obj=AddStaff.objects.get(id=user_id)
        AddContact.objects.get_or_create(
            user=request.user,
            staff_id=user_id,
            contact_user=staff_obj.user,
            usertype=usertype
        )
        AddContact.objects.get_or_create(
            user=staff_obj.user,
            staff_id=user_id,
            contact_user=request.user,
            usertype='Student'
        )
    else:
        if usertype == 'Student':
            user_obj = StudentAdmission.objects.get(id=user_id)
            user_obj_id=user_obj.user_student
        elif usertype == 'Parent':
            user_obj = StudentAdmission.objects.get(id=user_id)
            user_obj_id=user_obj.user_parent
        print('===',user_obj_id)
        AddContact.objects.get_or_create(
            user=request.user,
            student_id=user_id,
            contact_user=user_obj_id,
            usertype=usertype
        )
        AddContact.objects.get_or_create(
            user=user_obj_id,
            student_id=user_id,
            contact_user=request.user,
            usertype='Student'
        )
    return redirect('chat_index')

@login_required
@user_type_required('Student')
def chat(request,pk):
    staff_records=AddStaff.objects.all()
    student_records=StudentAdmission.objects.all()
    contact_record = AddContact.objects.filter(user=request.user)
    contact_obj= AddContact.objects.get(id=pk)
    message_records= ContanctMessage.objects.filter(contact=contact_obj)
    message_records.filter(status='sended').update(status='readed')
    records=[]
    for data in contact_record:
        dict={}
        count=ContanctMessage.objects.filter(status='sended',contact=data).count()
        dict['obj']=data
        dict['unread_count']=count
        records.append(dict)
    context={
        'staff_records':staff_records,'student_records':student_records,'contact_record':contact_record,
        'contact_obj':contact_obj,'pk':int(pk),'message_records':message_records,'records':records
            }
    return render(request,'Chat/chat_student.html',context)

@login_required
@user_type_required('Student')
def student_profile_update(request):
    records=StudentAdmission.objects.all()
    record=Studentprofileupdate.objects.all().first()
    if record:
        if record and record.fieldshide:
            student_fields_hide=record.fieldshide
        else:
            student_fields_hide=[]
    if records:
        record=StudentAdmission.objects.get(id=request.student.id)
        form=StudentsHideFieldForm(instance=record)
        if request.method=='POST':
            first_name=request.POST.get('first_name')
            if first_name:
                record.first_name=first_name
            last_name=request.POST.get('last_name')
            if last_name:
                record.last_name=last_name
            date_of_birth=request.POST.get('date_of_birth')
            if date_of_birth:
                record.date_of_birth=date_of_birth
            gender=request.POST.get('gender')
            if gender:
                record.gender_id=gender
            religion=request.POST.get('religion')
            if religion:
                record.religion=religion
            Caste=request.POST.get('Caste')
            if Caste:
                record.Caste=Caste
            religion=request.POST.get('religion')
            if religion:
                record.religion=religion
            mobile_number=request.POST.get('mobile_number')
            if mobile_number:
                record.mobile_number=mobile_number
            email=request.POST.get('email')
            if email:
                record.email=email
            religion=request.POST.get('religion')
            if religion:
                record.religion=religion
            admission_date=request.POST.get('admission_date')
            if admission_date:
                record.admission_date=admission_date
            student_photo=request.POST.get('student_photo')
            if student_photo:
                record.student_photo=student_photo
            Blood_group=request.POST.get('Blood_group')
            if Blood_group:
                record.Blood_group=Blood_group
            height=request.POST.get('height')
            if height:
                record.height=height
            student_house=request.POST.get('student_house')
            if student_house:
                record.student_house_id=student_house
            weight=request.POST.get('weight')
            if weight:
                record.weight=weight
            category=request.POST.get('category')
            if category:
                record.category_id=category
            Father_name=request.POST.get('Father_name')
            if Father_name:
                record.Father_name=Father_name
            Father_phone=request.POST.get('Father_phone')
            if Father_phone:
                record.Father_phone=Father_phone
            Father_occupation=request.POST.get('Father_occupation')
            if Father_occupation:
                record.Father_occupation=Father_occupation
            Father_photo=request.POST.get('Father_photo')
            if Father_photo:
                record.Father_photo=Father_photo
            mother_name=request.POST.get('mother_name')
            if mother_name:
                record.mother_name=mother_name
            mother_photo=request.POST.get('mother_photo')
            if mother_photo:
                record.mother_photo=mother_photo
            mother_occupation=request.POST.get('mother_occupation')
            if mother_occupation:
                record.mother_occupation=mother_occupation
            if_guardian_is=request.POST.get('if_guardian_is')
            if if_guardian_is:
                record.if_guardian_is_id=if_guardian_is
            guardian_name=request.POST.get('guardian_name')
            if guardian_name:
                record.guardian_name=guardian_name
            guardian_relation=request.POST.get('guardian_relation')
            if guardian_relation:
                record.guardian_relation=guardian_relation
            guardian_email=request.POST.get('guardian_email')
            if guardian_email:
                record.guardian_email=guardian_email
            guardian_phone=request.POST.get('guardian_phone')
            if guardian_phone:
                record.guardian_phone=guardian_phone
            guardian_occupation=request.POST.get('guardian_occupation')
            if guardian_occupation:
                record.guardian_occupation=guardian_occupation
            guardian_photo=request.POST.get('guardian_photo')
            if guardian_photo:
                record.guardian_photo=guardian_photo
            guardian_address=request.POST.get('guardian_address')
            if guardian_address:
                record.guardian_address=guardian_address
            religion=request.POST.get('religion')
            if religion:
                record.religion=religion
            current_address=request.POST.get('current_address')
            if current_address:
                record.current_address=current_address
            permanent_address=request.POST.get('permanent_address')
            if permanent_address:
                record.permanent_address=permanent_address
            bank_account_number=request.POST.get('bank_account_number')
            if bank_account_number:
                record.bank_account_number=bank_account_number
            bank_name=request.POST.get('bank_name')
            if bank_name:
                record.bank_name=bank_name
            ifsc_code=request.POST.get('ifsc_code')
            if ifsc_code:
                record.ifsc_code=ifsc_code
            national_identification_number=request.POST.get('national_identification_number')
            if national_identification_number:
                record.national_identification_number=national_identification_number
            local_identification_number=request.POST.get('local_identification_number')
            if local_identification_number:
                record.local_identification_number=local_identification_number
            rte=request.POST.get('rte')
            if rte:
                record.rte_id=rte
            previous_school_detail=request.POST.get('previous_school_detail')
            if previous_school_detail:
                record.previous_school_detail=previous_school_detail
            record.save()
            form=StudentsHideFieldForm(request.POST,request.FILES,instance=record)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/student/student_profile_update')
            else:
                print(form.errors)

    context={
             'records':records,'form':form,'student_fields_hide':student_fields_hide,'record':record
            }
    return render(request,'Student_part/student_profile_update.html',context)


