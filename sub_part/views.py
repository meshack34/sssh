from django.http import HttpResponse, HttpResponseRedirect
import json, random, string
from django.shortcuts import render, redirect, get_object_or_404
from sub_part.models import *
from sub_part.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .password import generate_password
from .emails import new_staff_account_email
from django.db.models import Count, Sum
from .emails import new_staff_account_email, send_email_notification
from datetime import datetime, timedelta, date, time
from django.template.defaultfilters import floatformat
import pandas as pd
from payment.models import PaymentKeys
from .sms import *
from .decorators import *
import calendar
from django.utils import timezone
from num2words import num2words
from .accounts import *


def signup(request):
    if request.method == "GET":
        form = SignUpForm()
        context = {
            "form": form,
        }
        return render(request, "Auth/SignUp.html", context)
    elif request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect("signin")
        else:
            context = {
                "form": form,
            }
            return render(request, "Auth/SignUp.html", context)


def signin(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            form = AuthenticationForm()
            context = {
                "form": form,
            }
            return render(request, "Auth/SignIn.html", context)
        else:
            return redirect("dashboard")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            un = form.cleaned_data["username"]
            pwd = form.cleaned_data["password"]
            user = authenticate(username=un, password=pwd)
            if user is not None:
                login(request, user)
                if request.user.user_type == "Student":
                    return redirect("student_dashboard_student")
                elif request.user.user_type == "Parent":
                    return redirect("parent_dashboard")
                else:
                    return redirect("dashboard")
            else:
                print("invalid username and password")
                context = {
                    "form": form,
                    "error": "Invalid Username And Password",
                }
                return render(request, "Auth/SignIn.html", context)
        else:
            print(form.errors)
            context = {
                "form": form,
            }
            return render(request, "Auth/SignIn.html", context)


def signout(request):
    if request.user.is_authenticated:
        logout(request)
        print("Im log out")
        return redirect("signin")
    else:
        return redirect("signin")


# @login_required
# @user_type_required("Staff")
def dashboard(request):
    print("session", request.Session)
    if request.user.is_authenticated:
        current_month = datetime.now().month
        current_year = datetime.now().year
        year_1 = StudentAdmission.objects.filter(admission_date__year=current_year)
        year_2 = StudentAdmission.objects.filter(admission_date__year=current_year - 1)
        year_3 = StudentAdmission.objects.filter(admission_date__year=current_year - 2)
        year_4 = StudentAdmission.objects.filter(admission_date__year=current_year - 3)
        year_5 = StudentAdmission.objects.filter(admission_date__year=current_year - 4)
        year_6 = StudentAdmission.objects.filter(admission_date__year=current_year - 5)
        month_jun = StudentAdmission.objects.filter(
            admission_date__month=1, admission_date__year=current_year
        )
        month_Fab = StudentAdmission.objects.filter(
            admission_date__month=2, admission_date__year=current_year
        )
        month_Mar = StudentAdmission.objects.filter(
            admission_date__month=3, admission_date__year=current_year
        )
        month_Apr = StudentAdmission.objects.filter(
            admission_date__month=4, admission_date__year=current_year
        )
        month_MAY = StudentAdmission.objects.filter(
            admission_date__month=5, admission_date__year=current_year
        )
        month_June = StudentAdmission.objects.filter(
            admission_date__month=6, admission_date__year=current_year
        )
        month_July = StudentAdmission.objects.filter(
            admission_date__month=7, admission_date__year=current_year
        )
        month_Aug = StudentAdmission.objects.filter(
            admission_date__month=8, admission_date__year=current_year
        )
        month_Sep = StudentAdmission.objects.filter(
            admission_date__month=9, admission_date__year=current_year
        )
        month_oct = StudentAdmission.objects.filter(
            admission_date__month=10, admission_date__year=current_year
        )
        month_Nov = StudentAdmission.objects.filter(
            admission_date__month=11, admission_date__year=current_year
        )
        month_Dec = StudentAdmission.objects.filter(
            admission_date__month=12, admission_date__year=current_year
        )
        total_complaints = Complain.objects.count()
        total_students = StudentAdmission.objects.count()
        total_teacher = AddStaff.objects.count()
        current_date = date.today()
        current_datetime = datetime.now()
        current_session = request.Session
        students_fees = (
            StudentFess.objects.filter(
                session=current_session, created_at__month=current_month
            ).aggregate(Sum("paid_amount"))["paid_amount__sum"]
            or 0
        )
        students_expenaces = (
            AddExpense.objects.filter(date__year=current_year).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        library_return = IssueBook.objects.filter(status="Returned").count()
        library_complete = IssueBook.objects.filter(status="complete").count()
        library_book = AddBook.objects.count()
        fees_unpaid = FeesAssign.objects.filter(status="pending").count()
        fees_paid = FeesAssign.objects.filter(status="paid").count()
        fees_pertial = FeesAssign.objects.filter(status="partially paid").count()
        staff_present_today = StaffAttendance.objects.filter(
            attendance_date=current_date, status="present"
        ).count()
        student_present_total = StudentAttendance.objects.filter(
            attendance_date=current_date, attendance_status="present"
        ).count()
        student_half_total = StudentAttendance.objects.filter(
            attendance_status="half"
        ).count()
        student_absent_total = StudentAttendance.objects.filter(
            attendance_status="Absent"
        ).count()
        student_late_total = StudentAttendance.objects.filter(
            attendance_status="Late"
        ).count()
        student_present_today = StudentAttendance.objects.filter(
            attendance_status="present"
        ).count()
        upcoming_events = AlumniEvent.objects.filter(
            event_date_from__year=current_year
        ).count()
        current_students = StudentAdmission.objects.filter(
            session=current_session
        ).count()
        total_paid_amount = (
            StudentFess.objects.filter(session=current_session).aggregate(
                Sum("paid_amount")
            )["paid_amount__sum"]
            or 0
        )
        # total_expense_spent = AddExpense.objects.aggregate(total_expense_spent=models.Sum('amount'))['total_expense_spent'] or 0
        total_expense_spent = (
            AddExpense.objects.aggregate(total_expense_spent=models.Sum("amount"))[
                "total_expense_spent"
            ]
            or 0
        )
        income_total_earned = (
            AddIncome.objects.aggregate(income_total_earned=models.Sum("amount"))[
                "income_total_earned"
            ]
            or 0
        )
       
        income_total, expense_total, net_result = calculate_net_gains_losses()
      
                
        # Calculate the total net result 
        # total_net_result = income_total_earned - total_expense_spent + total_paid_amount
        # Calculate the total net result as an integer (remove decimal points)
        total_net_result = int(income_total_earned - total_expense_spent + total_paid_amount)


        roles = Role.objects.all()
        role_counts = []
        records = EventCalendar.objects.all()
        record = Calendarnofication.objects.all()

        for role in roles:
            count = AddStaff.objects.filter(roles=role).count()
            role_counts.append((role, count))

        context = {
            "dashboard": "active",
            'income_total': income_total,
            'expense_total': expense_total,
            'net_result': net_result,
            'income_total_earned':income_total_earned,
            'total_net_result': total_net_result,
            "total_complaints": total_complaints,
            "total_students": total_students,
            "total_teacher": total_teacher,
            "staff_present_today": staff_present_today,
            "student_present_today": student_present_today,
            "upcoming_events_count": upcoming_events,
            "total_paid_amount": total_paid_amount,
            "total_expense_spent": total_expense_spent,
            "role_counts": role_counts,
            "records": records,
            "record": record,
            "students_fees": students_fees,
            "students_expenaces": students_expenaces,
            "student_late_total": student_late_total,
            "student_absent_total": student_absent_total,
            "student_present_total": student_present_total,
            "student_half_total": student_half_total,
            "fees_unpaid": fees_unpaid,
            "fees_paid": fees_paid,
            "fees_pertial": fees_pertial,
            "library_return": library_return,
            "library_complete": library_complete,
            "library_book": library_book,
            "current_students": current_students,
            "month_jun": month_jun.count(),
            "month_Fab": month_Fab.count(),
            "month_Mar": month_Mar.count(),
            "month_Apr": month_Apr.count(),
            "month_MAY": month_MAY.count(),
            "month_June": month_June.count(),
            "month_July": month_July.count(),
            "month_Aug": month_Aug.count(),
            "month_Sep": month_Sep.count(),
            "month_oct": month_oct.count(),
            "month_Nov": month_Nov.count(),
            "month_Dec": month_Dec.count(),
            "year_6": year_6.count(),
            "year_5": year_5.count(),
            "year_4": year_4.count(),
            "year_3": year_3.count(),
            "year_2": year_2.count(),
            "year_1": year_1.count(),
        }

        return render(request, "dashboard.html", context)
    else:
        return redirect("signin")


@login_required
@user_type_required("Staff")
def admission_enquiry(request):
    if (
        request.user.is_superuser
        or "admission_enquiry_view" in request.permissions
        or "admission_enquiry_add" in request.permissions
    ):
        try:
            records = AdmissionEnquiry.objects.all()
            form = AdmissionEnquiryForm()
            if request.method == "POST":
                form = AdmissionEnquiryForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/admission_enquiry")
            context = {"form": form, "records": records, "admission_enquiry": "active"}
            return render(request, "Front_Office/admission_enquiry.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def admission_enquiry_edit(request, pk):
    if request.user.is_superuser or "admission_enquiry_edit" in request.permissions:
        try:
            records = AdmissionEnquiry.objects.all()
            record = AdmissionEnquiry.objects.get(id=pk)
            form = AdmissionEnquiryForm(instance=record)
            if request.method == "POST":
                form = AdmissionEnquiryForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/admission_enquiry")
            context = {"form": form, "records": records, "admission_enquiry": "active"}

            return render(request, "Front_Office/admission_enquiry_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def admission_enquiry_view(request, pk):
    if request.user.is_superuser or "admission_enquiry_view" in request.permissions:
        try:
            records = AdmissionEnquiry.objects.all()
            record = AdmissionEnquiry.objects.get(id=pk)
            form = AdmissionEnquiryForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "admission_enquiry": "active",
                "view": True,
            }
            return render(request, "Front_Office/admission_enquiry_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def admission_enquiry_delete(request, pk):
    AdmissionEnquiry.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/admission_enquiry")


@login_required
@user_type_required("Staff")
def phone_call_log(request):
    if (
        request.user.is_superuser
        or "phone_call_log_view" in request.permissions
        or "phone_call_log_add" in request.permissions
    ):
        try:
            records = PhoneCallLog.objects.all()
            form = PhoneCallLogForm()
            if request.method == "POST":
                print("3")
                form = PhoneCallLogForm(request.POST)
                if form.is_valid():
                    print("4")
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/phone_call_log")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "phone_call_log": "active"}
            return render(request, "Front_Office/phone_call_log.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def phone_call_log_edit(request, pk):
    if request.user.is_superuser or "phone_call_log_edit" in request.permissions:
        try:
            records = PhoneCallLog.objects.all()
            record = PhoneCallLog.objects.get(id=pk)
            form = PhoneCallLogForm(instance=record)
            if request.method == "POST":
                form = PhoneCallLogForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/phone_call_log")
            context = {
                "form": form,
                "records": records,
                "phone_call_log": "active",
                "edit": True,
            }
            return render(request, "Front_Office/phone_call_log.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def phone_call_log_view(request, pk):
    if request.user.is_superuser or "phone_call_log_view" in request.permissions:
        try:
            records = PhoneCallLog.objects.all()
            record = PhoneCallLog.objects.get(id=pk)
            form = PhoneCallLogForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "phone_call_log": "active",
                "view": True,
            }
            return render(request, "Front_Office/phone_call_log.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def phone_call_log_delete(request, pk):
    if request.user.is_superuser or "phone_call_log_delete" in request.permissions:
        try:
            PhoneCallLog.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/phone_call_log")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def postal_dispatch(request):
    if (
        request.user.is_superuser
        or "postal_dispatch_view" in request.permissions
        or "postal_dispatch_add" in request.permissions
    ):
        try:
            records = PostalDispatch.objects.all()
            form = PostalDispatchForm()
            if request.method == "POST":
                form = PostalDispatchForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/postal_dispatch")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "postal_dispatch": "active",
            }
            return render(request, "Front_Office/postal_dispatch.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def postal_dispatch_edit(request, pk):
    if request.user.is_superuser or "postal_dispatch_edit" in request.permissions:
        try:
            records = PostalDispatch.objects.all()
            record = PostalDispatch.objects.get(id=pk)
            form = PostalDispatchForm(instance=record)
            if request.method == "POST":
                form = PostalDispatchForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/postal_dispatch")
            context = {
                "form": form,
                "records": records,
                "postal_dispatch": "active",
                "edit": True,
            }
            return render(request, "Front_Office/postal_dispatch.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def postal_dispatch_view(request, pk):
    if request.user.is_superuser or "postal_dispatch_view" in request.permissions:
        try:
            records = PostalDispatch.objects.all()
            record = PostalDispatch.objects.get(id=pk)
            form = PostalDispatchForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "postal_dispatch": "active",
                "view": True,
            }
            return render(request, "Front_Office/postal_dispatch.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def postal_dispatch_delete(request, pk):
    if request.user.is_superuser or "postal_dispatch_delete" in request.permissions:
        try:
            PostalDispatch.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/postal_dispatch")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def postal_receive(request):
    if (
        request.user.is_superuser
        or "postal_receive_view" in request.permissions
        or "postal_receive_add" in request.permissions
    ):
        try:
            records = PostalReceive.objects.all()
            form = PostalReceiveForm()
            if request.method == "POST":
                print("3")
                form = PostalReceiveForm(request.POST)
                if form.is_valid():
                    print("4")
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/postal_receive")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "postal_receive": "active"}
            return render(request, "Front_Office/postal_receive.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def postal_receive_edit(request, pk):
    if request.user.is_superuser or "postal_receive_edit" in request.permissions:
        try:
            records = PostalReceive.objects.all()
            record = PostalReceive.objects.get(id=pk)
            form = PostalReceiveForm(instance=record)
            if request.method == "POST":
                form = PostalReceiveForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/postal_receive")
            context = {
                "form": form,
                "records": records,
                "postal_receive": "active",
                "edit": True,
            }
            return render(request, "Front_Office/postal_receive.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def postal_receive_view(request, pk):
    if request.user.is_superuser or "postal_receive_view" in request.permissions:
        try:
            records = PostalReceive.objects.all()
            record = PostalReceive.objects.get(id=pk)
            form = PostalReceiveForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "postal_receive": "active",
                "view": True,
            }
            return render(request, "Front_Office/postal_receive.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def postal_receive_delete(request, pk):
    if request.user.is_superuser or "postal_receive_delete" in request.permissions:
        try:
            PostalReceive.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/postal_receive")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def complain(request):
    if (
        request.user.is_superuser
        or "complain_view" in request.permissions
        or "complain_add" in request.permissions
    ):
        try:
            records = Complain.objects.all()
            form = ComplainForm()
            if request.method == "POST":
                form = ComplainForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/complain")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "complain": "active",
            }
            return render(request, "Front_Office/complain.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def complain_edit(request, pk):
    if request.user.is_superuser or "complain_edit" in request.permissions:
        try:
            records = Complain.objects.all()
            record = Complain.objects.get(id=pk)
            form = ComplainForm(instance=record)
            if request.method == "POST":
                form = ComplainForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/complain")
            context = {
                "form": form,
                "records": records,
                "complain": "active",
                "edit": True,
            }
            return render(request, "Front_Office/complain.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def complain_view(request, pk):
    if request.user.is_superuser or "complain_view" in request.permissions:
        try:
            records = Complain.objects.all()
            record = Complain.objects.get(id=pk)
            form = ComplainForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "complain": "active",
                "view": True,
            }
            return render(request, "Front_Office/complain.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def complain_delete(request, pk):
    if request.user.is_superuser or "complain_delete" in request.permissions:
        try:
            Complain.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/complain")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def setup_front_office_purpose(request):
    if (
        request.user.is_superuser
        or "setup_front_office_view" in request.permissions
        or "setup_front_office_add" in request.permissions
    ):
        try:
            records = Purpose.objects.all()
            form = PurposeForm()
            if request.method == "POST":
                form = PurposeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/setup_front_office_purpose")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "setup_front_office_purpose": "active",
            }
            return render(
                request, "Front_Office/setup_front_office_purpose.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def setup_front_office_purpose_edit(request, pk):
    if request.user.is_superuser or "setup_front_office_edit" in request.permissions:
        try:
            records = Purpose.objects.all()
            record = Purpose.objects.get(id=pk)
            form = PurposeForm(instance=record)
            if request.method == "POST":
                form = PurposeForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/setup_front_office_purpose")
            context = {
                "form": form,
                "records": records,
                "setup_front_office_purpose": "active",
                "edit": True,
            }
            return render(
                request, "Front_Office/setup_front_office_purpose.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def setup_front_office_purpose_delete(request, pk):
    if request.user.is_superuser or "setup_front_office_delete" in request.permissions:
        try:
            Purpose.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/setup_front_office_purpose")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def setup_front_office_complain_type(request):
    if (
        request.user.is_superuser
        or "setup_front_office_view" in request.permissions
        or "setup_front_office_add" in request.permissions
    ):
        try:
            records = ComplainType.objects.all()
            form = ComplainTypeForm()
            if request.method == "POST":
                form = ComplainTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/setup_front_office_complain_type")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "setup_front_office_purpose": "active",
                "view": True,
            }
            return render(
                request, "Front_Office/setup_front_office_complain_type.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def setup_front_office_complain_type_edit(request, pk):
    if request.user.is_superuser or "setup_front_office_edit" in request.permissions:
        try:
            records = ComplainType.objects.all()
            record = ComplainType.objects.get(id=pk)
            form = ComplainTypeForm(instance=record)
            if request.method == "POST":
                form = ComplainTypeForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/setup_front_office_complain_type")
            context = {
                "form": form,
                "records": records,
                "setup_front_office_purpose": "active",
            }
            return render(
                request,
                "Front_Office/setup_front_office_complain_type_edit.html",
                context,
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def setup_front_office_complain_type_delete(request, pk):
    ComplainType.objects.get(id=pk).delete()
    return HttpResponseRedirect("/setup_front_office_complain_type")


@login_required
@user_type_required("Staff")
def setup_front_office_source(request):
    if (
        request.user.is_superuser
        or "setup_front_office_view" in request.permissions
        or "setup_front_office_add" in request.permissions
    ):
        try:
            records = Source.objects.all()
            form = SourceForm()
            if request.method == "POST":
                form = SourceForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/setup_front_office_source")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "setup_front_office_purpose": "active",
                "view": True,
            }
            return render(
                request, "Front_Office/setup_front_office_source.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def setup_front_office_source_edit(request, pk):
    records = Source.objects.all()
    record = Source.objects.get(id=pk)
    form = SourceForm(instance=record)
    if request.method == "POST":
        form = SourceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/setup_front_office_source")
    context = {"form": form, "records": records, "setup_front_office_purpose": "active"}
    return render(request, "Front_Office/setup_front_office_source_edit.html", context)


@login_required
@user_type_required("Staff")
def setup_front_office_source_delete(request, pk):
    Source.objects.get(id=pk).delete()
    return HttpResponseRedirect("/setup_front_office_source")


def setup_front_office_reference(request):
    records = Reference.objects.all()
    form = ReferenceForm()
    if request.method == "POST":
        form = ReferenceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/setup_front_office_reference")
        else:
            print(form.errors)
    context = {
        "form": form,
        "records": records,
        "setup_front_office_purpose": "active",
        "view": True,
    }
    return render(request, "Front_Office/setup_front_office_reference.html", context)


@login_required
@user_type_required("Staff")
def setup_front_office_reference_edit(request, pk):
    records = Reference.objects.all()
    record = Reference.objects.get(id=pk)
    form = ReferenceForm(instance=record)
    if request.method == "POST":
        form = ReferenceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/setup_front_office_reference")
    context = {"form": form, "records": records, "setup_front_office_purpose": "active"}
    return render(
        request, "Front_Office/setup_front_office_reference_edit.html", context
    )


@login_required
@user_type_required("Staff")
def setup_front_office_reference_delete(request, pk):
    Reference.objects.get(id=pk).delete()
    return HttpResponseRedirect("/setup_front_office_reference")


@login_required
@user_type_required("Staff")
def student_details(request):
    if request.user.is_superuser or "student_information_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                if classs and section:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, section_id=section, session=request.Session
                    )
                elif classs:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, session=request.Session
                    )
                elif section:
                    records = StudentAdmission.objects.filter(
                        section_id=section, session=request.Session
                    )
                print(records)
                context = {
                    "student_details": "active",
                    "records": records,
                    "class_records": class_records,
                }
                return render(
                    request, "Student_information/student_details.html", context
                )
            context = {
                "student_details": "active",
                "class_records": class_records,
            }
            return render(request, "Student_information/student_details.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Assuming you have a Session model in sub_part.models
from sub_part.models import Session


@login_required
@user_type_required("Staff")
def student_admission(request):
    if request.user.is_superuser or "student_information_add" in request.permissions:
        try:
            system_fields = SystemFields.objects.all()
            system_field = (
                system_fields.last().student_fields if system_fields.last() else None
            )
            custom_fields = CustomFields.objects.filter(field_belongs_to="Student")
            records = StudentAdmission.objects.all()
            # student_account = None
            # Create the corresponding Account for the student using the function from accounts.py
            student_account = create_student_account(obj)
            form = StudentAdmissionForm()

            if request.method == "POST":
                form = StudentAdmissionForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)

                    password_student = generate_password()
                    password_parent = generate_password()

                    last_name = form.cleaned_data["last_name"] or ""

                    # Create a user account for the student
                    username_student = f"student{records.count()}"
                    user_student = User.objects.create_user(
                        username=username_student,
                        first_name=form.cleaned_data["first_name"],
                        last_name=last_name,
                        email=form.cleaned_data["email"],
                        password=password_student,
                        user_type="Student",
                    )
                    user_student.save()

                    # Create a user account for the parent
                    username_parent = f"parent{records.count()}"
                    user_parent = User.objects.create_user(
                        username=username_parent,
                        first_name=form.cleaned_data["guardian_name"],
                        email=form.cleaned_data["guardian_email"],
                        password=password_parent,
                        user_type="Parent",
                    )
                    user_parent.save()

                    # Send an email to the student
                    recipient_name_student = obj.first_name
                    recipient_email_student = form.cleaned_data["email"]
                    new_staff_account_email(
                        recipient_name_student,
                        recipient_email_student,
                        password_student,
                    )

                    # Send an email to the parent
                    recipient_name_parent = obj.guardian_name
                    recipient_email_parent = form.cleaned_data["guardian_email"]
                    new_staff_account_email(
                        recipient_name_parent, recipient_email_parent, password_parent
                    )

                    # Create StudentAdmission instance
                    obj.session = request.Session
                    obj.user_student_id = user_student.pk
                    obj.user_parent_id = user_parent.pk
                    obj.account = student_account
                    obj.created_by = request.user
                    obj.save()

                    # Check if the session exists, create if not
                    session_instance, created = Session.objects.get_or_create(
                        session=request.Session
                    )

                    LoginCredentials.objects.create(
                        student_id=obj.pk,
                        student_username=username_student,
                        student_password=password_student,
                        parent_username=username_parent,
                        parent_passwod=password_parent,
                    )

                    StudentSession.objects.create(
                        session=session_instance,
                        student_id=obj.pk,
                        status="Active",
                    )

                    StudentClass.objects.create(
                        session=session_instance,
                        student_id=obj.pk,
                        Class_id=request.POST.get("Class"),
                        section_id=request.POST.get("section"),
                        status="Active",
                    )

                    # customs fields
                    for data in custom_fields:
                        if data.field_type == "multiselect":
                            value = request.POST.getlist(f"{data.field_name}")
                        else:
                            value = request.POST.get(f"{data.field_name}")
                        if value:
                            StudentCustomFieldValues.objects.create(
                                field=data, student_id=obj.pk, value=value
                            )

                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/student_admission")

                else:
                    print(form.errors)

            context = {
                "form": form,
                "records": records,
                "student_admission": "active",
                "student_account": student_account,
                "view": True,
                "custom_fields": custom_fields,
                "system_fields": system_field,
            }
            return render(
                request, "Student_information/student_admission.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def online_admission(request):
    context = {"online_admission": "active"}
    return render(request, "Student_information/online_admission.html", context)


@login_required
@user_type_required("Staff")
def disabled_students(request):
    if request.user.is_superuser or "disble_student_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                print(classs, section)
                if classs and section:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs,
                        section_id=section,
                        status="Disable",
                        session=request.Session,
                    )
                elif classs:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, status="Disable", session=request.Session
                    )
                elif section:
                    records = StudentAdmission.objects.filter(
                        section_id=section, status="Disable", session=request.Session
                    )
                context = {
                    "disabled_students": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                }
                return render(
                    request, "Student_information/disabled_students.html", context
                )
            context = {
                "disabled_students": "active",
                "class_records": class_records,
                "section_records": section_records,
            }
            return render(
                request, "Student_information/disabled_students.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def multi_class_student(request):
    context = {"multi_class_student": "active"}
    return render(request, "Student_information/multi_class_student.html", context)


@login_required
@user_type_required("Staff")
def bulk_delete(request):
    if request.user.is_superuser or "student_information_delete" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            if request.POST.get("search") == "search":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                print(classs, section)
                if classs and section:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, section_id=section, session=request.Session
                    )
                elif classs:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, session=request.Session
                    )
                elif section:
                    records = StudentAdmission.objects.filter(
                        section_id=section, session=request.Session
                    )
                context = {
                    "bulk_delete": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                }
                return render(request, "Student_information/bulk_delete.html", context)
            if request.POST.get("delete") == "delete":
                check_list = request.POST.getlist("check")
                StudentAdmission.objects.filter(id__in=check_list).delete()

            context = {
                "bulk_delete": "active",
                "class_records": class_records,
                "section_records": section_records,
            }
            return render(request, "Student_information/bulk_delete.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_category(request):
    if (
        request.user.is_superuser
        or "student_categories_view" in request.permissions
        or "student_categories_add" in request.permissions
    ):
        try:
            records = StudentCategory.objects.all()
            form = StudentCategoryForm()
            if request.method == "POST":
                form = StudentCategoryForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/student_category")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "student_category": "active"}
            return render(request, "Student_information/student_category.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_category_edit(request, pk):
    if request.user.is_superuser or "student_categories_edit" in request.permissions:
        try:
            records = StudentCategory.objects.all()
            record = StudentCategory.objects.get(id=pk)
            form = StudentCategoryForm(instance=record)
            if request.method == "POST":
                form = StudentCategoryForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/student_category")
            context = {
                "form": form,
                "records": records,
                "student_category": "active",
                "edit": True,
            }
            return render(request, "Student_information/student_category.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_category_view(request, pk):
    if request.user.is_superuser or "student_categories_edit" in request.permissions:
        try:
            records = StudentCategory.objects.all()
            record = StudentCategory.objects.get(id=pk)
            form = StudentCategoryForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "student_category": "active",
                "view": True,
            }
            return render(request, "Student_information/student_category.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


def student_category_delete(request, pk):
    if request.user.is_superuser or "student_categories_edit" in request.permissions:
        try:
            StudentCategory.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/student_category")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_house(request):
    if (
        request.user.is_superuser
        or "student_house_view" in request.permissions
        or "student_house_add" in request.permissions
    ):
        try:
            records = StudentHouse.objects.all()
            form = StudentHouseForm()
            if request.method == "POST":
                form = StudentHouseForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/student_house")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "student_house": "active",
            }
            return render(request, "Student_information/student_house.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_house_edit(request, pk):
    if request.user.is_superuser or "student_house_edit" in request.permissions:
        try:
            records = StudentHouse.objects.all()
            record = StudentHouse.objects.get(id=pk)
            form = StudentHouseForm(instance=record)
            if request.method == "POST":
                form = StudentHouseForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/student_house")
            context = {
                "form": form,
                "records": records,
                "student_house": "active",
                "edit": True,
            }
            return render(request, "Student_information/student_house.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_house_view(request, pk):
    if (
        request.user.is_superuser
        or "student_house_view" in request.permissions
        or request.permissions
    ):
        try:
            records = StudentHouse.objects.all()
            record = StudentHouse.objects.get(id=pk)
            form = StudentHouseForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "student_house": "active",
                "view": True,
            }
            return render(request, "Student_information/student_house.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_house_delete(request, pk):
    if (
        request.user.is_superuser
        or "student_house_delete" in request.permissions
        or request.permissions
    ):
        try:
            StudentHouse.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/student_house")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def disabled_reason(request):
    if (
        request.user.is_superuser
        or "disable_student_view" in request.permissions
        or "disable_student_add" in request.permissions
    ):
        try:
            records = DisableReason.objects.all()
            form = DisableReasonForm()
            if request.method == "POST":
                form = DisableReasonForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/disabled_reason")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "disabled_reason": "active",
            }
            return render(request, "Student_information/disabled_reason.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def disabled_reason_edit(request, pk):
    if (
        request.user.is_superuser
        or "disable_student_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = DisableReason.objects.all()
            record = DisableReason.objects.get(id=pk)
            form = DisableReasonForm(instance=record)
            if request.method == "POST":
                form = StudentHouseForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/disabled_reason")
            context = {
                "form": form,
                "records": records,
                "disabled_reason": "active",
                "edit": True,
            }
            return render(request, "Student_information/disabled_reason.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def disabled_reason_view(request, pk):
    if (
        request.user.is_superuser
        or "disable_student_view" in request.permissions
        or request.permissions
    ):
        try:
            records = DisableReason.objects.all()
            record = DisableReason.objects.get(id=pk)
            form = DisableReasonForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "disabled_reason": "active",
                "view": True,
            }
            return render(request, "Student_information/disabled_reason.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def disabled_reason_delete(request, pk):
    if (
        request.user.is_superuser
        or "disable_student_delete" in request.permissions
        or request.permissions
    ):
        try:
            DisableReason.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/disabled_reason")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


## Income
@login_required
@user_type_required("Staff")
def add_income(request):
    if (
        request.user.is_superuser
        or "income_view" in request.permissions
        or "income_add" in request.permissions
    ):
        try:
            records = AddIncome.objects.all()
            form = AddIncomeForm()
            # Get user_id from the current user
            user_id = request.user.id

            # Assuming User model has a ForeignKey to School
            user_school = request.user.school

            # Get the school account associated with the user's school
            school_account = user_school.account
            if request.method == "POST":
                form = AddIncomeForm(request.POST)
                if form.is_valid():
                    income_instance = form.save()

                    # Call collect_income function
                    success = collect_income(income_instance, user_id)

                    if success:
                        messages.success(request, "Record Saved Successfully")
                    else:
                        messages.error(request, "Failed to process the income")
                    return HttpResponseRedirect("/add_income")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "add_income": "active"}
            return render(request, "Income/add_income.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Expense
# Expense
@login_required
@user_type_required("Staff")
def add_expense(request):
    if (
        request.user.is_superuser
        or "expense_view" in request.permissions
        or "expense_add" in request.permissions
        or request.permissions
    ):
        try:
            records = AddExpense.objects.all()
            form = AddExpenseForm()

            # Get user_id from the current user
            user_id = request.user.id

            # Assuming User model has a ForeignKey to School
            user_school = request.user.school

            # Get the school account associated with the user's school
            school_account = user_school.account

            if request.method == "POST":
                form = AddExpenseForm(request.POST, request.FILES)
                if form.is_valid():
                    expense_instance = form.save()

                    # Call collect_expense function with user_id
                    success = collect_expense(expense_instance, user_id)

                    if success:
                        messages.success(request, "Record Saved Successfully")
                    else:
                        messages.error(request, "Failed to process the expense")
                    return HttpResponseRedirect("/add_expense")
                else:
                    print(form.errors)

            context = {"form": form, "records": records, "add_expense": "active"}
            return render(request, "Expenses/add_expense.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_income_edit(request, pk):
    if (
        request.user.is_superuser
        or "income_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = AddIncome.objects.all()
            record = AddIncome.objects.get(id=pk)
            form = AddIncomeForm(instance=record)
            if request.method == "POST":
                form = StudentHouseForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_income")
            context = {
                "form": form,
                "records": records,
                "add_income": "active",
                "edit": True,
            }
            return render(request, "Income/add_income.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_income_view(request, pk):
    if (
        request.user.is_superuser
        or "income_view" in request.permissions
        or request.permissions
    ):
        try:
            records = AddIncome.objects.all()
            record = AddIncome.objects.get(id=pk)
            form = AddIncomeForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "add_income": "active",
                "view": True,
            }
            return render(request, "Income/add_income.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_income_delete(request, pk):
    if (
        request.user.is_superuser
        or "income_delete" in request.permissions
        or request.permissions
    ):
        try:
            AddIncome.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_income")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def edit_income(request):
    form = AddIncomeForm()
    context = {
        "form": form,
    }
    return render(request, "Income/edit_income.html", context)


@login_required
@user_type_required("Staff")
def search_income(request):
    if (
        request.user.is_superuser
        or "search_income_view" in request.permissions
        or request.permissions
    ):
        try:
            if request.method == "POST":
                from_date = request.POST.get("from_date")
                to_date = request.POST.get("to_date")

                filters = {}
                if from_date and to_date:
                    filters["date__range"] = [from_date, to_date]
                elif from_date:
                    filters["date__gte"] = from_date
                elif to_date:
                    filters["date__lte"] = to_date

                records = AddIncome.objects.filter(**filters)
                context = {
                    "search_income": "active",
                    "records": records,
                }
                return render(request, "Income/search_income.html", context)
            context = {
                "search_income": "active",
            }
            return render(request, "Income/search_income.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def income_head(request):
    if (
        request.user.is_superuser
        or "income_head_view" in request.permissions
        or "income_head_add" in request.permissions
        or request.permissions
    ):
        try:
            records = Incomehead.objects.all()
            form = IncomeheadForm()
            if request.method == "POST":
                form = IncomeheadForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/income_head")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "income_head": "active"}
            return render(request, "Income/income_head.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def income_head_edit(request, pk):
    if (
        request.user.is_superuser
        or "income_head_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = Incomehead.objects.all()
            record = Incomehead.objects.get(id=pk)
            form = IncomeheadForm(instance=record)
            if request.method == "POST":
                form = IncomeheadForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/income_head")
            context = {
                "form": form,
                "records": records,
                "income_head": "active",
                "edit": True,
            }
            return render(request, "Income/income_head.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def income_head_view(request, pk):
    if (
        request.user.is_superuser
        or "income_head_view" in request.permissions
        or request.permissions
    ):
        try:
            records = Incomehead.objects.all()
            record = Incomehead.objects.get(id=pk)
            form = IncomeheadForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "income_head": "active",
                "view": True,
            }
            return render(request, "Income/income_head.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def income_head_delete(request, pk):
    if (
        request.user.is_superuser
        or "income_head_delete" in request.permissions
        or request.permissions
    ):
        try:
            Incomehead.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/income_head")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def edit_income_head(request):
    form = AddIncomeForm()
    context = {
        "form": form,
    }
    return render(request, "Income/edit_income_head.html", context)


# accounts
# Gl LIne
@login_required
@user_type_required("Staff")
def add_gline(request):
    try:
        # Permission checks
        if (
            request.user.is_superuser
            or "add_gline" in request.permissions
            or request.permissions
        ):
            glines = GLLine.objects.all()
            form = GLLineForm()

            if request.method == "POST":
                form = GLLineForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/add_gline")

            context = {"form": form, "glines": glines}
            return render(request, "Accounts/add_gline.html", context)
        else:
            return render(request, "error.html")
    except Exception as error:
        return render(request, "error.html", {"error": error})
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the dashboard for unauthenticated users


@login_required
@user_type_required("Staff")
def view_gline(request):
    try:
        # Permission checks
        if (
            request.user.is_superuser
            or "view_gline" in request.permissions
            or request.permissions
        ):
            glines = GLLine.objects.all()
            context = {"glines": glines}
            return render(request, "Accounts/view_gline.html", context)
    except Exception as error:
        return render(request, "error.html", {"error": error})
    else:
        return render(
            request,
            "error.html",
            {"message": "You don't have permission to access this page."},
        )
    return redirect("dashboard")  # Redirect to the dashboard for unauthenticated users


@login_required
@user_type_required("Staff")
def add_gline_view(request, pk):
    if (
        request.user.is_superuser
        or "income_head_view" in request.permissions
        or request.permissions
    ):
        try:
            records = GLLine.objects.all()
            record = GLLine.objects.get(line_number=pk)
            form = GLLineForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "income_head": "active",
                "view": True,
            }
            return render(request, "Accounts/add_gline.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_gline_edit(request, pk):
    if (
        request.user.is_superuser
        or "add_gline_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = GLLine.objects.all()
            record = GLLine.objects.get(id=pk)
            form = GLLineForm(instance=record)
            if request.method == "POST":
                form = GLLineForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/income_head")
            context = {
                "form": form,
                "records": records,
                "income_head": "active",
                "edit": True,
            }
            return render(request, "Accounts/add_gline.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
def all_gline(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_gline"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            context = {"add_account_type": "active"}
            return render(request, "Accounts/all_gline.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
@user_type_required("Staff")
def add_gline_delete(request, pk):
    if (
        request.user.is_superuser
        or "add_gline_delete" in request.permissions
        or request.permissions
    ):
        try:
            GLLine.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_gline")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Assert Type
@login_required
def add_asset_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_asset_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = AssetTypeForm()
            if request.method == "POST":
                form = AssetTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_asset_type")
            else:
                form = AssetTypeForm()

            return render(request, "Accounts/add_asset_type.html", {"form": form})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
@user_type_required("Staff")
def add_asset_type(request):
    try:
        # Permission checks
        if (
            request.user.is_superuser
            or "add_asset_type" in request.permissions
            or request.permissions
        ):
            glines = AssetType.objects.all()
            form = AssetTypeForm()

            if request.method == "POST":
                form = AssetTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/add_asset_type")

            context = {"form": form, "glines": glines}
            return render(request, "Accounts/add_asset_type.html", context)
        else:
            return render(request, "error.html")
    except Exception as error:
        return render(request, "error.html", {"error": error})
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the dashboard for unauthenticated users


@login_required
def view_asset_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_asset_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            assets = AssetType.objects.all()
            return render(request, "view_asset_type.html", {"assets": assets})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_asset_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_asset_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            context = {"add_account_type": "active"}
            return render(request, "all_asset_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


# Account Type
@login_required
def add_account_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_account_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = AccountTypeForm()
            if request.method == "POST":
                form = AccountTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_account_type")
            else:
                form = AccountTypeForm()
            context = {"form": form, "add_account_type": "active"}
            return render(request, "add_account_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_account_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_account_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            accounts = AccountType.objects.all()
            return render(request, "view_account_type.html", {"accounts": accounts})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_account_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_account_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "all_account_type.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
@user_type_required("Staff")
def account_type(request):
    if (
        request.user.is_superuser
        or "income_head_view" in request.permissions
        or "account_type" in request.permissions
        or request.permissions
    ):
        try:
            records = AccountType.objects.all()
            form = AccountTypeForm()
            if request.method == "POST":
                form = AccountTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/account_type")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "charge_typecharge_type": "active",
            }
            return render(request, "Accounts/account_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def account_type_edit(request, pk):
    if (
        request.user.is_superuser
        or "charge_type_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = AccountType.objects.all()
            record = AccountType.objects.get(id=pk)
            form = AccountTypeForm(instance=record)
            if request.method == "POST":
                form = AccountTypeForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/account_type")
            context = {
                "form": form,
                "records": records,
                "charge_type": "active",
                "edit": True,
            }
            return render(request, "Accounts/account_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def account_type_view(request, pk):
    if (
        request.user.is_superuser
        or "charge_type_view" in request.permissions
        or request.permissions
    ):
        try:
            records = AccountType.objects.all()
            record = AccountType.objects.get(id=pk)
            form = AccountTypeForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "charge_type": "active",
                "view": True,
            }
            return render(request, "Accounts/account_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def account_type_delete(request, pk):
    if (
        request.user.is_superuser
        or "charge_type_delete" in request.permissions
        or request.permissions
    ):
        try:
            ChargeType.objects.get(charge_type=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/account_type")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Add Account
@login_required
@user_type_required("Staff")
def add_account(request):
    if (
        request.user.is_superuser
        or "income_view" in request.permissions
        or "add_account" in request.permissions
    ):
        try:
            records = Account.objects.all()
            form = AccountForm()
            if request.method == "POST":
                form = AccountForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/add_account")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "add_account": "active"}
            return render(request, "Accounts/add_account.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def view_account_edit(request, pk):
    if (
        request.user.is_superuser
        or "view_account_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = Account.objects.all()
            record = Account.objects.get(id=pk)
            form = AccountForm(instance=record)
            if request.method == "POST":
                form = StudentHouseForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_income")
            context = {
                "form": form,
                "records": records,
                "add_income": "active",
                "edit": True,
            }
            return render(request, "Income/add_income.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def view_account_view(request, pk):
    if (
        request.user.is_superuser
        or "income_view" in request.permissions
        or request.permissions
    ):
        try:
            records = Account.objects.all()
            record = Account.objects.get(id=pk)
            form = AccountForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "add_income": "active",
                "view": True,
            }
            return render(request, "Income/add_income.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def view_account_delete(request, pk):
    if (
        request.user.is_superuser
        or "income_delete" in request.permissions
        or request.permissions
    ):
        try:
            Account.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_income")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Transaction
@login_required
def add_transaction(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_transaction"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = AccountForm()
            if request.method == "POST":
                form = AccountForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_account_type")
            else:
                form = AccountForm()
            context = {"form": form, "add_account": "active"}
            return render(request, "add_transaction.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_transaction(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_transaction"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            accounts = TransactionType.objects.all()
            context = {"accounts": accounts}
            return render(request, "view_transaction.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_transaction(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_transaction"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "all_transaction.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


# Transaction Code
@login_required
def add_transaction_code(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_transaction_code"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = TransactionCodeForm()
            if request.method == "POST":
                form = TransactionCodeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_transaction_code")
            else:
                form = TransactionCodeForm()
            context = {"form": form, "add_transaction_code": "active"}
            return render(request, "add_transaction_code.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_transaction_code(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_transaction_code"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            codes = ChargeType.objects.all()
            context = {"codes": codes}
            return render(request, "view_transcation_code.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


# Charge Type
@login_required
def add_charge_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_charge_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = ChargeTypeForm()
            if request.method == "POST":
                form = ChargeTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_charge_type")
            else:
                form = ChargeTypeForm()
            context = {"form": form, "add_charge_type": "active"}
            return render(request, "add_charge_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_charge_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_charge_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            types = TransactionCode.objects.all()
            context = {"types": types}
            return render(request, "view_charge_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
@user_type_required("Staff")
def charge_type(request):
    if (
        request.user.is_superuser
        or "income_head_view" in request.permissions
        or "charge_type" in request.permissions
        or request.permissions
    ):
        try:
            records = ChargeType.objects.all()
            form = ChargeTypeForm()
            if request.method == "POST":
                form = ChargeTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/charge_type")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "charge_typecharge_type": "active",
            }
            return render(request, "Accounts/charge_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def charge_type_edit(request, pk):
    if (
        request.user.is_superuser
        or "charge_type_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = ChargeType.objects.all()
            record = ChargeType.objects.get(charge_type=pk)
            form = ChargeTypeForm(instance=record)
            if request.method == "POST":
                form = ChargeTypeForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/charge_type")
            context = {
                "form": form,
                "records": records,
                "charge_type": "active",
                "edit": True,
            }
            return render(request, "Accounts/charge_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def charge_type_view(request, pk):
    if (
        request.user.is_superuser
        or "charge_type_view" in request.permissions
        or request.permissions
    ):
        try:
            records = ChargeType.objects.all()
            record = ChargeType.objects.get(charge_type=pk)
            form = ChargeTypeForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "charge_type": "active",
                "view": True,
            }
            return render(request, "Accounts/charge_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def charge_type_delete(request, pk):
    if (
        request.user.is_superuser
        or "charge_type_delete" in request.permissions
        or request.permissions
    ):
        try:
            ChargeType.objects.get(charge_type=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/income_head")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Transaction Type
@login_required
def add_transaction_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_transaction_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = TransactionTypeForm()
            if request.method == "POST":
                form = TransactionTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_transaction_type")
            else:
                form = TransactionTypeForm()
            context = {"form": form, "add_transaction_type": "active"}
            return render(request, "add_transaction_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_transaction_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_transaction_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            types = TransactionType.objects.all()
            context = {"types": types}
            return render(request, "view_transaction_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


# Account Entry
# def account_entry(member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id):
#     try:
#         entry_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
#         print("Account Entry Statement ...")
#         print(member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id)

#         # Debit account process
#         dr_acc_detail = Account.objects.get(account_number=dr_acc)
#         AccountEntry.objects.create(
#             entry_ID=entry_id,
#             transaction_ID=transaction_id,
#             user_id=member_id,
#             account_number_id=dr_acc,
#             group_name_id=group_id,
#             amount=-pay_amount,
#             currency="KES",
#             debit_credit_marker="Debit",
#         )
#         dr_acc_detail.current_cleared_balance -= float(pay_amount)
#         dr_acc_detail.total_balance -= float(pay_amount)
#         dr_acc_detail.save()
#         print("Credit process.")

#         # Credit account process
#         entry_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
#         cr_acc_detail = Account.objects.get(account_number=cr_acc)
#         AccountEntry.objects.create(
#             entry_ID=entry_id,
#             transaction_ID=transaction_id,
#             user_id=member_id,
#             account_number_id=cr_acc,
#             group_name_id=group_id,
#             amount=pay_amount,
#             currency="KES",
#             debit_credit_marker="Credit",
#         )
#         print("here...")
#         cr_acc_detail.current_cleared_balance += float(pay_amount)
#         cr_acc_detail.total_balance += float(pay_amount)
#         cr_acc_detail.save()
#         print("llllll")
#         return True
#     except Exception as error:
#         print("error ", error)
#         return False

# from django.db import transaction


def account_entry(member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id):
    try:
        entry_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        print("Account Entry Statement ...")
        print(member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id)

        # Debit Account Process
        dr_acc_detail = Account.objects.get(account_number=dr_acc)
        AccountEntry.objects.create(
            entry_ID=entry_id,
            transaction_ID=transaction_id,
            user_id=member_id,
            account_number_id=dr_acc,
            group_name_id=group_id,
            amount=-pay_amount,
            currency="KES",
            debit_credit_marker="Debit",
        )
        dr_acc_detail.current_cleared_balance -= float(pay_amount)
        dr_acc_detail.total_balance -= float(pay_amount)
        dr_acc_detail.save()

        # Credit Account Process
        entry_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        cr_acc_detail = Account.objects.get(account_number=str(cr_acc))
        AccountEntry.objects.create(
            entry_ID=entry_id,
            transaction_ID=transaction_id,
            user_id=member_id,
            account_number_id=cr_acc,
            group_name_id=group_id,
            amount=pay_amount,
            currency="KES",
            debit_credit_marker="Credit",
        )
        cr_acc_detail.current_cleared_balance += float(pay_amount)
        cr_acc_detail.total_balance += float(pay_amount)
        cr_acc_detail.save()
        result = account_entry(
            member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id
        )

        return True
    except Exception as error:
        print("Error: ", error)
        return False


# import logging
# import random
# import string
# from main.models import Account, AccountEntry

# logger = logging.getLogger(__name__)

# def process_debit_entry(entry_id, transaction_id, member_id, dr_acc, group_id, pay_amount):
#     try:
#         dr_acc_detail = Account.objects.get(account_number=dr_acc)

#         # Debit entry logic
#         AccountEntry.objects.create(
#             entry_ID=entry_id,
#             transaction_ID=transaction_id,
#             user_id=member_id,
#             account_number_id=dr_acc,
#             group_name_id=group_id,
#             amount=-pay_amount,
#             currency='KES',
#             debit_credit_marker='Debit',
#         )

#         dr_acc_detail.current_cleared_balance -= float(pay_amount)
#         dr_acc_detail.total_balance -= float(pay_amount)
#         dr_acc_detail.save()

#         return True
#     except Account.DoesNotExist as account_not_found:
#         logger.error(f"Error: {account_not_found}")
#         return False
#     except Exception as error:
#         logger.error(f"Unexpected error in debit entry: {error}")
#         return False

# def process_credit_entry(entry_id, transaction_id, member_id, cr_acc, group_id, pay_amount):
#     try:
#         cr_acc_detail = Account.objects.get(account_number=cr_acc)

#         # Credit entry logic
#         AccountEntry.objects.create(
#             entry_ID=entry_id,
#             transaction_ID=transaction_id,
#             user_id=member_id,
#             account_number_id=cr_acc,
#             group_name_id=group_id,
#             amount=pay_amount,
#             currency='KES',
#             debit_credit_marker='Credit',
#         )

#         cr_acc_detail.current_cleared_balance += float(pay_amount)
#         cr_acc_detail.total_balance += float(pay_amount)
#         cr_acc_detail.save()

#         return True
#     except Account.DoesNotExist as account_not_found:
#         logger.error(f"Error: {account_not_found}")
#         return False
#     except Exception as error:
#         logger.error(f"Unexpected error in credit entry: {error}")
#         return False

# def account_entry(member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id):
#     try:
#         entry_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
#         process_debit_entry(entry_id, transaction_id, member_id, dr_acc, group_id, pay_amount)
#         process_credit_entry(entry_id, transaction_id, member_id, cr_acc, group_id, pay_amount)
#         return True
#     except Exception as error:
#         logger.error(f"Error in account entry: {error}")
#         return False


@login_required
def account_entry_view(request):
    if request.user.is_authenticated:
        check_function_name = (
            "account_entry_view"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                # Retrieve data from the form
                member_id = request.POST.get("member_id")
                group_id = request.POST.get("group_id")
                pay_amount = float(request.POST.get("pay_amount"))
                dr_acc = request.POST.get("dr_acc")
                cr_acc = request.POST.get("cr_acc")
                transaction_id = request.POST.get("transaction_id")

                # Call the account_entry function
                success = utils.account_entry(
                    member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id
                )

                if success:
                    return render(request, "account_success_template.html")
                else:
                    return render(request, "error_template.html")

            return render(request, "account_entry_form.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "dashboard"
        )  # Redirect to the login page for unauthenticated users


@login_required
@user_type_required("Staff")
def account_entry_edit(request, pk):
    if (
        request.user.is_superuser
        or "view_account_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = AccountEntry.objects.all()
            record = AccountEntry.objects.get(id=pk)
            form = AccountEntryForm(instance=record)
            if request.method == "POST":
                form = StudentHouseForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_income")
            context = {
                "form": form,
                "records": records,
                "add_income": "active",
                "edit": True,
            }
            return render(request, "Income/add_income.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def account_entry_delete(request, pk):
    if (
        request.user.is_superuser
        or "income_delete" in request.permissions
        or request.permissions
    ):
        try:
            AccountEntry.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_income")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Fees Collection
@login_required
@user_type_required("Staff")
def collect_fees(request):
    print(f"is superuser {request.user.is_superuser}")
    if request.user.is_superuser:
        # or "collect_fees_add" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                print(classs, section)
                if classs and section:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, section_id=section, session=request.Session
                    )
                elif classs:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, session=request.Session
                    )
                elif section:
                    records = StudentAdmission.objects.filter(
                        section_id=section, session=request.Session
                    )
                context = {
                    "collect_fees": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                }
                return render(request, "Fees_Collection/collect_fees.html", context)
            context = {
                "collect_fees": "active",
                "class_records": class_records,
                "section_records": section_records,
            }

            return render(request, "Fees_Collection/collect_fees.html", context)
        except Exception as error:
            print(f"error {error}")
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def class_students(request):
    print(f"is superuser {request.user.is_superuser}")
    if request.user.is_superuser:
        # or "collect_fees_add" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                print(classs, section)
                if classs and section:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, section_id=section, session=request.Session
                    )
                elif classs:
                    records = StudentAdmission.objects.filter(
                        Class_id=classs, session=request.Session
                    )
                elif section:
                    records = StudentAdmission.objects.filter(
                        section_id=section, session=request.Session
                    )
                context = {
                    "collect_fees": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                }
                return render(request, "Fees_Collection/class_students.html", context)
            context = {
                "collect_fees": "active",
                "class_records": class_records,
                "section_records": section_records,
            }

            return render(request, "Fees_Collection/class_students.html", context)
        except Exception as error:
            print(f"error {error}")
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# @login_required
# @user_type_required("Staff")
# def collect_fees(request):
#     print(f"is superuser {request.user.is_superuser}")
#     if request.user.is_superuser:
#         try:
#             class_records = Class.objects.all()
#             section_records = Section.objects.all()

#             if request.method == "POST":
#                 class_id = request.POST.get("class")
#                 section_id = request.POST.get("section")

#                 if class_id and section_id:
#                     records = StudentAdmission.objects.filter(
#                         Class_id=class_id, section_id=section_id, session=request.Session
#                     )
#                 elif class_id:
#                     records = StudentAdmission.objects.filter(
#                         Class_id=class_id, session=request.Session
#                     )
#                 elif section_id:
#                     records = StudentAdmission.objects.filter(
#                         section_id=section_id, session=request.Session
#                     )

#                 # Assuming each student pays a fixed fee (for simplicity)
#                 fee_amount = 100  # You can replace this with the actual fee amount

#                 # Simulate a scenario where a student pays fees
#                 for student in records:
#                     # Create student account
#                     if student.school is not None:
#                         student_account = create_student_account(student)

#                         # Ensure student has a valid school attribute
#                         if student.school is not None:
#                             # Create school account if not exists
#                             school_account = create_school_account(student.school)

#                     # student_account = create_student_account(student)

#                     # Create school account if not exists
#                     # school_account = create_school_account(student.school)

#                     # Simulate a transaction entry for fee payment
#                             success = account_entry(
#                                 member_id=student.id,
#                                 group_id=student.school.id,
#                                 pay_amount=fee_amount,
#                                 dr_acc=school_account,
#                                 cr_acc=student_account,
#                                 transaction_id=f"FEES_{student.id}",
#                             )

#                         if success:
#                             print(f"Fee collected for student {student.id}")

#                 context = {
#                     "collect_fees": "active",
#                     "records": records,
#                     "class_records": class_records,
#                     "section_records": section_records,
#                 }

#                 return render(request, "Fees_Collection/collect_fees.html", context)

#             context = {
#                 "collect_fees": "active",
#                 "class_records": class_records,
#                 "section_records": section_records,
#                 "records": records,
#             }

#             return render(request, "Fees_Collection/collect_fees.html", context)

#         except Exception as error:
#             print(f"error {error}")
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")


@login_required
@user_type_required("Staff")
def collect_fees_detail(request, pk):
    if request.user.is_superuser or "collect_fees_add" in request.permissions:
        try:
            toady_date = datetime.now().date()
            records = StudentAdmission.objects.get(id=pk)
            fees_records = FeesAssign.objects.filter(
                student_id=pk, session=request.Session
            )
            # fees_discount=FeesTypeDiscount.objects.all()
            fees_discount = DiscountAssign.objects.filter(
                student=pk, session=request.Session
            )
            paid_record = StudentFess.objects.filter(
                student=pk, session=request.Session
            )

            if request.method == "POST":
                amount = request.POST.get("amount")
                percentage = request.POST.get("percentage")
                discount_group = request.POST.get("discount_group")
                amount_discount = request.POST.get("amount_discount")
                amount_fine = request.POST.get("amount_fine")
                payment_mode_fee = request.POST.get("payment_mode_fee")
                description = request.POST.get("description")
                fess_id = request.POST.get("fees_idd")
                fees_record = FeesAssign.objects.get(id=fess_id)
                if discount_group:
                    dis = DiscountAssign.objects.filter(
                        id=discount_group,
                    ).last()
                    if dis:
                        dis.status = "applied"
                        dis.fees_id = fess_id
                        dis.save()
                        fees_record.Dicount_amount = (
                            fees_record.Dicount_amount + dis.discount.amount
                        )
                if amount_fine:
                    fees_record.fine_amount = int(amount_fine) + fees_record.fine_amount
                StudentFess.objects.create(
                    student_id=pk,
                    paid_amount=amount,
                    discount_group_id=discount_group,
                    payment_mode_fee=payment_mode_fee,
                    amount_discount=amount_discount,
                    amount_fine=amount_fine,
                    description=description,
                    status="Paid",
                    fess_id=fess_id,
                    session=request.Session,
                    created_by=request.user,
                )

                fees_record.paid_amount = int(fees_record.paid_amount) + int(amount)
                if fees_record.balance_amount == None:
                    balance = (
                        int(fees_record.fees.amount)
                        - int(amount)
                        - int(amount_discount)
                    )
                    paid = fees_record.paid_amount
                else:
                    balance = (
                        int(fees_record.balance_amount)
                        - int(amount)
                        - int(amount_discount)
                    )
                    paid = int(fees_record.paid_amount) + int(amount)
                fees_record.balance_amount = balance
                # fees_record.paid_amount=paid
                if balance == 0:
                    fees_record.status = "fully paid"
                else:
                    fees_record.status = "partially paid"
                fees_record.save()

                # for student in records:
                if records.school is not None:
                    # Retrieve the user-inputted amount from the form
                    # fee_amount = request.POST.get(f"fee_amount_{records.id}")
                    print("amount", amount)
                    fee_amount = amount
                    # Ensure fee_amount is not None and is a valid number
                    if fee_amount is not None and fee_amount.isdigit():
                        fee_amount = int(fee_amount)
                    else:
                        print(f"Invalid fee amount for student {records.id}")
                        # Handle the error or return an appropriate response

                    # Collect fees from student and credit it to the school
                    # success = collect_school_fees(request,records, fee_amount)
                    # Assuming you have the student and fee_amount variables defined earlier in your code
                    success = collect_school_fees(
                        records_id=records.id,
                        fee_amount=fee_amount,
                        user_id=request.user.id,
                    )

                    if success:
                        print(f"Fee collected for student {records.id}")
                    else:
                        print(f"Failed to collect fee for student {records.id}")

                return HttpResponseRedirect(f"/collect_fees_detail/{pk}")

            context = {
                "records": records,
                "fees_records": fees_records,
                "toady_date": toady_date,
                "fees_discount": fees_discount,
                "paid_record": paid_record,
                "collect_fees": "active",
            }
            return render(request, "Fees_Collection/collect_fees_detail.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# cumulative total


from django.db.models import Sum

# ...


@login_required
@user_type_required("Staff")
def collect_fees_total(request, pk):
    if request.user.is_superuser or "collect_fees_add" in request.permissions:
        try:
            today_date = datetime.now().date()
            records = StudentAdmission.objects.get(id=pk)
            fees_records = FeesAssign.objects.filter(
                student_id=pk, session=request.Session
            )
            fees_discount = DiscountAssign.objects.filter(
                student=pk, session=request.Session
            )

            # Use the PaymentRecord model to get total paid_amount for all students
            total_paid_amount_all_students = PaymentRecord.objects.filter(
                session=request.Session
            ).aggregate(Sum("paid_amount"))["paid_amount__sum"]

            print(total_paid_amount_all_students)

            if request.method == "POST":
                context = {
                    "records": records,
                    "fees_records": fees_records,
                    "today_date": today_date,
                    "fees_discount": fees_discount,
                    "collect_fees": "active",
                    "total_paid_amount_all_students": total_paid_amount_all_students,
                }

            return render(request, "Fees_Collection/collect_fees_detail.html", context)

        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def search_fee_payment(request):
    if request.user.is_superuser or "search_fees_payment_view" in request.permissions:
        try:
            if request.method == "POST":
                records = StudentFess.objects.filter(
                    id=request.POST.get("payment_id"), session=request.Session
                ).last()
                context = {"search_fee_payment": "active", "records": records}
                return render(
                    request, "Fees_Collection/search_fee_payment.html", context
                )
            context = {"search_fee_payment": "active"}
            return render(request, "Fees_Collection/search_fee_payment.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def search_due_fee(request):
    if request.user.is_superuser or "search_due_fees_view" in request.permissions:
        try:
            fees_type = FeesType.objects.all()
            Classs = Class.objects.all()
            if request.method == "POST":
                records = FeesAssign.objects.filter(
                    fees__fees_type=request.POST.get("fees_type"),
                    session=request.Session,
                    student__Class=request.POST.get("class"),
                    student__section=request.POST.get("section"),
                    student__session=request.Session,
                ).exclude(status="fully paid")
                print("xxxxxxxxxxxxxxxxxx", records)

                context = {
                    "search_due_fee": "active",
                    "fees_type": fees_type,
                    "Classs": Classs,
                    "records": records,
                }
                return render(request, "Fees_Collection/search_due_fee.html", context)
            context = {
                "search_due_fee": "active",
                "fees_type": fees_type,
                "Classs": Classs,
            }
            return render(request, "Fees_Collection/search_due_fee.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_master(request):
    if (
        request.user.is_superuser
        or "fees_master_add" in request.permissions
        or "fees_master_view" in request.permissions
    ):
        try:
            records = FeesMaster.objects.filter(status="Active")
            form = FeesMasterForm()
            if request.method == "POST":
                form = FeesMasterForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/fees_master")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "fees_master": "active"}
            return render(request, "Fees_Collection/fees_master.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_master_assign(request, pk):
    if request.user.is_superuser or "fees_gp_assign_view" in request.permissions:
        try:
            fees_record = FeesMaster.objects.get(id=pk)
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            category_records = StudentCategory.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                Category = request.POST.get("category")
                gender = request.POST.get("gender")
                RET = request.POST.get("RET")
                filters = {}
                if classs:
                    filters["Class"] = classs
                if section:
                    filters["section"] = section
                if Category:
                    filters["category"] = Category
                if gender:
                    filters["gender"] = gender
                if RET:
                    filters["rte"] = RET

                records = StudentAdmission.objects.filter(
                    **filters, session=request.Session
                )
                context = {
                    "fees_master": "active",
                    "category_records": category_records,
                    "class_records": class_records,
                    "section_records": section_records,
                    "records": records,
                    "fees_record": fees_record,
                    "records_count": records.count(),
                }
                return render(
                    request, "Fees_Collection/fees_master_assign.html", context
                )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")

    context = {
        "fees_master": "active",
        "category_records": category_records,
        "class_records": class_records,
        "section_records": section_records,
        "fees_record": fees_record,
    }
    return render(request, "Fees_Collection/fees_master_assign.html", context)


def fees_master_assign_js(request):
    id_list = request.GET.getlist("id_list[]")
    fees_id = request.GET.get("fees_id")
    fees_master = FeesMaster.objects.get(id=fees_id)
    for data in id_list:
        FeesAssign.objects.get_or_create(
            student_id=data,
            fees_id=fees_id,
            balance_amount=fees_master.amount,
            paid_amount=0,
            status="pending",
            session=request.Session,
        )
    data = "Saved Sucessfully"
    return JsonResponse(data, safe=False)


@login_required
def discount_js(request):
    disc = request.GET.get("disc")
    disc_ass = DiscountAssign.objects.get(id=disc)
    data = disc_ass.discount.amount
    return JsonResponse(data, safe=False)


@login_required
@user_type_required("Staff")
def fees_master_edit_1(request, pk):
    if request.user.is_superuser or "fees_master_edit" in request.permissions:
        try:
            records = FeesMaster.objects.all()
            record = FeesMaster.objects.get(id=pk)
            form = FeesMasterForm(instance=record)
            if request.method == "POST":
                form = FeesMasterForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/fees_master")
            context = {
                "form": form,
                "records": records,
                "fees_master": "active",
                "edit": True,
            }
            return render(request, "Fees_Collection/fees_master.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_master_view(request, pk):
    if request.user.is_superuser or "fees_master_view" in request.permissions:
        try:
            records = FeesMaster.objects.all()
            record = FeesMaster.objects.get(id=pk)
            form = FeesMasterForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "fees_master": "active",
                "view": True,
            }
            return render(request, "Fees_Collection/fees_master.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# larann
@login_required
@user_type_required("Staff")
def fees_master_delete(request, pk):
    if request.user.is_superuser or "fees_master_delete" in request.permissions:
        try:
            FeesMaster.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/fees_master")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_master_edit(request):
    form = FeesMasterForm()
    context = {
        "form": form,
    }
    return render(request, "Fees_Collection/fees_master_edit.html", context)


@login_required
@user_type_required("Staff")
def fees_group(request):
    if (
        request.user.is_superuser
        or "fees_group_view" in request.permissions
        or "fees_group_add" in request.permissions
    ):
        try:
            records = FeesGroup.objects.all()
            form = FeesGroupForm()
            if request.method == "POST":
                form = FeesGroupForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/fees_group")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "fees_group": "active",
            }
            return render(request, "Fees_Collection/fees_group.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_group_edit(request, pk):
    if request.user.is_superuser or "fees_group_edit" in request.permissions:
        try:
            records = FeesGroup.objects.all()
            record = FeesGroup.objects.get(id=pk)
            form = FeesGroupForm(instance=record)
            if request.method == "POST":
                form = FeesGroupForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/fees_group")
            context = {
                "form": form,
                "records": records,
                "fees_group": "active",
                "edit": True,
            }
            return render(request, "Fees_Collection/fees_group.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_group_view(request, pk):
    if request.user.is_superuser or "fees_group_view" in request.permissions:
        try:
            records = FeesGroup.objects.all()
            record = FeesGroup.objects.get(id=pk)
            form = FeesGroupForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "fees_group": "active",
                "view": True,
            }
            return render(request, "Fees_Collection/fees_group.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_group_delete(request, pk):
    if request.user.is_superuser or "fees_group_delete" in request.permissions:
        try:
            FeesGroup.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/fees_group")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def edit_fees_group(request):
    form = FeesGroupForm()
    context = {
        "form": form,
    }
    return render(request, "Fees_Collection/edit_fees_group.html", context)


@login_required
@user_type_required("Staff")
def fees_type(request):
    if (
        request.user.is_superuser
        or "fees_type_view" in request.permissions
        or "fees_type_add" in request.permissions
    ):
        try:
            records = FeesType.objects.all()
            form = FeesTypeForm()
            if request.method == "POST":
                form = FeesTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/fees_type")
                else:
                    for field_name, error_messages in form.errors.items():
                        for message in error_messages:
                            messages.error(
                                request, f"{field_name.capitalize()}: {message}"
                            )
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "fees_type": "active",
            }
            return render(request, "Fees_Collection/fees_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_type_edit(request, pk):
    if request.user.is_superuser or "fees_type_edit" in request.permissions:
        try:
            records = FeesType.objects.all()
            record = FeesType.objects.get(id=pk)
            form = FeesTypeForm(instance=record)
            if request.method == "POST":
                form = FeesTypeForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/fees_type")
            context = {
                "form": form,
                "records": records,
                "fees_type": "active",
                "edit": True,
            }
            return render(request, "Fees_Collection/fees_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_type_view(request, pk):
    if request.user.is_superuser or "fees_type_view" in request.permissions:
        try:
            records = FeesType.objects.all()
            record = FeesType.objects.get(id=pk)
            form = FeesTypeForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "fees_type": "active",
                "view": True,
            }
            return render(request, "Fees_Collection/fees_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_type_delete(request, pk):
    if request.user.is_superuser or "fees_type_delete" in request.permissions:
        try:
            FeesType.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/fees_type")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def edit_fees_type(request):
    form = FeesGroupForm()
    context = {
        "form": form,
    }
    return render(request, "Fees_Collection/edit_fees_type.html", context)


# ... (your existing imports and decorators)

from django.http import JsonResponse


@login_required
@user_type_required("Staff")
def fees_discount(request):
    if (
        request.user.is_superuser
        or "fees_discount_add" in request.permissions
        or "fees_discount_view" in request.permissions
    ):
        try:
            # Dynamically get the FeesMaster instance
            total_fees_master = (
                FeesMaster.objects.first()
            )  # You can adjust the query as needed

            if not total_fees_master:
                messages.warning(request, "No FeesMaster instance found.")
                return HttpResponseRedirect("/fees_discount")

            total_fees_amount = total_fees_master.amount

            records = FeesTypeDiscount.objects.all()
            initial_data = {"total_fees_amount": total_fees_amount}

            form = FeesTypeDiscountForm(initial=initial_data)

            if request.method == "POST":
                form = FeesTypeDiscountForm(request.POST)
                if form.is_valid():
                    discount = form.save(commit=False)

                    if discount.discount_type == "Discount Percentage":
                        total_amount = total_fees_amount
                        calculated_percentage_amount = (
                            discount.percentage / 100
                        ) * total_amount
                        discount.amount = calculated_percentage_amount
                        discount.percentage_amount = calculated_percentage_amount

                        print(f"Calculated Amount: {discount.amount}")
                        print(
                            f"Calculated Percentage Amount: {discount.percentage_amount}"
                        )

                    discount.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/fees_discount")
                else:
                    print(form.errors)

            context = {"form": form, "records": records, "fees_discountt": "active"}
            return render(request, "Fees_Collection/fees_discount.html", context)

        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# @login_required
# @user_type_required("Staff")
# def fees_discount(request):
#     if (
#         request.user.is_superuser
#         or "fees_discount_add" in request.permissions
#         or "fees_discount_view" in request.permissions
#     ):
#         try:
#             # Dynamically get the FeesMaster instance
#             total_fees_master = (
#                 FeesMaster.objects.first()
#             )  # You can adjust the query as needed

#             if not total_fees_master:
#                 messages.warning(request, "No FeesMaster instance found.")
#                 return HttpResponseRedirect("/fees_discount")

#             total_fees_amount = total_fees_master.amount

#             records = FeesTypeDiscount.objects.all()
#             initial_data = {"total_fees_amount": total_fees_amount}

#             form = FeesTypeDiscountForm(initial=initial_data)

#             if request.method == "POST":
#                 form = FeesTypeDiscountForm(request.POST)
#                 if form.is_valid():
#                     discount = form.save(commit=False)

#                     if discount.discount_type == "Discount Percentage":
#                         total_amount = total_fees_amount
#                         calculated_percentage_amount = (
#                             discount.percentage / 100
#                         ) * total_amount
#                         discount.amount = calculated_percentage_amount
#                         discount.percentage_amount = calculated_percentage_amount

#                         print(f"Calculated Amount: {discount.amount}")
#                         print(
#                             f"Calculated Percentage Amount: {discount.percentage_amount}"
#                         )
#                     discount.save()
#                     messages.success(request, "Record Saved Successfully")
#                     return HttpResponseRedirect("/fees_discount")
#                 else:
#                     print(form.errors)

#             context = {"form": form, "records": records, "fees_discountt": "active"}
#             return render(request, "Fees_Collection/fees_discount.html", context)

#         except Exception as error:
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_discount_edit(request, pk):
    if request.user.is_superuser or "fees_discount_edit" in request.permissions:
        try:
            records = FeesTypeDiscount.objects.all()
            record = FeesTypeDiscount.objects.get(id=pk)
            form = FeesTypeDiscountForm(instance=record)
            if request.method == "POST":
                form = FeesTypeDiscountForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/fees_discount")
            context = {
                "form": form,
                "records": records,
                "fees_discount": "active",
                "edit": True,
            }
            return render(request, "Fees_Collection/fees_discount.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def fees_discount_assign(request, pk):
    if request.user.is_superuser or "fees_assign_discount_view" in request.permissions:
        try:
            fees_discount = FeesTypeDiscount.objects.get(id=pk)
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            category_records = StudentCategory.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                Category = request.POST.get("category")
                gender = request.POST.get("gender")
                RET = request.POST.get("RET")
                filters = {}
                if classs:
                    filters["Class"] = classs
                if section:
                    filters["section"] = section
                if Category:
                    filters["category"] = Category
                if gender:
                    filters["gender"] = gender
                if RET:
                    filters["rte"] = RET

                records = StudentAdmission.objects.filter(
                    **filters, session=request.Session
                )
                context = {
                    "fees_discountt": "active",
                    "category_records": category_records,
                    "class_records": class_records,
                    "section_records": section_records,
                    "records": records,
                    "fees_discount": fees_discount,
                    "records_count": records.count(),
                }
                return render(
                    request, "Fees_Collection/fees_discount_assign.html", context
                )

            context = {
                "fees_discountt": "active",
                "category_records": category_records,
                "class_records": class_records,
                "section_records": section_records,
                "fees_discount": fees_discount,
            }
            return render(request, "Fees_Collection/fees_discount_assign.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
def fees_discount_assign_js(request):
    id_list = request.GET.getlist("id_list[]")
    fees_id = request.GET.get("fees_id")
    for data in id_list:
        DiscountAssign.objects.get_or_create(
            student_id=data,
            discount_id=fees_id,
            status="pending",
            session=request.Session,
        )
    data = "Saved Sucessfully"
    return JsonResponse(data, safe=False)


def fees_discount_delete(request, pk):
    if request.user.is_superuser or "fees_discount_delete" in request.permissions:
        try:
            FeesTypeDiscount.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/fees_discount")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def edit_fees_discount(request):
    form = FeesGroupForm()
    context = {
        "form": form,
    }
    return render(request, "Fees_Collection/edit_fees_discount.html", context)


from django.db.models import Sum


@login_required
@user_type_required("Staff")
def fees_carry_forward(request):
    class_records = Class.objects.all()
    Session_records = Session.objects.exclude(id=request.Session.id)
    if request.method == "POST":
        session = request.POST.get("session")
        pre_fess = FeesAssign.objects.filter(
            student__Class__id=request.POST.get("class"),
            student__section__id=request.POST.get("section"),
            session=session,
            status__in=["pending", "partially paid"],
        )
        admis_no_list = list(set([data.student.admission_no for data in pre_fess]))
        pre_fees_rcords = []
        for data in admis_no_list:
            dict = {}
            records = pre_fess.filter(student__admission_no=data)
            dict["obj"] = records.last()
            dict["total_amount"] = records.aggregate(Sum("balance_amount"))[
                "balance_amount__sum"
            ]
            pre_fees_rcords.append(dict)
        context = {
            "fees_carry_forward": "active",
            "class_records": class_records,
            "Session_records": Session_records,
            "pre_fees_rcords": pre_fees_rcords,
            "session": session,
        }
        return render(request, "Fees_Collection/fees_carry_forward.html", context)
    context = {
        "fees_carry_forward": "active",
        "class_records": class_records,
        "Session_records": Session_records,
    }
    return render(request, "Fees_Collection/fees_carry_forward.html", context)


@login_required
@user_type_required("Staff")
def fees_carry_forward_save(request):
    admission_list = request.POST.getlist("admission_no")
    print("admission_list", request.POST)
    for data in admission_list:
        print("===", data)
        amount = request.POST.get(f"amount_{data}")
        fess_group = FeesGroup.objects.get_or_create(name="Balance Master")
        fess_type = FeesType.objects.get_or_create(
            name="Previous Session Balance", Fees_code="Previous Session Balance"
        )
        print(fess_group[0].id, "========.SSS")
        fess_master = FeesMaster.objects.get_or_create(
            fees_group_id=fess_group[0].id,
            fees_type_id=fess_type[0].id,
            amount=amount,
            percentage=0,
            fine_amount=0,
            status="Inactive",
        )
        student_obj = StudentAdmission.objects.filter(admission_no=data).first()
        FeesAssign.objects.create(
            student=student_obj,
            fees=fess_master[0],
            balance_amount=amount,
            paid_amount=0,
            session=request.Session,
            status="pending",
        )
        session = request.POST.get("session")
        pre_fess = FeesAssign.objects.filter(
            student__admission_no=data, session=session
        )
        for update in pre_fess:
            update.status = "Forward"
            update.save()
    return redirect("fees_carry_forward")


@login_required
@user_type_required("Staff")
def fees_remainder(request):
    context = {"fees_remainder": "active"}
    return render(request, "Fees_Collection/fees_remainder.html", context)


# Expense
# Expense
@login_required
@user_type_required("Staff")
def add_expense(request):
    if (
        request.user.is_superuser
        or "expense_view" in request.permissions
        or "expense_add" in request.permissions
        or request.permissions
    ):
        try:
            records = AddExpense.objects.all()
            form = AddExpenseForm()

            # Get user_id from the current user
            user_id = request.user.id

            # Assuming User model has a ForeignKey to School
            user_school = request.user.school

            # Get the school account associated with the user's school
            school_account = user_school.account

            if request.method == "POST":
                form = AddExpenseForm(request.POST, request.FILES)
                if form.is_valid():
                    expense_instance = form.save()

                    # Call collect_expense function with user_id
                    success = collect_expense(expense_instance, user_id)

                    if success:
                        messages.success(request, "Record Saved Successfully")
                    else:
                        messages.error(request, "Failed to process the expense")
                    return HttpResponseRedirect("/add_expense")
                else:
                    print(form.errors)

            context = {"form": form, "records": records, "add_expense": "active"}
            return render(request, "Expenses/add_expense.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_expense_edit(request, pk):
    if (
        request.user.is_superuser
        or "expense_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = AddExpense.objects.all()
            record = AddExpense.objects.get(id=pk)
            form = AddExpenseForm(instance=record)
            if request.method == "POST":
                form = AddExpenseForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_expense")
            context = {
                "form": form,
                "records": records,
                "add_expense": "active",
                "edit": True,
            }
            return render(request, "Expenses/add_expense.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_expense_view(request, pk):
    if (
        request.user.is_superuser
        or "expense_view" in request.permissions
        or request.permissions
    ):
        try:
            records = AddExpense.objects.all()
            record = AddExpense.objects.get(id=pk)
            form = AddExpenseForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "add_expense": "active",
                "view": True,
            }
            return render(request, "Expenses/add_expense.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_expense_delete(request, pk):
    if (
        request.user.is_superuser
        or "expense_delete" in request.permissions
        or request.permissions
    ):
        try:
            AddExpense.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_expense")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def edit_add_expense(request):
    form = AddExpenseForm()
    context = {
        "form": form,
    }
    return render(request, "Expenses/edit_add_expense.html", context)


@login_required
@user_type_required("Staff")
def search_expense(request):
    if (
        request.user.is_superuser
        or "search_expense_view" in request.permissions
        or request.permissions
    ):
        try:
            if request.method == "POST":
                from_date = request.POST.get("from_date")
                to_date = request.POST.get("to_date")
                filters = {}
                if from_date and to_date:
                    filters["date__range"] = [from_date, to_date]
                elif from_date:
                    filters["date__gte"] = from_date
                elif to_date:
                    filters["date__lte"] = to_date

                records = AddExpense.objects.filter(**filters)
                context = {
                    "search_expense": "active",
                    "records": records,
                }
                return render(request, "Expenses/search_expense.html", context)
            context = {
                "search_expense": "active",
            }
            return render(request, "Expenses/search_expense.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def expense_head(request):
    if (
        request.user.is_superuser
        or "expense_head_view" in request.permissions
        or "expense_head_add" in request.permissions
        or request.permissions
    ):
        try:
            records = ExpenseHead.objects.all()
            form = ExpenseHeadForm()
            if request.method == "POST":
                form = ExpenseHeadForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/expense_head")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "expense_head": "active"}
            return render(request, "Expenses/expense_head.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def expense_head_edit_1(request, pk):
    if (
        request.user.is_superuser
        or "expense_head_edit" in request.permissions
        or request.permissions
    ):
        try:
            records = ExpenseHead.objects.all()
            record = ExpenseHead.objects.get(id=pk)
            form = ExpenseHeadForm(instance=record)
            if request.method == "POST":
                form = ExpenseHeadForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/expense_head")
            context = {
                "form": form,
                "records": records,
                "expense_head": "active",
                "edit": True,
            }
            return render(request, "Expenses/expense_head.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def expense_head_view(request, pk):
    if (
        request.user.is_superuser
        or "expense_head_view" in request.permissions
        or request.permissions
    ):
        try:
            records = ExpenseHead.objects.all()
            record = ExpenseHead.objects.get(id=pk)
            form = ExpenseHeadForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "expense_head": "active",
                "view": True,
            }
            return render(request, "Expenses/expense_head.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def expense_head_delete(request, pk):
    if (
        request.user.is_superuser
        or "expense_head_delete" in request.permissions
        or request.permissions
    ):
        try:
            ExpenseHead.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/expense_head")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Attendance
@login_required
@user_type_required("Staff")
def student_attendance(request):
    if (
        request.user.is_superuser
        or "student_period_attendance_add" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            if request.POST.get("search") == "search":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                attendance_date = request.POST.get("attendance_date")
                filters = {}
                if classs:
                    filters["Class"] = classs
                if section:
                    filters["section"] = section
                records = StudentAdmission.objects.filter(
                    **filters, session=request.Session
                )
                attendance_records = StudentAttendance.objects.filter(
                    student_id__in=records.values("id"), attendance_date=attendance_date
                )

                context = {
                    "student_attendance": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                    "attendance_date": attendance_date,
                    "attendance_records": attendance_records,
                }
                return render(request, "Attendance/student_attendance.html", context)
            if request.POST.get("all_save") == "all_save":
                student_id = request.POST.getlist("student_id")
                for data in student_id:
                    print(request.POST.get(f"attendance{data}"))
                    holiday = request.POST.get("holiday")
                    if request.POST.get(f"attendance{data}") or holiday:
                        edit_stu = StudentAttendance.objects.filter(
                            student=data,
                            attendance_date=request.POST.get("attendance_date1"),
                        ).last()
                        if holiday:
                            attendance_status = "Holiday"
                        else:
                            attendance_status = request.POST.get(f"attendance{data}")
                        if edit_stu:
                            edit_stu.attendance_status = attendance_status
                            edit_stu.note = request.POST.get(f"note{data}")
                            edit_stu.save()
                        else:
                            print("save")
                            StudentAttendance.objects.create(
                                student_id=data,
                                attendance_status=attendance_status,
                                attendance_date=request.POST.get("attendance_date1"),
                                note=request.POST.get(f"note{data}"),
                            )
                messages.success(request, "Record Saved Successfully")
                return redirect("student_attendance")
            context = {
                "student_attendance": "active",
                "class_records": class_records,
                "section_records": section_records,
            }
            return render(request, "Attendance/student_attendance.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def approve_leave(request):
    if request.user.is_superuser or "approve_leave_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            records = Addleave.objects.filter(session=request.Session)
            if request.POST.get("search") == "search":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                filters = {}
                if classs:
                    filters["Class"] = classs
                if section:
                    filters["section"] = section
                stu = StudentAdmission.objects.filter(
                    **filters, session=request.Session
                )
                records = Addleave.objects.filter(
                    student__in=stu.values("id"), session=request.Session
                )
            form = AddleaveForm()
            if request.method == "POST":
                form = AddleaveForm(request.POST)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.session = request.Session
                    instance.created_by = request.user
                    instance.save()
                    return HttpResponseRedirect("/approve_leave")
            context = {
                "form": form,
                "records": records,
                "approve_leave": "active",
                "class_records": class_records,
                "section_records": section_records,
            }
            return render(request, "Attendance/approve_leave.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def leave_approve_disappove(request, pk):
    records = Addleave.objects.get(id=pk)
    if records.status == "disapprove":
        records.status = "approve"
        records.approved_by = request.user
        messages.success(request, "Record Saved Successfully")
    elif records.status == "approve":
        records.status = "disapprove"
        messages.success(request, "Record Saved Successfully")
    records.save()
    return redirect("approve_leave")


@login_required
@user_type_required("Staff")
def approve_leave_edit(request, pk):
    if request.user.is_superuser or "approve_leave_edit" in request.permissions:
        try:
            records = Addleave.objects.all()
            record = Addleave.objects.get(id=pk)
            form = AddleaveForm(instance=record)
            if request.method == "POST":
                form = AddleaveForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/approve_leave")
            context = {"form": form, "records": records, "approve_leave": "active"}
            return render(request, "Attendance/approve_leave_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def approve_leave_view(request, pk):
    if request.user.is_superuser or "approve_leave_view" in request.permissions:
        try:
            records = Addleave.objects.all()
            record = Addleave.objects.get(id=pk)
            form = AddleaveForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "approve_leave": "active",
                "view": True,
            }
            return render(request, "Attendance/approve_leave_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def approve_leave_delete(request, pk):
    if request.user.is_superuser or "approve_leave_delete" in request.permissions:
        try:
            Addleave.objects.get(id=pk).delete()
            return HttpResponseRedirect("/approve_leave")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def attendance_by_date(request):
    if request.user.is_superuser or "attendance_by_date_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            if request.POST.get("search") == "search":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                attendance_date = request.POST.get("attendance_date")
                filters = {}
                if classs:
                    filters["Class"] = classs
                if section:
                    filters["section"] = section
                records = StudentAdmission.objects.filter(
                    **filters, session=request.Session
                )
                attendance_records = StudentAttendance.objects.filter(
                    attendance_date=attendance_date, student__in=records.values("id")
                )
                context = {
                    "attendance_by_date": "active",
                    "records": records,
                    "class_records": class_records,
                    "attendance_records": attendance_records,
                    "section_records": section_records,
                    "attendance_date": attendance_date,
                }
                return render(request, "Attendance/attendance_by_date.html", context)
            context = {
                "attendance_by_date": "active",
                "class_records": class_records,
                "section_records": section_records,
            }
            return render(request, "Attendance/attendance_by_date.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Examinations


@login_required
@user_type_required("Staff")
def exam_group(request):
    if (
        request.user.is_superuser
        or "exam_group_add" in request.permissions
        or "exam_group_view" in request.permissions
    ):
        try:
            exam_group = examGroup.objects.all()
            records = []
            for data in exam_group:
                dict = {}
                total = AddExam.objects.filter(
                    exam_group=data.id, session=request.Session
                ).count()
                dict["id"] = data.id
                dict["name"] = data.name
                dict["exam_type"] = data.exam_type
                dict["description"] = data.description
                dict["exam_count"] = total
                records.append(dict)
            form = examGroupForm()
            if request.method == "POST":
                form = examGroupForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/exam_group")
            context = {"form": form, "records": records, "exam_group": "active"}
            return render(request, "Examinations/exam_group.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def exam_group_edit(request, pk):
    if request.user.is_superuser or "exam_group_edit" in request.permissions:
        try:
            records = examGroup.objects.all()
            record = examGroup.objects.get(id=pk)
            form = examGroupForm(instance=record)
            if request.method == "POST":
                form = examGroupForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/exam_group")
            context = {
                "form": form,
                "records": records,
                "exam_group": "active",
                "edit": True,
            }
            return render(request, "Examinations/exam_group.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def exam_group_view(request, pk):
    if request.user.is_superuser or "exam_group_view" in request.permissions:
        try:
            records = examGroup.objects.all()
            record = examGroup.objects.get(id=pk)
            form = examGroupForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "exam_group": "active",
                "view": True,
            }
            return render(request, "Examinations/exam_group.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def exam_group_delete(request, pk):
    if request.user.is_superuser or "exam_group_delete" in request.permissions:
        try:
            examGroup.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/exam_group")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def exam_schedule(request):
    if request.user.is_superuser or "exam_schedule_view" in request.permissions:
        try:
            exam_group = examGroup.objects.all()
            if request.method == "POST":
                records = AddExamSubject.objects.filter(exam=request.POST.get("exam"))
                context = {
                    "exam_schedule": "active",
                    "exam_group": exam_group,
                    "records": records,
                }
                return render(request, "Examinations/exam_schedule.html", context)
            context = {"exam_schedule": "active", "exam_group": exam_group}
            return render(request, "Examinations/exam_schedule.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
def exam_js(request):
    exam_records = AddExam.objects.filter(
        exam_group=request.GET.get("exam_group"), session=request.Session
    ).values("id", "Exam")
    return JsonResponse(data=list(exam_records), safe=False)


@login_required
@user_type_required("Staff")
def exam_result(request):
    if request.user.is_superuser or "exam_result_view" in request.permissions:
        try:
            exam_group = examGroup.objects.all()
            class_records = Class.objects.all()
            session_records = Session.objects.all()
            if request.method == "POST":
                exams = AddExamSubject.objects.filter(exam=request.POST.get("exam"))
                student = ExamStudent.objects.filter(
                    Class=request.POST.get("class"),
                    section=request.POST.get("section"),
                    exam=request.POST.get("exam"),
                )
                records = EntryMarks.objects.filter(
                    student__Class=request.POST.get("class"),
                    student__section=request.POST.get("section"),
                    exam=request.POST.get("exam"),
                )
                listt = []
                for data in student:
                    total_mark = 0
                    total = 0
                    mark_list = []
                    results = []
                    for sub in exams:
                        dict = {}
                        mark = EntryMarks.objects.filter(
                            exam_subject=sub, exam_student=data
                        ).last()
                        dic = {}
                        if mark:
                            dic["subject"] = mark.subject
                            total_mark += mark.marks
                            if mark.marks <= sub.marks_min:
                                results.append("Fail")
                                dic["marks"] = f"{mark.marks} (F)"
                            else:
                                results.append("Pass")
                                dic["marks"] = mark.marks
                        else:
                            dic["subject"] = sub.subject
                            dic["marks"] = ""
                            results.append(None)
                        total += sub.marks_max
                        mark_list.append(dic)

                    dict["mark_list"] = mark_list
                    dict["obj"] = data
                    dict["total"] = f"{total_mark}/{int(total)}"
                    dict["percentage"] = int(total_mark * 100 / int(total))
                    dict["result"] = results
                    grad_record = AddGrade.objects.filter(
                        exam_type=data.exam.exam_group.exam_type
                    )
                    dict["grade"] = ""
                    for grad in grad_record:
                        if (
                            grad.percent_from >= dict["percentage"]
                            and grad.percent_up_to <= dict["percentage"]
                        ):
                            dict["grade"] = grad.grade_name

                    listt.append(dict)
                context = {
                    "exam_result": "active",
                    "exam_group": exam_group,
                    "class_records": class_records,
                    "session_records": session_records,
                    "exams": exams,
                    "records": records,
                    "listt": listt,
                }
                return render(request, "Examinations/exam_result.html", context)
            context = {
                "exam_result": "active",
                "exam_group": exam_group,
                "class_records": class_records,
                "session_records": session_records,
            }
            return render(request, "Examinations/exam_result.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def design_admit_card(request):
    if (
        request.user.is_superuser
        or "design_admit_card_view" in request.permissions
        or "design_admit_card_add" in request.permissions
    ):
        try:
            records = AdmitCard.objects.all()
            form = AdmitCardForm()
            if request.method == "POST":
                form = AdmitCardForm(request.POST, request.FILES)
                print(form)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/design_admit_card")
            context = {"form": form, "records": records, "design_admit_card": "active"}
            print(records)
            return render(request, "Examinations/design_admit_card.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def design_admit_card_edit(request, pk):
    if request.user.is_superuser or "design_admit_card_edit" in request.permissions:
        if True:
            records = AdmitCard.objects.all()
            record = AdmitCard.objects.get(id=pk)
            form = AdmitCardForm(instance=record)
            if request.method == "POST":
                form = AdmitCardForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/design_admit_card")
            context = {
                "form": form,
                "records": records,
                "design_admit_card": "active",
                "record": record,
                "edit": True,
            }
            return render(request, "Examinations/design_admit_card.html", context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def design_admit_card_view(request, pk):
    if request.user.is_superuser or "design_admit_card_view" in request.permissions:
        try:
            records = AdmitCard.objects.all()
            record = AdmitCard.objects.get(id=pk)
            form = AdmitCardForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "design_admit": "active",
                "view": True,
                "record": record,
            }
            return render(request, "Examinations/design_admit_card.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def design_admit_card_delete(request, pk):
    if request.user.is_superuser or "design_admit_card_delete" in request.permissions:
        try:
            AdmitCard.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/design_admit_card")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def print_admit_card(request):
    eaxm_records = examGroup.objects.all()
    session_records = Session.objects.all()
    class_records = Class.objects.all()
    admit_card_records = AdmitCard.objects.all()
    if request.method == "POST":
        exam = request.POST.get("exam")
        admit_card = request.POST.get("admit_card")
        records = ExamStudent.objects.filter(
            exam=exam,
            student__session=request.POST.get("session"),
            Class=request.POST.get("class"),
            section=request.POST.get("section"),
        )
        context = {
            "print_admit_card": "active",
            "eaxm_records": eaxm_records,
            "session_records": session_records,
            "class_records": class_records,
            "records": records,
            "admit_card_records": admit_card_records,
            "exam": exam,
            "admit_card": admit_card,
        }
        return render(request, "Examinations/print_admit_card.html", context)
    context = {
        "print_admit_card": "active",
        "eaxm_records": eaxm_records,
        "session_records": session_records,
        "class_records": class_records,
        "admit_card_records": admit_card_records,
    }
    return render(request, "Examinations/print_admit_card.html", context)


@login_required
@user_type_required("Staff")
def printing_admit_card(request):
    admit_card = AdmitCard.objects.get(id=request.POST.get("admit_card"))
    student_records = StudentAdmission.objects.filter(
        id__in=request.POST.getlist("checkbox")
    )
    exam_sub = AddExamSubject.objects.filter(exam=request.POST.get("exam"))
    records = []
    for data in student_records:
        dict = {}
        exam_mark = EntryMarks.objects.filter(student=data)
        dict["student_obj"] = data
        dict["marks"] = exam_mark
        records.append(dict)
    print(records)
    context = {
        "print_admit_card": "active",
        "records": records,
        "data": admit_card,
        "exam_sub": exam_sub,
    }
    return render(request, "Examinations/printing_admit_card.html", context)


@login_required
@user_type_required("Staff")
def design_marksheet(request):
    if (
        request.user.is_superuser
        or "design_marksheet_add" in request.permissions
        or "design_marksheet_view" in request.permissions
    ):
        try:
            records = DesignMarkSheet.objects.all()
            form = DesignMarkSheetForm()
            if request.method == "POST":
                form = DesignMarkSheetForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/design_marksheet")
            context = {"form": form, "records": records, "design_marksheet": "active"}
            return render(request, "Examinations/design_marksheet.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def design_marksheet_edit(request, pk):
    if request.user.is_superuser or "design_marksheet_edit" in request.permissions:
        try:
            records = DesignMarkSheet.objects.all()
            record = DesignMarkSheet.objects.get(id=pk)
            form = DesignMarkSheetForm(instance=record)
            if request.method == "POST":
                form = DesignMarkSheetForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/design_marksheet")
            context = {
                "form": form,
                "records": records,
                "design_marksheet": "active",
                "record": record,
                "edit": True,
            }
            return render(request, "Examinations/design_marksheet.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def design_marksheet_view(request, pk):
    if request.user.is_superuser or "design_admit_card_view" in request.permissions:
        try:
            records = DesignMarkSheet.objects.all()
            record = DesignMarkSheet.objects.get(id=pk)
            form = DesignMarkSheetForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "design_marksheet": "active",
                "view": True,
                "record": record,
            }
            return render(request, "Examinations/design_marksheet.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def design_marksheet_delete(request, pk):
    if request.user.is_superuser or "design_marksheet_delete":
        try:
            DesignMarkSheet.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/design_marksheet")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def print_marksheet(request):
    eaxm_records = examGroup.objects.all()
    session_records = Session.objects.all()
    class_records = Class.objects.all()
    marksheet_records = DesignMarkSheet.objects.all()
    if request.method == "POST":
        exam = request.POST.get("exam")
        admit_card = request.POST.get("admit_card")
        records = ExamStudent.objects.filter(
            exam=exam,
            student__session=request.POST.get("session"),
            Class=request.POST.get("class"),
            section=request.POST.get("section"),
        )
        context = {
            "print_marksheet": "active",
            "eaxm_records": eaxm_records,
            "session_records": session_records,
            "class_records": class_records,
            "marksheet_records": marksheet_records,
            "records": records,
            "exam": exam,
            "admit_card": admit_card,
        }
        return render(request, "Examinations/print_marksheet.html", context)
    context = {
        "print_marksheet": "active",
        "eaxm_records": eaxm_records,
        "session_records": session_records,
        "class_records": class_records,
        "marksheet_records": marksheet_records,
    }
    return render(request, "Examinations/print_marksheet.html", context)


@login_required
@user_type_required("Staff")
def printing_marksheet(request):
    marksheet = DesignMarkSheet.objects.get(id=request.POST.get("admit_card"))
    student_records = StudentAdmission.objects.filter(
        id__in=request.POST.getlist("checkbox")
    )
    exam_sub = AddExamSubject.objects.filter(exam=request.POST.get("exam"))
    records = []
    for data in student_records:
        dict = {}
        exam_mark = EntryMarks.objects.filter(student=data)
        dict["student_obj"] = data
        dict["marks"] = exam_mark
        dict["total"] = exam_mark.aggregate(Sum("marks")).get("marks__sum")
        dict["total_in_words"] = num2words(dict["total"]).upper()
        grad_record = AddGrade.objects.filter(
            exam_type=exam_mark.first().exam.exam_group.exam_type
        )
        dict["percentage"] = int(
            dict["total"]
            * 100
            / int(
                exam_mark.aggregate(Sum("exam_subject__marks_max")).get(
                    "exam_subject__marks_max__sum"
                )
            )
        )
        dict["grade"] = ""
        for grad in grad_record:
            if (
                grad.percent_from >= dict["percentage"]
                and grad.percent_up_to <= dict["percentage"]
            ):
                dict["grade"] = grad.grade_name

        records.append(dict)
    context = {
        "print_admit_card": "active",
        "records": records,
        "data": marksheet,
        "exam_sub": exam_sub,
    }
    return render(request, "Examinations/printing_marksheet.html", context)

    # grade


@login_required
@user_type_required("Staff")
def marks_grade(request):
    records = AddGrade.objects.all()
    form = AddGradeForm()
    if request.method == "POST":
        form = AddGradeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/marks_grade")
    context = {"form": form, "records": records, "marks_grade": "active"}
    return render(request, "Examinations/marks_grade.html", context)


@login_required
@user_type_required("Staff")
def marks_grade_edit(request, pk):
    records = AddGrade.objects.all()
    record = AddGrade.objects.get(id=pk)
    form = AddGradeForm(instance=record)
    if request.method == "POST":
        form = AddGradeForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/marks_grade")
    context = {"form": form, "records": records, "marks_grade": "active"}
    return render(request, "Examinations/marks_grade_edit.html", context)


@login_required
@user_type_required("Staff")
def marks_grade_view(request, pk):
    records = AddGrade.objects.all()
    record = AddGrade.objects.get(id=pk)
    form = AddGradeForm(instance=record)
    context = {"form": form, "records": records, "marks_grade": "active", "view": True}
    return render(request, "Examinations/marks_grade_edit.html", context)


@login_required
@user_type_required("Staff")
def marks_grade_delete(request, pk):
    AddGrade.objects.get(id=pk).delete()
    return HttpResponseRedirect("/marks_grade")


# assign subject


@login_required
@user_type_required("Staff")
def assign_subject(request):
    records = AssignSubject.objects.all()
    subject_records = Subjects.objects.all()
    form = AssignSubjectForm()
    if request.method == "POST":
        form = AssignSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Saved Successfully")
            return HttpResponseRedirect("/assign_subject")
        else:
            messages.error(request, "Record not saved")
            return redirect("assign_subject")

    context = {
        "form": form,
        "records": records,
        "subject_records": subject_records,
        "marks_grade": "active",
    }
    return render(request, "Examinations/assign_subject.html", context)


@login_required
@user_type_required("Staff")
def assign_subject_edit(request, pk):
    records = AssignSubject.objects.all()
    record = AssignSubject.objects.get(id=pk)
    form = AssignSubjectForm(instance=record)
    if request.method == "POST":
        form = AssignSubjectForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/assign_subject")
    context = {"form": form, "records": records, "marks_grade": "active"}
    return render(request, "Examinations/assign_subject_edit.html", context)


@login_required
@user_type_required("Staff")
def assign_subject_view(request, pk):
    records = AssignSubject.objects.all()
    record = AssignSubject.objects.get(id=pk)
    form = AssignSubjectForm(instance=record)
    context = {"form": form, "records": records, "marks_grade": "active", "view": True}
    return render(request, "Examinations/assign_subject_edit.html", context)


@login_required
@user_type_required("Staff")
def assign_subject_delete(request, pk):
    AssignSubject.objects.get(id=pk).delete()
    return HttpResponseRedirect("/assign_subject")


@login_required
@user_type_required("Staff")
def online_exam(request):
    records = OnlineExam.objects.all()
    form = OnlineExamForm()
    if request.method == "POST":
        form = OnlineExamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/online_exam")
        else:
            print(form.errors)
    context = {"form": form, "records": records, "online_exam": "active"}
    return render(request, "OnlineExamination/online_exam.html", context)


@login_required
@user_type_required("Staff")
def online_exam_edit(request, pk):
    records = OnlineExam.objects.all()
    record = OnlineExam.objects.get(id=pk)
    form = OnlineExamForm(instance=record)
    if request.method == "POST":
        form = OnlineExamForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/online_exam")
    context = {"form": form, "records": records, "online_exam": "active"}
    return render(request, "OnlineExamination/online_exam_edit.html", context)


@login_required
@user_type_required("Staff")
def online_exam_view(request, pk):
    records = OnlineExam.objects.all()
    record = OnlineExam.objects.get(id=pk)
    form = OnlineExamForm(instance=record)
    context = {"form": form, "records": records, "online_exam": "active", "view": True}
    return render(request, "OnlineExamination/online_exam_edit.html", context)


@login_required
@user_type_required("Staff")
def online_exam_delete(request, pk):
    OnlineExam.objects.get(id=pk).delete()
    return HttpResponseRedirect("/online_exam")


@login_required
@user_type_required("Staff")
def question_bank(request):
    if (
        request.user.is_superuser
        or "online_admission_view" in request.permissions
        or "online_admission_add" in request.permissions
    ):
        try:
            records = QuestionBank.objects.all()
            form = QuestionBankForm()
            if request.method == "POST":
                form = QuestionBankForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/question_bank")
            context = {"form": form, "records": records, "question_bank": "active"}
            return render(request, "OnlineExamination/question_bank.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "error.html")


@login_required
@user_type_required("Staff")
def question_bank_edit(request, pk):
    if request.user.is_superuser or "online_admission_edit" in request.permissions:
        try:
            records = QuestionBank.objects.all()
            record = QuestionBank.objects.get(id=pk)
            form = QuestionBankForm(instance=record)
            if request.method == "POST":
                form = QuestionBankForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/question_bank")
            context = {
                "form": form,
                "records": records,
                "question_bank": "active",
                "edit": True,
            }
            return render(request, "OnlineExamination/question_bank.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "error.html")


@login_required
@user_type_required("Staff")
def question_bank_view(request, pk):
    if request.user.is_superuser or "online_admission_view" in request.permissions:
        try:
            records = QuestionBank.objects.all()
            record = QuestionBank.objects.get(id=pk)
            form = QuestionBankForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "question_bank": "active",
                "view": True,
            }
            return render(request, "OnlineExamination/question_bank.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "error.html")


@login_required
@user_type_required("Staff")
def question_bank_delete(request, pk):
    QuestionBank.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/question_bank")


# Lesson Plan


def get_week_dates(year, week_number):
    # Calculate the date of the first day of the year
    first_day_of_year = datetime(year, 1, 1)

    # Calculate the date of the first day of the requested week
    days_offset = (week_number - 1) * 7
    first_day_of_week = first_day_of_year + timedelta(days=days_offset)

    # Create a list to hold all the dates of the week
    week_dates = []

    # Calculate the dates for the rest of the week
    for i in range(1, 8):
        next_day = first_day_of_week + timedelta(days=i)
        week_dates.append(next_day)

    return week_dates


@login_required
@user_type_required("Staff")  # manage_lesson_plan Pending
def manage_lesson_plan(request):
    staff_records = AddStaff.objects.filter(roles__name__icontains="teacher")
    if request.method == "POST":
        lesson_records = Lesson.objects.all()
        topic_records = topic.objects.all()
        teacher = request.POST.get("teacher")
        week = request.POST.get("week_days")
        week_split = week.split("-")
        year = int(week_split[0])
        week_number = int(week_split[1][1:])
        dates_in_week = get_week_dates(year, week_number)
        TimeTable_records = TimeTable.objects.filter(
            teacher=teacher, session=request.Session
        )
        week_days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        Monday = []
        Tuesday = []
        Wednesday = []
        Thursday = []
        Friday = []
        Saturday = []
        Sunday = []
        week_no = 0
        for days in week_days:
            time_table_record = TimeTable_records.filter(day=days)
            for data in time_table_record:
                lesson_plan = LessonPlan.objects.filter(
                    time_table=data, date=dates_in_week[week_no].date()
                ).last()
                if week_no == 0:
                    if lesson_plan:
                        Monday.append(["Edit", lesson_plan])
                    else:
                        Monday.append(["Add", data])
                elif week_no == 1:
                    if lesson_plan:
                        Tuesday.append(["Edit", lesson_plan])
                    else:
                        Tuesday.append(["Add", data])
                elif week_no == 2:
                    if lesson_plan:
                        Wednesday.append(["Edit", lesson_plan])
                    else:
                        Wednesday.append(["Add", data])
                elif week_no == 3:
                    if lesson_plan:
                        Thursday.append(["Edit", lesson_plan])
                    else:
                        Thursday.append(["Add", data])
                elif week_no == 4:
                    if lesson_plan:
                        Friday.append(["Edit", lesson_plan])
                    else:
                        Friday.append(["Add", data])
                elif week_no == 5:
                    if lesson_plan:
                        Saturday.append(["Edit", lesson_plan])
                    else:
                        Saturday.append(["Add", data])
                elif week_no == 6:
                    if lesson_plan:
                        Sunday.append(["Edit", lesson_plan])
                    else:
                        Sunday.append(["Add", data])
            print(Monday)
            week_no += 1
        context = {
            "manage_lesson_plan": "active",
            "staff_records": staff_records,
            "TimeTable_records": TimeTable_records,
            "lesson_records": lesson_records,
            "topic_records": topic_records,
            "dates_in_week": dates_in_week,
            "Monday": Monday,
            "Tuesday": Tuesday,
            "Wednesday": Wednesday,
            "Thursday": Thursday,
            "Friday": Friday,
            "Saturday": Saturday,
            "Sunday": Sunday,
            "teacher": int(teacher),
            "week": week,
        }
        return render(request, "Lesson_plan/manage_lesson_plan.html", context)
    context = {"manage_lesson_plan": "active", "staff_records": staff_records}
    return render(request, "Lesson_plan/manage_lesson_plan.html", context)


@login_required
def manage_lesson_topic_js(request):
    records = topic.objects.filter(lesson_name=request.GET.get("lesson_id"))
    print(records)
    return JsonResponse(data=list(records.values("id", "topic_name")), safe=False)


@login_required
def edit_manage_lesson_js(request):
    records = LessonPlan.objects.get(id=request.GET.get("pk"))
    data = {
        "id": records.id,
        "lesson": records.lesson.id,
        "topic": records.topic.id,
        "lesson_name": records.lesson.lesson_name,
        "topic_name": records.topic.topic_name,
        "sub_topic": records.sub_topic,
        "time_from": records.time_table.time_from,
        "time_to": records.time_table.time_to,
        "time_table": records.time_table.id,
        "date": records.date,
        "teaching_method": records.teaching_method,
        "general_objectives": records.general_objectives,
        "pervious_knowledge": records.pervious_knowledge,
        "comprehensive_questions": records.comprehensive_questions,
        "presentation": records.presentation,
        "class": records.time_table.Class.Class,
        "section": records.time_table.section.section_name,
        "subject": records.time_table.subject.subject_name,
    }
    return JsonResponse(data)


@login_required
@user_type_required("Staff")
def manage_lesson_save(request):
    lesson_plan_id = request.POST.get("lesson_plan_id")
    print(lesson_plan_id)
    if lesson_plan_id:
        record = LessonPlan.objects.get(id=lesson_plan_id)
        record.lesson_id = request.POST.get("lesson")
        record.topic_id = request.POST.get("topic")
        record.time_table_id = request.POST.get("timetable_id")
        record.sub_topic = request.POST.get("sub_topic")
        record.lecture_youtube_url = request.POST.get("lecture_youtube_url")
        if request.FILES.get("lecture_vedio"):
            record.lecture_vedio = request.FILES.get("lecture_vedio")
        if request.FILES.get("attachment"):
            record.attachment = request.FILES.get("attachment")
        record.teaching_method = request.POST.get("teaching_method")
        record.general_objectives = request.POST.get("general_objectives")
        record.pervious_knowledge = request.POST.get("pervious_knowledge")
        record.comprehensive_questions = request.POST.get("comprehensive_questions")
        record.presentation = request.POST.get("presentation")
        record.date = request.POST.get("date")
        record.save()
    else:
        print("else")
        LessonPlan.objects.create(
            lesson_id=request.POST.get("lesson"),
            topic_id=request.POST.get("topic"),
            time_table_id=request.POST.get("timetable_id"),
            sub_topic=request.POST.get("sub_topic"),
            lecture_youtube_url=request.POST.get("lecture_youtube_url"),
            lecture_vedio=request.FILES.get("lecture_vedio"),
            attachment=request.FILES.get("attachment"),
            teaching_method=request.POST.get("teaching_method"),
            general_objectives=request.POST.get("general_objectives"),
            pervious_knowledge=request.POST.get("pervious_knowledge"),
            comprehensive_questions=request.POST.get("comprehensive_questions"),
            presentation=request.POST.get("presentation"),
            date=request.POST.get("date"),
            created_by=request.user,
        )
    return redirect("manage_lesson_plan")


@login_required
@user_type_required("Staff")
def manage_lesson_delete(request, pk):
    LessonPlan.objects.get(id=pk).delete()
    return redirect("manage_lesson_plan")


@login_required
@user_type_required("Staff")
def lesson(request):
    if (
        request.user.is_superuser
        or "lesson_view" in request.permissions
        or "lesson_add" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            records = Lesson.objects.all().order_by("subject")
            if request.method == "POST":
                classs = request.POST.get("Class")
                section = request.POST.get("section")
                subject_groups = request.POST.get("subject_group")
                subject = request.POST.get("subject")
                lesson_list = request.POST.getlist("lesson_name")
                for i in range(len(lesson_list)):
                    Lesson.objects.get_or_create(
                        Class_id=classs,
                        section_id=section,
                        subject_group_id=subject_groups,
                        subject_id=subject,
                        lesson_name=lesson_list[i],
                    )
                messages.success(request, "Record Saved Successfully")
                return HttpResponseRedirect("/lesson")

            context = {
                "records": records,
                "lesson": "active",
                "class_records": class_records,
            }
            return render(request, "Lesson_plan/lesson.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def lesson_edit(request, sub):
    if request.user.is_superuser or "lesson_edit" in request.permissions:
        try:
            class_records = Class.objects.all()
            record = Lesson.objects.filter(subject=sub)
            records = Lesson.objects.all().order_by("subject")
            if request.method == "POST":
                classs = request.POST.get("Class")
                section = request.POST.get("section")
                subject_groups = request.POST.get("subject_group")
                subject = request.POST.get("subject")
                lesson_list = request.POST.getlist("lesson_name")
                new_lesson_list = request.POST.getlist("new_lesson_name")
                ids = request.POST.getlist("ids")
                for i in range(len(lesson_list)):
                    data = Lesson.objects.get(id=ids[i])
                    data.Class_id = classs
                    data.section_id = section
                    data.subject_group_id = subject_groups
                    data.subject_id = subject
                    data.lesson_name = lesson_list[i]
                    data.save()
                for i in range(len(new_lesson_list)):
                    Lesson.objects.get_or_create(
                        Class_id=classs,
                        section_id=section,
                        subject_group_id=subject_groups,
                        subject_id=subject,
                        lesson_name=new_lesson_list[i],
                    )
                messages.warning(request, "Record Updated Successfully")
                return HttpResponseRedirect("/lesson")
            context = {
                "record": record,
                "lesson": "active",
                "class_records": class_records,
                "records": records,
            }
            return render(request, "Lesson_plan/lesson_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def lesson_view(request, sub):
    if request.user.is_superuser or "lesson_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            records = Lesson.objects.all().order_by("subject")
            record = Lesson.objects.filter(subject=sub).order_by("subject")
            context = {
                "record": record,
                "lesson": "active",
                "view": True,
                "class_records": class_records,
                "records": records,
            }
            return render(request, "Lesson_plan/lesson_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def lesson_delete(request, pk):
    if request.user.is_superuser or "lesson_edit" in request.permissions:
        try:
            data = Lesson.objects.get(id=pk)
            sub = data.subject.id
            data.delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect(f"/lesson_edit/{sub}")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def lesson_bulk_delete(request, sub):
    Lesson.objects.filter(subject=sub).delete()
    return HttpResponseRedirect("/lesson")


@login_required
@user_type_required("Staff")
def topicc(request):
    if (
        request.user.is_superuser
        or "topic_view" in request.permissions
        or "topic_add" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            records = topic.objects.all().order_by("lesson_name")
            if request.method == "POST":
                classs = request.POST.get("Class")
                section = request.POST.get("section")
                subject_groups = request.POST.get("subject_group")
                subject = request.POST.get("subject")
                lesson = request.POST.get("lesson")
                topic_list = request.POST.getlist("topic_name")
                for i in range(len(topic_list)):
                    topic.objects.get_or_create(
                        Class_id=classs,
                        section_id=section,
                        subject_group_id=subject_groups,
                        subject_id=subject,
                        lesson_name_id=lesson,
                        topic_name=topic_list[i],
                    )
                return HttpResponseRedirect("/topicc")
            context = {
                "records": records,
                "topicc": "active",
                "class_records": class_records,
            }
            return render(request, "Lesson_plan/topicc.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def topicc_edit(request, pk):
    if request.user.is_superuser or "topic_edit" in request.permissions:
        try:
            class_records = Class.objects.all()
            records = topic.objects.filter(lesson_name=pk)
            if request.method == "POST":
                classs = request.POST.get("Class")
                section = request.POST.get("section")
                subject_groups = request.POST.get("subject_group")
                subject = request.POST.get("subject")
                lesson = request.POST.get("lesson")
                topic_list = request.POST.getlist("topic_name")
                ids = request.POST.getlist("ids")
                new_topic_list = request.POST.getlist("new_topic_name")
                for i in range(len(topic_list)):
                    obj = topic.objects.get(id=ids[i])
                    obj.Class_id = classs
                    obj.section_id = section
                    obj.subject_group_id = subject_groups
                    obj.subject_id = subject
                    obj.lesson_name_id = lesson
                    obj.topic_name = topic_list[i]
                for i in range(len(new_topic_list)):
                    topic.objects.get_or_create(
                        Class_id=classs,
                        section_id=section,
                        subject_group_id=subject_groups,
                        subject_id=subject,
                        lesson_name_id=lesson,
                        topic_name=new_topic_list[i],
                    )
                return HttpResponseRedirect("/topicc")
            context = {
                "records": records,
                "topicc": "active",
                "class_records": class_records,
            }
            return render(request, "Lesson_plan/topicc_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def topicc_view(request, pk):
    if request.user.is_superuser or "topic_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            records = topic.objects.filter(lesson_name=pk)
            context = {
                "records": records,
                "topic": "active",
                "view": True,
                "class_records": class_records,
            }
            return render(request, "Lesson_plan/topicc_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def topicc_delete(request, pk):
    if request.user.is_superuser or "topic_edit" in request.permissions:
        try:
            data = topic.objects.get(id=pk)
            pk = data.lesson_name.id
            data.delete()
            return HttpResponseRedirect(f"/topicc_edit/{pk}")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def topic_bulk_delete(request, pk):
    if request.user.is_superuser or "topic_delete" in request.permissions:
        try:
            topic.objects.filter(lesson_name=pk).delete()
            return HttpResponseRedirect("/topicc")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Academics


@login_required
@user_type_required("Staff")
def promote_students(request):
    class_records = Class.objects.all()
    # PromoteStudent.objects.all().delete()
    session_records = Session.objects.all()
    if request.POST.get("search") == "search":
        classs = request.POST.get("class")
        section = request.POST.get("section")
        filters = {}
        if classs:
            filters["Class"] = classs
        if section:
            filters["section"] = section
        records = StudentAdmission.objects.filter(**filters, session=request.Session)
        print("records", records)
        student_list = []
        for stu in records:
            attendance_records = StudentAttendance.objects.filter(student_id=stu).last()
            if attendance_records:
                student_list.append([attendance_records, "1"])
            else:
                student_list.append([stu, "0"])
        context = {
            "promote_students": "active",
            "records": records,
            "class_records": class_records,
            "student_list": student_list,
            "session_records": session_records,
        }
        return render(request, "Academics/promote_students.html", context)
    if request.POST.get("all_save") == "all_save":
        student_id = request.POST.getlist("student_id")
        for data in student_id:
            if request.POST.get(f"next_session_status{data}") == "continue":
                promoto_student = PromoteStudent.objects.filter(
                    student=data, session=request.POST.get("session")
                ).last()

                if not promoto_student:
                    PromoteStudent.objects.get_or_create(
                        student_id=data,
                        Class_id=request.POST.get("class"),
                        section_id=request.POST.get("section"),
                        session_id=request.POST.get("session"),
                        currrent_result=request.POST.get(f"current_result{data}"),
                        next_session_status=request.POST.get(
                            f"next_session_status{data}"
                        ),
                    )
                    obj = StudentAdmission.objects.get(id=data)
                    StudentAdmission.objects.get_or_create(
                        admission_no=obj.admission_no,
                        roll_number=obj.roll_number,
                        Class_id=request.POST.get("class"),
                        section_id=request.POST.get("section"),
                        first_name=obj.first_name,
                        last_name=obj.last_name,
                        gender=obj.gender,
                        date_of_birth=obj.date_of_birth,
                        category=obj.category,
                        religion=obj.religion,
                        Caste=obj.Caste,
                        mobile_number=obj.mobile_number,
                        email=obj.email,
                        admission_date=obj.admission_date,
                        student_photo=obj.student_photo,
                        Blood_group=obj.Blood_group,
                        student_house=obj.student_house,
                        height=obj.height,
                        weight=obj.weight,
                        as_on_date=obj.as_on_date,
                        Father_name=obj.Father_name,
                        Father_phone=obj.Father_phone,
                        Father_occupation=obj.Father_occupation,
                        Father_photo=obj.Father_photo,
                        mother_photo=obj.mother_photo,
                        if_guardian_is=obj.if_guardian_is,
                        guardian_name=obj.guardian_name,
                        guardian_relation=obj.guardian_relation,
                        guardian_email=obj.guardian_email,
                        guardian_phone=obj.guardian_phone,
                        guardian_occupation=obj.guardian_occupation,
                        guardian_photo=obj.guardian_photo,
                        guardian_address=obj.guardian_address,
                        if_permanent_address_is_current_address=obj.if_permanent_address_is_current_address,
                        current_address=obj.current_address,
                        permanent_address=obj.permanent_address,
                        vehicle_number=obj.vehicle_number,
                        route_list=obj.route_list,
                        hostel=obj.hostel,
                        room_number=obj.room_number,
                        bank_account_number=obj.bank_account_number,
                        bank_name=obj.bank_name,
                        ifsc_code=obj.ifsc_code,
                        national_identification_number=obj.national_identification_number,
                        local_identification_number=obj.local_identification_number,
                        rte=obj.rte,
                        previous_school_detail=obj.previous_school_detail,
                        note=obj.note,
                        title_1=obj.title_1,
                        documents_1=obj.documents_1,
                        title_2=obj.title_2,
                        documents_2=obj.documents_2,
                        title_3=obj.title_3,
                        documents_3=obj.documents_3,
                        title_4=obj.title_4,
                        documents_4=obj.documents_4,
                        disable_date=obj.disable_date,
                        diable_reson=obj.diable_reson,
                        disable_note=obj.disable_note,
                        status=obj.status,
                        session_id=request.POST.get("session"),
                        user_student=obj.user_student,
                        user_parent=obj.user_parent,
                        created_by=obj.created_by,
                        created_at=obj.created_at,
                    )
        return redirect("promote_students")
    context = {"promote_students": "active", "class_records": class_records}
    return render(request, "Academics/promote_students.html", context)


# assign class teacher
@login_required
@user_type_required("Staff")
def assign_class_teacher(request):
    if (
        request.user.is_superuser
        or "assign_class_teacher_view" in request.permissions
        or "assign_class_teacher_add" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            class_teacher = AddStaff.objects.all()
            records = AssignClassTeacher.objects.filter(session=request.Session)
            teacher = AddStaff.objects.filter(roles__name__icontains="teacher")
            form = AssignClassTeacherForm()
            if request.method == "POST":
                form = AssignClassTeacherForm(request.POST)
                if form.is_valid():
                    form.save()
                    obj = form.save(commit=False)
                    obj.session = request.Session
                    obj.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/assign_class_teacher")
            context = {
                "form": form,
                "records": records,
                "assign_class_teacher": "active",
                "teacher": teacher,
                "class_records": class_records,
                "class_teacher": class_teacher,
            }
            return render(request, "Academics/assign_class_teacher.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_class_teacher_edit(request, pk):
    if request.user.is_superuser or "assign_class_teacher_edit" in request.permissions:
        try:
            class_records = Class.objects.all()
            class_teacher = AddStaff.objects.all()
            records = AssignClassTeacher.objects.filter(session=request.Session)
            teacher = AddStaff.objects.filter(roles__name__icontains="teacher")
            record = AssignClassTeacher.objects.get(id=pk)
            lists = record.class_teacher.all()
            list = [data.id for data in lists]
            assign_teacher = record.class_teacher.all()
            form = AssignClassTeacherForm(instance=record)
            if request.method == "POST":
                form = AssignClassTeacherForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/assign_class_teacher")
            context = {
                "form": form,
                "records": records,
                "assign_class_teacher": "active",
                "teacher": teacher,
                "assign_teacher": assign_teacher,
                "edit": True,
                "list": list,
                "class_records": class_records,
                "class_teacher": class_teacher,
                "record": record,
            }
            return render(request, "Academics/assign_class_teacher.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_class_teacher_view(request, pk):
    if request.user.is_superuser or "assign_class_teacher_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            class_teacher = AddStaff.objects.all()
            records = AssignClassTeacher.objects.filter(session=request.Session)
            teacher = AddStaff.objects.filter(roles__name__icontains="teacher")
            record = AssignClassTeacher.objects.get(id=pk)
            lists = record.class_teacher.all()
            list = [data.id for data in lists]
            form = AssignClassTeacherForm(instance=record)
            assign_teacher = record.class_teacher.all()
            context = {
                "form": form,
                "AssignClassTeacher": "active",
                "view": True,
                "assign_teacher": assign_teacher,
                "teacher": teacher,
                "records": records,
                "class_records": class_records,
                "class_teacher": class_teacher,
                "list": list,
                "record": record,
            }
            return render(request, "Academics/assign_class_teacher.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_class_teacher_delete(request, pk):
    if (
        request.user.is_superuser
        or "assign_class_teacher_delete" in request.permissions
    ):
        try:
            AssignClassTeacher.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/assign_class_teacher")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# assign subject teacher
@login_required
@user_type_required("Staff")
def assign_subject_teacher(request):
    if (
        request.user.is_superuser
        or "assign_class_teacher_view" in request.permissions
        or "assign_class_teacher_add" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            class_teacher = AddStaff.objects.all()
            subject_records = Subjects.objects.all()
            records = AssignSubjectTeacher.objects.filter(session=request.Session)
            teacher = AddStaff.objects.filter(roles__name__icontains="teacher")
            form = AssignSubjectTeacherForm()
            if request.method == "POST":
                form = AssignSubjectTeacherForm(request.POST)
                if form.is_valid():
                    form.save()
                    obj = form.save(commit=False)
                    obj.session = request.Session
                    obj.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/assign_subject_teacher")
            context = {
                "form": form,
                "records": records,
                "assign_class_teacher": "active",
                "teacher": teacher,
                "class_records": class_records,
                "subject_records": subject_records,
                "class_teacher": class_teacher,
            }
            return render(request, "Academics/assign_subject_teacher.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_subject_teacher_edit(request, pk):
    if request.user.is_superuser or "assign_class_teacher_edit" in request.permissions:
        try:
            class_records = Class.objects.all()
            class_teacher = AddStaff.objects.all()
            records = AssignClassTeacher.objects.filter(session=request.Session)
            teacher = AddStaff.objects.filter(roles__name__icontains="teacher")
            record = AssignClassTeacher.objects.get(id=pk)
            lists = record.class_teacher.all()
            list = [data.id for data in lists]
            assign_teacher = record.class_teacher.all()
            form = AssignClassTeacherForm(instance=record)
            if request.method == "POST":
                form = AssignClassTeacherForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/assign_class_teacher")
            context = {
                "form": form,
                "records": records,
                "assign_class_teacher": "active",
                "teacher": teacher,
                "assign_teacher": assign_teacher,
                "edit": True,
                "list": list,
                "class_records": class_records,
                "class_teacher": class_teacher,
                "record": record,
            }
            return render(request, "Academics/assign_class_teacher.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_subject_teacher_view(request, pk):
    if request.user.is_superuser or "assign_class_teacher_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            class_teacher = AddStaff.objects.all()
            records = AssignClassTeacher.objects.filter(session=request.Session)
            teacher = AddStaff.objects.filter(roles__name__icontains="teacher")
            record = AssignClassTeacher.objects.get(id=pk)
            lists = record.class_teacher.all()
            list = [data.id for data in lists]
            form = AssignClassTeacherForm(instance=record)
            assign_teacher = record.class_teacher.all()
            context = {
                "form": form,
                "AssignClassTeacher": "active",
                "view": True,
                "assign_teacher": assign_teacher,
                "teacher": teacher,
                "records": records,
                "class_records": class_records,
                "class_teacher": class_teacher,
                "list": list,
                "record": record,
            }
            return render(request, "Academics/assign_class_teacher.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_subject_teacher_delete(request, pk):
    if (
        request.user.is_superuser
        or "assign_class_teacher_delete" in request.permissions
    ):
        try:
            AssignClassTeacher.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/assign_class_teacher")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
def section_js(request):
    class_id = request.GET.get("class_id")
    classs = Class.objects.get(id=class_id)
    section = classs.section.all()
    return JsonResponse(data=list(section.values("id", "section_name")), safe=False)


def demo_js(request):
    # record=AddStaff.objects.get(id=pk)
    role_id = request.GET.get("role_id")
    classs = AddStaff.objects.filter(roles=role_id)
    return JsonResponse(
        data=list(classs.values("id", "first_name", "staff_id")), safe=False
    )


@login_required
def subject_grp_js(request):
    classs = request.GET.get("class_id")
    suction_id = request.GET.get("section_id")
    subjectt = SubjectGroup.objects.filter(Class_id=classs, section_id=suction_id)
    return JsonResponse(data=list(subjectt.values("id", "name")), safe=False)


@login_required
def subject_js(request):
    classs = request.GET.get("class_id")
    suction_id = request.GET.get("section_id")
    subject_grp = request.GET.get("subject_grp_id")
    subjectss = SubjectGroup.objects.get(
        Class_id=classs, section_id=suction_id, id=subject_grp
    )
    subjecttt = subjectss.subject.all()
    return JsonResponse(data=list(subjecttt.values("id", "subject_name")), safe=False)


@login_required
def topic_js(request):
    classs = request.GET.get("class_id")
    suction_id = request.GET.get("section_id")
    subject_grp = request.GET.get("subject_grp_id")
    subjectt = request.GET.get("subject")
    subject = Lesson.objects.filter(
        Class_id=classs,
        section_id=suction_id,
        subject_group_id=subject_grp,
        subject_id=subjectt,
    )


@login_required
def student_report_js(request):
    classs = request.GET.get("class_id")
    suction_id = request.GET.get("section_id")
    category = request.GET.get("id_category")
    gender = request.GET.get("id_gender")
    subject = StudentAdmission.objects.filter(
        Class_id=classs, section_id=suction_id, category_id=category, gender_id=gender
    )
    return JsonResponse(data=list(subject.values("id", "rte")), safe=False)


@login_required
def leave_type_js(request):
    name = request.GET.get("name")
    leaves = StaffLeave.objects.filter(staff=name)
    available_leaves = AvailableLeave.objects.filter(
        staff_leave__in=leaves.values("id"), session=request.Session
    )
    if not available_leaves:
        for data in leaves:
            AvailableLeave.objects.get_or_create(
                staff_leave=data,
                available_leave=data.total_leave,
                total_leave=data.total_leave,
                session=request.Session,
            )
    record = available_leaves.filter(available_leave__gt=0)
    return JsonResponse(
        data=list(
            record.values(
                "staff_leave__leave_type_id",
                "staff_leave__leave_type__name",
                "available_leave",
            )
        ),
        safe=False,
    )


@login_required
@user_type_required("Staff")
def class_timetable_view(request):
    if (
        request.user.is_superuser
        or "class_time_table_view" in request.permissions
        or "class_time_table_edit" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                TimeTable_records = TimeTable.objects.filter(
                    Class=classs, section=section, session=request.Session
                )

                context = {
                    "class_records": class_records,
                    "section_records": section_records,
                    "classs": int(classs),
                    "section": int(section),
                    "TimeTable_records": TimeTable_records,
                    "class_timetablee": "active",
                }
                return render(request, "Academics/class_timetable_view.html", context)
            context = {
                "class_records": class_records,
                "section_records": section_records,
                "class_timetablee": "active",
            }
            return render(request, "Academics/class_timetable_view.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def class_timetable(request):
    if (
        request.user.is_superuser
        or "class_time_table_view" in request.permissions
        or "class_time_table_edit" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            subject_group_records = SubjectGroup.objects.all()
            if request.POST.get("search") == "search":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                subject_group = request.POST.get("subject_group")
                section_records = Section.objects.all()
                subject_group_record = SubjectGroup.objects.get(id=subject_group)
                subject_records = Subjects.objects.filter(
                    id__in=subject_group_record.subject.all()
                )
                assign_teacher = AssignClassTeacher.objects.filter(
                    Class=classs, section=section, session=request.Session
                ).last()
                print("assign_teacher", assign_teacher)
                teacher_records = assign_teacher.class_teacher.all()
                print("teacher_records", teacher_records)
                TimeTable_records = TimeTable.objects.filter(
                    Class=classs,
                    section=section,
                    subject_group=subject_group,
                    session=request.Session,
                )
                context = {
                    "class_records": class_records,
                    "class_timetablee": "active",
                    "subject_group_records": subject_group_records,
                    "subject_records": subject_records,
                    "teacher_records": teacher_records,
                    "classs": int(classs),
                    "section": int(section),
                    "subject_group": int(subject_group),
                    "TimeTable_records": TimeTable_records,
                    "section_records": section_records,
                }
                return render(request, "Academics/class_timetable.html", context)
            context = {
                "class_records": class_records,
                "class_timetablee": "active",
                "subject_group_records": subject_group_records,
            }
            return render(request, "Academics/class_timetable.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
def timetable_save_js(request):
    subject_list = request.GET.getlist("subject[]")
    teacher_list = request.GET.getlist("teacher[]")
    from_time_list = request.GET.getlist("from_time[]")
    to_time_list = request.GET.getlist("to_time[]")
    room_nolist = request.GET.getlist("room_no[]")
    class_list = request.GET.get("class")
    section_list = request.GET.get("section")
    subject_groups_list = request.GET.get("subject_group")
    day = request.GET.get("day")
    for i in range(len(subject_list)):
        TimeTable.objects.get_or_create(
            Class_id=class_list,
            section_id=section_list,
            subject_group_id=subject_groups_list,
            subject_id=subject_list[i],
            teacher_id=teacher_list[i],
            time_from=from_time_list[i],
            time_to=to_time_list[i],
            room_no=room_nolist[i],
            day=day,
            session=request.Session,
        )
    return JsonResponse(data="success", safe=False)


@login_required
@user_type_required("Staff")
def timetable_delete(request):
    TimeTable.objects.get(id=request.GET.get("pk")).delete()
    return JsonResponse(data="success", safe=False)


@login_required
@user_type_required("Staff")
def teacher_timetable(request):
    teacher_records = AddStaff.objects.filter(roles__name__icontains="teacher")
    if request.method == "POST":
        teacher = request.POST.get("teacher")
        TimeTable_records = TimeTable.objects.filter(
            teacher=teacher, session=request.Session
        )

        context = {
            "teacher_records": teacher_records,
            "teacher": int(teacher),
            "TimeTable_records": TimeTable_records,
            "teacher_timetable": "active",
        }
        return render(request, "Academics/teacher_timetable.html", context)
    context = {"teacher_records": teacher_records, "teacher_timetable": "active"}
    return render(request, "Academics/teacher_timetable.html", context)


#  HR


@login_required
@user_type_required("Staff")
def add_staff(request):
    if request.user.is_superuser or "staff_add" in request.permissions:
        try:
            system_fields = SystemFields.objects.all()
            system_field = (
                system_fields.last().staff_fields if system_fields.last() else None
            )
            custom_fields = CustomFields.objects.filter(field_belongs_to="Staff")
            staffs = AddStaff.objects.all()
            leave_type = AddLeaveType.objects.all()
            form = AddStaffForm()
            if request.method == "POST":
                form = AddStaffForm(request.POST)
                if form.is_valid():
                    staff = form.save(commit=False)
                    staff.save()
                    password = generate_password()
                    if staff.last_name:
                        last_name = staff.last_name
                    else:
                        last_name = " "
                    user = User.objects.create_user(
                        username=staff.email,
                        email=staff.email,
                        first_name=staff.first_name,
                        last_name=last_name,
                        dob=staff.date_of_birth,
                        phone_number=staff.phone_no,
                        user_type="Staff",
                    )
                    user.set_password(password)
                    print(password)
                    user.save()
                    staff.user = user
                    staff.created_by = request.user
                    staff.save()
                    staff_leave = AddLeaveType.objects.all()

                    for data in staff_leave:
                        leave_count = request.POST.get(data.name)
                        if leave_count:
                            StaffLeave.objects.create(
                                staff_id=staff.pk,
                                leave_type=data,
                                total_leave=leave_count,
                            )

                    recipient_name = staff.first_name
                    to = staff.email
                    new_staff_account_email(recipient_name, to, password)
                    #  customs fields
                    for data in custom_fields:
                        if data.field_type == "multiselect":
                            value = request.POST.getlist(f"{data.field_name}")
                        else:
                            value = request.POST.get(f"{data.field_name}")
                        print(value)
                        if value:
                            print("===========", value)
                            StaffCustomFieldValues.objects.create(
                                field=data, staff_id=staff.pk, value=value
                            )
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/add_staff")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "staffs": staffs,
                "add_staff": "active",
                "view": True,
                "leave_type": leave_type,
                "custom_fields": custom_fields,
                "system_fields": system_field,
            }
            return render(request, "Human_Resource/add_staff.html", context)

        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def approve_leave_request(request):
    if (
        request.user.is_superuser
        or "approve_leave_request_view" in request.permissions
        or "approve_leave_request_add" in request.permissions
    ):
        try:
            records = ApproveLeave.objects.all()
            roles_records = Role.objects.all()
            if request.method == "POST":
                lop = int(request.POST.get("lop"))
                dates_str = request.POST.get("dates")
                leave_dates = dates_str.split(", ")
                leave_type = request.POST.get("available_leave")
                if lop:
                    leave_days = len(leave_dates) - lop
                    if leave_type:
                        lop_dates = leave_dates[leave_days:]
                    else:
                        lop_dates = leave_dates
                else:
                    leave_days = len(leave_dates)
                    lop_dates = []

                ApproveLeave.objects.create(
                    role_id=request.POST.get("role"),
                    name_id=request.POST.get("staff"),
                    apply_date=request.POST.get("apply_date"),
                    leave_type_id=request.POST.get("available_leave"),
                    leave_dates=leave_dates[:leave_days],
                    number_of_days=leave_days,
                    LOP_leave_dates=lop_dates,
                    LOP_number_of_days=lop,
                    reason=request.POST.get("reason"),
                    note=request.POST.get("notes"),
                    attach_document=request.FILES.get("document"),
                    status=request.POST.get("status"),
                    created_by=request.user,
                )
                available_leave = AvailableLeave.objects.filter(
                    staff_leave__leave_type=request.POST.get("available_leave"),
                    session=request.Session,
                ).last()
                available_leave.available_leave = (
                    available_leave.available_leave - leave_days
                )
                available_leave.save()
                return redirect("approve_leave_request")

            context = {
                "approve_leave_request": "active",
                "records": records,
                "roles_records": roles_records,
            }
            return render(request, "Human_Resource/approve_leave_request.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def approve_leave_request_edit(request, pk):
    if request.user.is_superuser or "approve_leave_request_edit" in request.permissions:
        try:
            records = ApproveLeave.objects.all()
            record = ApproveLeave.objects.get(id=pk)
            if request.method == "POST":
                record.status = request.POST.get("status")
                record.save()
                return HttpResponseRedirect("/approve_leave_request")
            context = {
                "records": records,
                "approve_leave_request": "active",
                "record": record,
                "edit": True,
            }
            return render(
                request, "Human_Resource/approve_leave_request_edit.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def approve_leave_request_delete(request, pk):
    if (
        request.user.is_superuser
        or "approve_leave_request_delete" in request.permissions
    ):
        try:
            ApproveLeave.objects.get(id=pk).delete()
            return HttpResponseRedirect("/approve_leave_request")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# apply leave


@login_required
@user_type_required("Staff")
def apply_leave(request):
    if (
        request.user.is_superuser
        or "apply_leave_view" in request.permissions
        or "apply_leave_add" in request.permissions
    ):
        if True:
            staff = AddStaff.objects.get(user=request.user)
            leaves = StaffLeave.objects.filter(staff=staff)
            available_leaves = AvailableLeave.objects.filter(
                staff_leave__in=leaves.values("id"), session=request.Session
            )
            if not available_leaves:
                for data in leaves:
                    AvailableLeave.objects.get_or_create(
                        staff_leave=data,
                        available_leave=data.total_leave,
                        total_leave=data.total_leave,
                        session=request.Session,
                    )
            approval_leaves = ApproveLeave.objects.filter(name=staff)
            if request.method == "POST":
                lop = int(request.POST.get("lop"))
                dates_str = request.POST.get("dates")
                leave_dates = dates_str.split(", ")
                leave_type = request.POST.get("available_leave")
                if lop:
                    leave_days = len(leave_dates) - lop
                    if leave_type:
                        lop_dates = leave_dates[leave_days:]
                    else:
                        lop_dates = leave_dates
                else:
                    leave_days = len(leave_dates)
                    lop_dates = []

                ApproveLeave.objects.create(
                    role=staff.roles,
                    name=staff,
                    apply_date=request.POST.get("apply_date"),
                    leave_type_id=request.POST.get("available_leave"),
                    leave_dates=leave_dates[:leave_days],
                    number_of_days=leave_days,
                    LOP_leave_dates=lop_dates,
                    LOP_number_of_days=lop,
                    reason=request.POST.get("reason"),
                    note=" ",
                    attach_document=request.FILES.get("document"),
                    status="Pending",
                    created_by=request.user,
                )
                available_leave = AvailableLeave.objects.filter(
                    staff_leave__leave_type=request.POST.get("available_leave"),
                    session=request.Session,
                ).last()
                available_leave.available_leave = (
                    available_leave.available_leave - leave_days
                )
                available_leave.save()
                return redirect("apply_leave")

            context = {
                "leaves": leaves,
                "apply_leave": "active",
                "available_leaves": available_leaves.filter(available_leave__gt=0),
                "approval_leaves": approval_leaves,
            }
            return render(request, "Human_Resource/apply_leave.html", context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def apply_leave_edit(request, pk):
    if request.user.is_superuser or "apply_leave_edit" in request.permissions:
        try:
            records = ApplyLeave.objects.all()
            record = ApplyLeave.objects.get(id=pk)
            form = ApplyLeaveForm(instance=record)
            if request.method == "POST":
                form = ApplyLeaveForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/apply_leave")
            context = {"form": form, "leaves": records, "apply_leave": "active"}
            return render(request, "Human_Resource/apply_leave_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def apply_leave_delete(request, pk):
    if request.user.is_superuser or "apply_leave_delete" in request.permissions:
        try:
            ApproveLeave.objects.get(id=pk).delete()
            return HttpResponseRedirect("/apply_leave")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_leave_type(request):
    if (
        request.user.is_superuser
        or "leave_types_view" in request.permissions
        or "leave_types_add" in request.permissions
    ):
        try:
            form = AddLeaveTypeForm()
            leaves = AddLeaveType.objects.all()
            if request.method == "POST":
                form = AddLeaveTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("add_leave_type")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("add_leave_type")
            context = {
                "form": form,
                "leaves": leaves,
                "add_leave_type": "active",
            }
            return render(request, "Human_Resource/add_leave_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_leave_type_edit(request, pk):
    if request.user.is_superuser or "leave_types_edit" in request.permissions:
        try:
            leaves = AddLeaveType.objects.all()
            record = AddLeaveType.objects.get(id=pk)
            form = AddLeaveTypeForm(instance=record)
            if request.method == "POST":
                form = AddLeaveTypeForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_leave_type")
            context = {
                "form": form,
                "leaves": leaves,
                "add_leave_type": "active",
                "edit": True,
            }
            return render(request, "Human_Resource/add_leave_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_leave_type_delete(request, pk):
    if request.user.is_superuser or "leave_types_delete" in request.permissions:
        try:
            AddLeaveType.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_leave_type")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def teachers_rating_list(request):
    if request.user.is_superuser or "teacher_reating_view" in request.permissions:
        try:
            records = TeacherRating.objects.all()
            context = {"teachers_rating_list": "active", "records": records}
            return render(request, "Human_Resource/teachers_rating_list.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def teacher_rating_approval(request, pk):
    obj = TeacherRating.objects.get(id=pk)
    obj.status = "approval"
    obj.save()
    return redirect("teachers_rating_list")


@login_required
@user_type_required("Staff")
def teacher_rating_delete(request, pk):
    obj = TeacherRating.objects.get(id=pk).delete()
    return redirect("teachers_rating_list")


# department
@login_required
@user_type_required("Staff")
def department(request):
    if (
        request.user.is_superuser
        or "department_view" in request.permissions
        or "department_add" in request.permissions
    ):
        try:
            form = DepartmentForm()
            departments = Department.objects.all()
            if request.method == "POST":
                form = DepartmentForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("department")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("department")
            context = {"form": form, "departments": departments, "department": "active"}
            return render(request, "Human_Resource/department.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def department_edit(request, pk):
    if request.user.is_superuser or "department_edit" in request.permissions:
        try:
            departments = Department.objects.all()
            department = Department.objects.get(id=pk)
            form = DepartmentForm(instance=department)
            if request.method == "POST":
                form = DepartmentForm(request.POST, instance=department)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/department")
            context = {
                "form": form,
                "departments": departments,
                "department": "active",
                "edit": True,
            }
            return render(request, "Human_Resource/department_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def department_delete(request, pk):
    if request.user.is_superuser or "department_delete" in request.permissions:
        try:
            department = Department.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("department", {"department": department})
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# company
@login_required
@user_type_required("Staff")
def company(request):
    if (
        request.user.is_superuser
        or "company_view" in request.permissions
        or "company_add" in request.permissions
    ):
        try:
            form = CompanyForm()
            companys = Company.objects.all()
            if request.method == "POST":
                form = CompanyForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("company")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("company")
            context = {"form": form, "companys": companys, "company": "active"}
            return render(request, "Structure/company.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def company_edit(request, pk):
    if request.user.is_superuser or "company_edit" in request.permissions:
        try:
            companys = Company.objects.all()
            company = Company.objects.get(id=pk)
            form = CompanyForm(instance=company)
            if request.method == "POST":
                form = CompanyForm(request.POST, instance=company)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/company")
            context = {
                "form": form,
                "companys": companys,
                "company": "active",
                "edit": True,
            }
            return render(request, "Structure/company_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def company_delete(request, pk):
    if request.user.is_superuser or "company_delete" in request.permissions:
        try:
            company = Company.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/company", {"company": company})
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# curriculum
@login_required
@user_type_required("Staff")
def curriculums(request):
    if (
        request.user.is_superuser
        or "curriculum_view" in request.permissions
        or "curriculum_add" in request.permissions
    ):
        try:
            form = CurriculumForm()
            curriculums = Curriculum.objects.all()
            if request.method == "POST":
                form = CurriculumForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("curriculums")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("curriculums")
            context = {"form": form, "curriculums": curriculums, "curriculum": "active"}
            return render(request, "Structure/curriculum.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def curriculum_edit(request, pk):
    if request.user.is_superuser or "curriculum_edit" in request.permissions:
        try:
            curriculums = Curriculum.objects.all()
            curriculum = Curriculum.objects.get(id=pk)
            form = CurriculumForm(instance=department)
            if request.method == "POST":
                form = CurriculumForm(request.POST, instance=department)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/curriculums")
            context = {
                "form": form,
                "curriculums": curriculums,
                "curriculum": "active",
                "edit": True,
            }
            return render(request, "Structure/curriculum.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def curriculum_delete(request, pk):
    if request.user.is_superuser or "department_delete" in request.permissions:
        try:
            department = Department.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("department", {"department": department})
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def designation(request):
    if (
        request.user.is_superuser
        or "designation_view" in request.permissions
        or "designation_add" in request.permissions
    ):
        try:
            form = DesignationForm()
            designations = Designation.objects.all()
            if request.method == "POST":
                form = DesignationForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("designation")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("designation")
            context = {
                "form": form,
                "designations": designations,
                "designation": "active",
            }
            return render(request, "Human_Resource/designation.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def designation_edit(request, pk):
    if request.user.is_superuser or "designation_edit" in request.permissions:
        try:
            designations = Designation.objects.all()
            designation = Designation.objects.get(id=pk)
            form = DesignationForm(instance=designation)
            if request.method == "POST":
                form = DesignationForm(request.POST, instance=designation)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/designation")
            context = {
                "form": form,
                "designations": designations,
                "designation": "active",
                "edit": True,
            }
            return render(request, "Human_Resource/designation.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def designation_delete(request, pk):
    if request.user.is_superuser or "designation_delete" in request.permissions:
        try:
            designation = Designation.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/designation", {"designation": designation})
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def notice_board(request):
    if (
        request.user.is_superuser
        or "notice_borad_view" in request.permissions
        or "notice_borad_add" in request.permissions
    ):
        try:
            form = noticeBoardForm()
            forms = Role.objects.all()
            notices = noticeBoard.objects.all()
            if request.method == "POST":
                titels = request.POST.get("title")
                notice_dates = request.POST.get("notice_date")
                massage = request.POST.get("message")
                publish = request.POST.get("publish_on")
                student = request.POST.getlist("noties_all")
                noticeBoard.objects.create(
                    title=titels,
                    notice_date=notice_dates,
                    message=massage,
                    publish_on=publish,
                    message_to=student,
                )
                messages.success(request, "Record Saved Successfully")
                return HttpResponseRedirect("/notice_board")
            context = {
                "form": form,
                "forms": forms,
                "records": notices,
                "notices": "active",
            }
            return render(request, "Communicate/notice_board.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def notice_board_edit(request, pk):
    if request.user.is_superuser or "notice_borad_edit" in request.permissions:
        try:
            notices = noticeBoard.objects.all()
            notice = noticeBoard.objects.get(id=pk)
            form = noticeBoardForm(instance=notice)
            if request.method == "POST":
                form = noticeBoardForm(request.POST, instance=notice)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/notice_board")
            context = {
                "form": form,
                "records": notices,
                "notices": "active",
                "edit": True,
            }
            return render(request, "Communicate/notice_board_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def notice_board_delete(request, pk):
    noticeBoard.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/notice_board")


@login_required
@user_type_required("Staff")
def email_sms_log(request):
    if request.user.is_superuser or "email_sms_log_view" in request.permissions:
        try:
            records = EmailSmsLog.objects.all()
            return render(
                request,
                "Communicate/email_sms_log.html",
                {"records": records, "email_sms_log": "active"},
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assignment_list(request):
    if request.user.is_superuser or "assigment_view" in request.permissions:
        try:
            records = UploadContent.objects.filter(content_type="assignments")
            context = {"records": records, "assignment_list": "active"}
            return render(request, "Download_center/assignment_list.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assignment_list_delete(request, pk):
    UploadContent.objects.get(id=pk).delete()
    return HttpResponseRedirect("/assignment_list")


@login_required
@user_type_required("Staff")
def study_material(request):
    records = UploadContent.objects.filter(content_type="study_material")
    context = {"records": records, "study_material": "active"}

    return render(request, "Download_center/study_material.html", context)


@login_required
@user_type_required("Staff")
def study_material_delete(request, pk):
    UploadContent.objects.get(id=pk).delete()
    return HttpResponseRedirect("/study_material")


@login_required
@user_type_required("Staff")
def syllabus(request):
    records = UploadContent.objects.filter(content_type="syllabus")
    context = {"records": records, "syllabus": "active"}
    return render(request, "Download_center/syllabus.html", context)


@login_required
@user_type_required("Staff")
def syllabus_delete(request, pk):
    UploadContent.objects.get(id=pk).delete()
    return HttpResponseRedirect("/syllabus")


@login_required
@user_type_required("Staff")
def other_download_list(request):
    records = UploadContent.objects.filter(content_type="other_download")
    context = {"records": records, "other_download_list": "active"}

    return render(request, "Download_center/other_download_list.html", context)


@login_required
@user_type_required("Staff")
def other_download_list_delete(request, pk):
    UploadContent.objects.get(id=pk).delete()
    return HttpResponseRedirect("/other_download_list")


@login_required
@user_type_required("Staff")  # Homework
def book_list(request):
    if (
        request.user.is_superuser
        or "books_list_view" in request.permissions
        or "books_list_add" in request.permissions
    ):
        try:
            form = AddBookForm()
            books = AddBook.objects.all()
            if request.method == "POST":
                form = AddBookForm(request.POST)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.available_qty = request.POST.get("qty")
                    data.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("book_list")
                else:
                    print(form.errors)
            context = {"form": form, "books": books, "book_list": "active"}
            return render(request, "Library/book_list.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def book_list_edit(request, pk):
    if request.user.is_superuser or "books_list_edit" in request.permissions:
        try:
            books = AddBook.objects.all()
            book = AddBook.objects.get(id=pk)
            form = AddBookForm(instance=book)
            if request.method == "POST":
                form = AddBookForm(request.POST, instance=book)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/book_list")
            context = {"form": form, "books": books, "book_list": "active"}
            return render(request, "Library/book_list_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def book_list_delete(request, pk):
    if "books_list_delete" in request.permissions or request.user.is_superuser:
        try:
            AddBook.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/book_list")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_staff_member(request):
    if "add_staff_member_view" in request.permissions or request.user.is_superuser:
        try:
            staff = AddStaff.objects.all()
            records = []
            for data in staff:
                dict = {}
                member = LibrayMember.objects.filter(
                    staff=data.id, status="active"
                ).last()
                if member:
                    dict["staff_id"] = None
                    dict["member_id"] = member.id
                    dict["library_card_no"] = member.library_card_no
                    dict["staff_name"] = (
                        member.staff.first_name + member.staff.first_name
                    )
                    dict["email"] = member.staff.email
                    dict["date_of_birth"] = member.staff.date_of_birth
                    dict["phone_no"] = member.staff.phone_no
                else:
                    dict["staff_id"] = data.id
                    dict["member_id"] = " "
                    dict["library_card_no"] = " "
                    dict["staff_name"] = data.first_name + data.first_name
                    dict["email"] = data.email
                    dict["date_of_birth"] = data.date_of_birth
                    dict["phone_no"] = data.phone_no
                records.append(dict)
            if request.method == "POST":
                staff_id = request.POST.get("staff_id")
                card_no = request.POST.get("card_no")
                staff = AddStaff.objects.get(id=staff_id)
                LibrayMember.objects.create(
                    staff_id=staff.id,
                    library_card_no=card_no,
                    member_type="Staff",
                )
                return redirect("add_staff_member")
            context = {"records": records, "add_staff_member": "active"}
            return render(request, "Library/add_staff_member.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def libary_surrender_card(request, pk):
    data = LibrayMember.objects.get(id=pk)
    data.status = "deactive"
    data.save()
    return redirect("add_staff_member")


@login_required
@user_type_required("Staff")
def stu_libary_surrender_card(request, pk):
    data = LibrayMember.objects.get(id=pk)
    data.status = "deactive"
    data.save()
    return redirect("add_student_member")


@login_required
@user_type_required("Staff")
def add_student_member(request):
    if "add_student_view" in request.permissions or request.user.is_superuser:
        if True:
            class_records = Class.objects.all()
            if request.POST.get("search") == "search":
                student = StudentAdmission.objects.filter(
                    Class=request.POST.get("class"),
                    section=request.POST.get("section"),
                    session=request.Session,
                )
                records = []
                for data in student:
                    dict = {}
                    member = LibrayMember.objects.filter(
                        student=data.id, status="active"
                    ).last()
                    print("====", member)
                    if member:
                        dict["staff_id"] = None
                        dict["member_id"] = member.id
                        dict["library_card_no"] = member.library_card_no
                        dict["staff_name"] = (
                            member.student.first_name + " " + member.student.first_name
                        )
                        dict["email"] = member.student.email
                        dict["date_of_birth"] = member.student.date_of_birth
                        dict["phone_no"] = member.student.mobile_number
                    else:
                        dict["staff_id"] = data.id
                        dict["member_id"] = " "
                        dict["library_card_no"] = " "
                        dict["staff_name"] = data.first_name + " " + data.first_name
                        dict["email"] = data.email
                        dict["date_of_birth"] = data.date_of_birth
                        dict["phone_no"] = data.mobile_number
                    records.append(dict)
                print(records)
                context = {
                    "records": records,
                    "add_student_member": "active",
                    "class_records": class_records,
                }
                return render(request, "Library/add_student_member.html", context)
            if request.POST.get("save") == "save":
                staff_id = request.POST.get("staff_id")
                card_no = request.POST.get("card_no")
                staff = StudentAdmission.objects.get(id=staff_id)
                LibrayMember.objects.create(
                    student_id=staff.id,
                    library_card_no=card_no,
                    member_type="Student",
                )
                return redirect("add_student_member")
            context = {"add_student_member": "active", "class_records": class_records}
            return render(request, "Library/add_student_member.html", context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def book_issuse_return(request):
    if "issue_return_view" in request.permissions or request.user.is_superuser:
        try:
            records = LibrayMember.objects.filter(status="active")
            context = {"records": records, "book_issuse_return": "active"}
            return render(request, "Library/book_issuse_return.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def member_book_issued(request, pk):
    if "issue_return_view" in request.permissions or request.user.is_superuser:
        try:
            member = LibrayMember.objects.get(id=pk)
            book = AddBook.objects.all()
            issue_records = IssueBook.objects.filter(member=pk)
            if request.method == "POST":
                book_id = request.POST.get("book")
                IssueBook.objects.create(
                    book_id=book_id,
                    member_id=pk,
                    due_return_date=request.POST.get("return_date"),
                    status="Issued",
                )
                book = book.get(id=book_id)
                book.available_qty -= 1
                book.save()
                return HttpResponseRedirect(f"/member_book_issue/{pk}")
            context = {
                "book": book,
                "book_issuse_return": "active",
                "issue_records": issue_records,
                "member": member,
            }
            return render(request, "Library/member_book_issued.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def book_return(request, pk):
    if "issue_return_view" in request.permissions or request.user.is_superuser:
        try:
            book = AddBook.objects.get(id=request.POST.get("book_id"))
            book.available_qty += 1
            book.save()
            issue_records = IssueBook.objects.get(id=request.POST.get("issue_id"))
            issue_records.status = "Returned"
            issue_records.return_date = request.POST.get("return_date")
            issue_records.save()
            return HttpResponseRedirect(f"/member_book_issue/{pk}")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
def book_qty_js(request):
    book_id = request.GET.get("book_id")
    book = AddBook.objects.get(id=book_id)
    return JsonResponse(data=book.available_qty, safe=False)


@login_required
@user_type_required("Staff")  # Inventory
def issue_item(request):
    if (
        "issue_item_view" in request.permissions
        or "issue_item_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = IssueItem.objects.all()
            if request.method == "POST":
                issue = IssueItem.objects.get(id=request.POST.get("id"))
                issue.status = "retured"
                ItemReturn.objects.create(
                    return_date=request.POST.get("item_return_date"),
                    remark=request.POST.get("remark"),
                    item_category_id=issue.item_category.id,
                    item_id=issue.item.id,
                    quantity=request.POST.get("item_qty"),
                )
                stock = ItemStockDeatail.objects.filter(
                    item_category=issue.item_category.id, item=issue.item.id
                ).last()
                stock.available_quantity = stock.available_quantity + int(
                    request.POST.get("item_qty")
                )
                issue.save()
                stock.save()
                return HttpResponseRedirect("/issue_item")
            context = {"records": records, "issue_item": "active"}
            return render(request, "Inventory/issue_item.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
def item_js(request):
    cat_id = request.GET.get("cat_id")
    item_records = AddItem.objects.filter(item_category=cat_id)
    return JsonResponse(data=list(item_records.values("id", "item")), safe=False)


@login_required
def item_available_js(request):
    item_id = request.GET.get("item_id")
    item_records = ItemStockDeatail.objects.filter(item=item_id).last()
    return JsonResponse(data=item_records.available_quantity, safe=False)


@login_required
@user_type_required("Staff")
def add_issue_item(request):
    records = IssueItem.objects.all()
    form = IssueItemForm()
    if request.method == "POST":
        form = IssueItemForm(request.POST)
        if form.is_valid():
            item_records = ItemStockDeatail.objects.filter(
                item=request.POST.get("item")
            ).last()
            item_records.available_quantity = item_records.available_quantity - int(
                request.POST.get("quantity")
            )
            item_records.save()
            form.save()
            messages.success(request, "Record Saved Successfully")
            return HttpResponseRedirect("/issue_item")
    context = {"form": form, "records": records, "issue_item": "active"}
    return render(request, "Inventory/add_issue_item.html", context)


@login_required
@user_type_required("Staff")
def issue_item_delete(request, pk):
    if "issue_item_delete" in request.permissions or request.user.is_superuser:
        try:
            IssueItem.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/issue_item")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")  # You need to define user_type_required decorator
def non_returnable_items_view(request):
    if (
        "non_returnable_item_view" in request.permissions
        or "non_returnable_item_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = NonReturnableItem.objects.all()

            if request.method == "POST":
                # Handle POST request if needed
                pass

            # Check if the user has exceeded the maximum quantity within the fixed duration
            for record in records:
                total_quantity_issued = NonReturnableItem.objects.filter(
                    staff=record.staff,
                    item=record.item,
                    duration_in_days__gte=record.duration_in_days,  # Check within the fixed duration
                ).aggregate(Sum("max_quantity"))["max_quantity__sum"]

                if (
                    total_quantity_issued is not None
                    and total_quantity_issued >= record.max_quantity
                ):
                    # Add logic to handle the case where the maximum quantity is exceeded
                    # For example, you can set a flag and use it in the template to display a message.
                    record.exceeded_max_quantity = True
                else:
                    record.exceeded_max_quantity = False

            context = {"records": records, "non_returnable_item": "active"}
            return render(request, "Inventory/non_returnable_item.html", context)

        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_stock(request):
    if (
        "add_item_stock_view" in request.permissions
        or "add_item_stock_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = ItemStock.objects.all()
            form = ItemStockForm()
            if request.method == "POST":
                form = ItemStockForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    detail_stock = ItemStockDeatail.objects.filter(
                        item_category=request.POST.get("item_category"),
                        item=request.POST.get("item"),
                    ).last()
                    if detail_stock:
                        detail_stock.quantity = detail_stock.quantity + int(
                            request.POST.get("quantity")
                        )
                        detail_stock.available_quantity = (
                            detail_stock.available_quantity
                            + int(request.POST.get("quantity"))
                        )
                        detail_stock.save()
                    else:
                        detail_form = ItemStockDeatailForm(request.POST)
                        data = detail_form.save(commit=False)
                        data.available_quantity = request.POST.get("quantity")
                        data.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/add_item_stock")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "add_item_stock": "active"}
            return render(request, "Inventory/add_item_stock.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_stock_edit(request, pk):
    if "add_item_stock_edit" in request.permissions or request.user.is_superuser:
        try:
            records = ItemStock.objects.all()
            record = ItemStock.objects.get(id=pk)
            form = ItemStockForm(instance=record)
            if request.method == "POST":
                form = ItemStockForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_item_stock")
            context = {
                "form": form,
                "records": records,
                "add_item_stock": "active",
                "edit": True,
            }
            return render(request, "Inventory/add_item_stock_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_stock_delete(request, pk):
    if "add_item_stock_delete" in request.permissions or request.user.is_superuser:
        try:
            record = ItemStock.objects.get(id=pk)
            detail_stock = ItemStockDeatail.objects.get(
                item_category=record.item_category.id, item=record.item.id
            )
            if detail_stock:
                detail_stock.quantity = detail_stock.quantity - record.quantity
                detail_stock.available_quantity = (
                    detail_stock.available_quantity - record.quantity
                )
                detail_stock.save()
            record.delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_item_stock")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")  # Assign To Raji
def add_item(request):
    if (
        "item_add_view" in request.permissions
        or "item_add_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = AddItem.objects.all()
            form = AddItemForm()
            if request.method == "POST":
                form = AddItemForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/add_item")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "add_item": "active"}
            return render(request, "Inventory/add_item.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_edit(request, pk):
    if "item_add_edit" in request.permissions or request.user.is_superuser:
        try:
            records = AddItem.objects.all()
            record = AddItem.objects.get(id=pk)
            form = AddItemForm(instance=record)
            if request.method == "POST":
                form = AddItemForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_item")
            context = {"form": form, "records": records, "add_item": "active"}
            return render(request, "Inventory/add_item.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_view(request, pk):
    if "item_add_view" in request.permissions or request.user.is_superuser:
        try:
            records = AddItem.objects.all()
            record = AddItem.objects.get(id=pk)
            form = AddItemForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "add_item": "active",
                "view": True,
            }
            return render(request, "Inventory/add_item.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_delete(request, pk):
    if "item_add_delete" in request.permissions or request.user.is_superuser:
        try:
            AddItem.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_item")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_category(request):
    if (
        "item_category_view" in request.permissions
        or "item_category_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = ItemCategory.objects.all()
            form = ItemCategoryForm()
            if request.method == "POST":
                form = ItemCategoryForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/add_item_category")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "add_item_category": "active"}
            return render(request, "Inventory/add_item_category.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_category_edit(request, pk):
    if "item_category_edit" in request.permissions or request.user.is_superuser:
        try:
            records = ItemCategory.objects.all()
            record = ItemCategory.objects.get(id=pk)
            form = ItemCategoryForm(instance=record)
            if request.method == "POST":
                form = ItemCategoryForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_item_category")
            context = {
                "form": form,
                "records": records,
                "add_item_category": "active",
                "edit": True,
            }
            return render(request, "Inventory/add_item_category.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_category_view(request, pk):
    if "item_category_view" in request.permissions or request.user.is_superuser:
        try:
            records = ItemCategory.objects.all()
            record = ItemCategory.objects.get(id=pk)
            form = ItemCategoryForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "add_item_category": "active",
                "view": True,
            }
            return render(request, "Inventory/add_item_category.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_item_category_delete(request, pk):
    if "item_category_delete" in request.permissions or request.user.is_superuser:
        try:
            ItemCategory.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_item_category")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def item_store(request):
    if (
        "item_store_view" in request.permissions
        or "item_store_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = ItemStore.objects.all()
            form = ItemStoreForm()
            if request.method == "POST":
                form = ItemStoreForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/item_store")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "item_store": "active"}
            return render(request, "Inventory/item_store.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def item_store_edit(request, pk):
    if "item_store_edit" in request.permissions or request.user.is_superuser:
        try:
            records = ItemStore.objects.all()
            record = ItemStore.objects.get(id=pk)
            form = ItemStoreForm(instance=record)
            if request.method == "POST":
                form = ItemStoreForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/item_store")
            context = {
                "form": form,
                "records": records,
                "item_store": "active",
                "edit": True,
            }
            return render(request, "Inventory/item_store.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def item_store_view(request, pk):
    if "item_store_view" in request.permissions or request.user.is_superuser:
        try:
            records = ItemStore.objects.all()
            record = ItemStore.objects.get(id=pk)
            form = ItemStoreForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "item_store": "active",
                "view": True,
            }
            return render(request, "Inventory/item_store.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def item_store_delete(request, pk):
    if "item_store_delete" in request.permissions or request.user.is_superuser:
        try:
            ItemStore.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/item_store")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def item_supplier(request):
    if (
        "item_supplier_view" in request.permissions
        or "item_supplier_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = ItemSupplier.objects.all()
            form = ItemSupplierForm()
            if request.method == "POST":
                form = ItemSupplierForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/item_supplier")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "item_supplier": "active"}
            return render(request, "Inventory/item_supplier.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def item_supplier_edit(request, pk):
    if "item_supplier_edit" in request.permissions or request.user.is_superuser:
        try:
            records = ItemSupplier.objects.all()
            record = ItemSupplier.objects.get(id=pk)
            form = ItemSupplierForm(instance=record)
            if request.method == "POST":
                form = ItemSupplierForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/item_supplier")
            context = {
                "form": form,
                "records": records,
                "item_supplier": "active",
                "edit": True,
            }
            return render(request, "Inventory/item_supplier.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def item_supplier_view(request, pk):
    if "item_supplier_view" in request.permissions or request.user.is_superuser:
        try:
            records = ItemSupplier.objects.all()
            record = ItemSupplier.objects.get(id=pk)
            form = ItemSupplierForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "item_supplier": "active",
                "view": True,
            }
            return render(request, "Inventory/item_supplier.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def item_supplier_delete(request, pk):
    if "item_supplier_delete" in request.permissions or request.user.is_superuser:
        try:
            ItemSupplier.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/item_supplier")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")  # Transport
def routes(request):
    if (
        request.user.is_superuser
        or "routes_view" in request.permissions
        or "routes_add" in request.permissions
    ):
        try:
            records = Route.objects.all()
            form = RouteForm()
            if request.method == "POST":
                form = RouteForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/routes")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "routes": "active"}
            return render(request, "Transport/routes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def routes_edit(request, pk):
    if request.user.is_superuser or "routes_edit" in request.permissions:
        try:
            records = Route.objects.all()
            record = Route.objects.get(id=pk)
            form = RouteForm(instance=record)
            if request.method == "POST":
                form = RouteForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/routes")
            context = {
                "form": form,
                "records": records,
                "routes": "active",
                "edit": True,
            }
            return render(request, "Transport/routes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def routes_view(request, pk):
    if request.user.is_superuser or "routes_view" in request.permissions:
        try:
            records = Route.objects.all()
            record = Route.objects.get(id=pk)
            form = RouteForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "routes": "active",
                "view": True,
            }
            return render(request, "Transport/routes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def routes_delete(request, pk):
    if request.user.is_superuser or "routes_delete" in request.permissions:
        try:
            Route.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/routes")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def vehicle(request):
    if (
        request.user.is_superuser
        or "vehicle_view" in request.permissions
        or "vehicle_add" in request.permissions
    ):
        try:
            records = Vehicle.objects.all()
            form = VehicleForm()
            if request.method == "POST":
                form = VehicleForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/vehicle")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "vehicle": "active"}
            return render(request, "Transport/vehicle.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def vehicle_edit(request, pk):
    if request.user.is_superuser or "vehicle_edit" in request.permissions:
        try:
            records = Vehicle.objects.all()
            record = Vehicle.objects.get(id=pk)
            form = VehicleForm(instance=record)
            if request.method == "POST":
                form = VehicleForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/vehicle")
            context = {
                "form": form,
                "records": records,
                "vehicle": "active",
                "edit": True,
            }
            return render(request, "Transport/vehicle.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def vehicle_view(request, pk):
    if request.user.is_superuser or "vehicle_view" in request.permissions:
        try:
            records = Vehicle.objects.all()
            record = Vehicle.objects.get(id=pk)
            form = VehicleForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "vehicle": "active",
                "view": True,
            }
            return render(request, "Transport/vehicle.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def vehicle_delete(request, pk):
    if request.user.is_superuser or "vehicle_delete" in request.permissions:
        try:
            Vehicle.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/vehicle")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_vehicle(request):
    if (
        request.user.is_superuser
        or "assign_vehicle_view" in request.permissions
        or "assign_vehicle_add" in request.permissions
    ):
        try:
            Route_name = Route.objects.all()
            vehicle_numbers = Vehicle.objects.all()
            records = AssignVehicle.objects.all()
            form = AssignVehicleForm()
            if request.method == "POST":
                form = AssignVehicleForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/assign_vehicle")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "assign_vehicle": "active",
                "vehicle_numbers": vehicle_numbers,
                "Route_name": Route_name,
            }
            return render(request, "Transport/assign_vehicle.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_vehicle_edit(request, pk):
    if request.user.is_superuser or "assign_vehicle_edit" in request.permissions:
        try:
            Route_name = Route.objects.all()
            records = AssignVehicle.objects.all()
            vehicle_numbers = Vehicle.objects.all()
            record = AssignVehicle.objects.get(id=pk)
            lists = record.vehicle.all()
            list = [data.id for data in lists]
            form = AssignVehicleForm(instance=record)
            if request.method == "POST":
                form = AssignVehicleForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/assign_vehicle")
            context = {
                "form": form,
                "records": records,
                "assign_vehicle": "active",
                "edit": True,
                "list": list,
                "record": record,
                "Route_name": Route_name,
                "vehicle_numbers": vehicle_numbers,
            }
            return render(request, "Transport/assign_vehicle.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_vehicle_view(request, pk):
    if request.user.is_superuser or "assign_vehicle_edit" in request.permissions:
        try:
            vehicle_numbers = Vehicle.objects.all()
            Route_name = Route.objects.all()
            records = AssignVehicle.objects.all()
            record = AssignVehicle.objects.get(id=pk)
            lists = record.vehicle.all()
            list = [data.id for data in lists]
            form = AssignVehicleForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "assign_vehicle": "active",
                "view": True,
                "record": record,
                "vehicle_numbers": vehicle_numbers,
                "Route_name": Route_name,
                "list": list,
            }
            return render(request, "Transport/assign_vehicle.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def assign_vehicle_delete(request, pk):
    if request.user.is_superuser or "assign_vehicle_edit" in request.permissions:
        try:
            AssignVehicle.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/assign_vehicle")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")  # Hostel
def hostel_room(request):
    if (
        "hostel_rooms_view" in request.permissions
        or "hostel_rooms_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = HostelRoom.objects.all()
            form = HostelRoomForm()
            if request.method == "POST":
                form = HostelRoomForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/hostel_room")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "hostel_room": "active"}
            return render(request, "Hostel/hostel_room.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def hostel_room_edit(request, pk):
    if request.user.is_superuser or "hostel_rooms_edit" in request.permissions:
        try:
            records = HostelRoom.objects.all()
            record = HostelRoom.objects.get(id=pk)
            form = HostelRoomForm(instance=record)
            if request.method == "POST":
                form = HostelRoomForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/hostel_room")
            context = {
                "form": form,
                "records": records,
                "hostel_room": "active",
                "edit": True,
            }
            return render(request, "Hostel/hostel_room.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def hostel_room_view(request, pk):
    if request.user.is_superuser or "hostel_rooms_view" in request.permissions:
        try:
            records = HostelRoom.objects.all()
            record = HostelRoom.objects.get(id=pk)
            form = HostelRoomForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "hostel_room": "active",
                "view": True,
            }
            return render(request, "Hostel/hostel_room.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def hostel_room_delete(request, pk):
    if request.user.is_superuser or "hostel_rooms_delete" in request.permissions:
        try:
            HostelRoom.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/hostel_room")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def room_type(request):
    if (
        "room_type_view" in request.permissions
        or "room_type_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = RoomType.objects.all()
            form = RoomTypeForm()
            if request.method == "POST":
                form = RoomTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/room_type")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "room_type": "active"}
            return render(request, "Hostel/room_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def room_type_edit(request, pk):
    if request.user.is_superuser or "room_type_edit" in request.permissions:
        try:
            records = RoomType.objects.all()
            record = RoomType.objects.get(id=pk)
            form = RoomTypeForm(instance=record)
            if request.method == "POST":
                form = RoomTypeForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/room_type")
            context = {
                "form": form,
                "records": records,
                "room_type": "active",
                "edit": True,
            }
            return render(request, "Hostel/room_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def room_type_view(request, pk):
    if request.user.is_superuser or "room_type_view" in request.permissions:
        try:
            records = RoomType.objects.all()
            record = RoomType.objects.get(id=pk)
            form = RoomTypeForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "room_type": "active",
                "view": True,
            }
            return render(request, "Hostel/room_type.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def room_type_delete(request, pk):
    if request.user.is_superuser or "room_type_delete" in request.permissions:
        try:
            RoomType.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/room_type")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def hostel(request):
    if (
        "hostel_view" in request.permissions
        or "hostel_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = Hostel.objects.all()
            form = HostelForm()
            if request.method == "POST":
                form = HostelForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/hostel")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "hostel": "active"}
            return render(request, "Hostel/hostel.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def hostel_edit(request, pk):
    if request.user.is_superuser or "hostel_edit" in request.permissions:
        try:
            records = Hostel.objects.all()
            record = Hostel.objects.get(id=pk)
            form = HostelForm(instance=record)
            if request.method == "POST":
                form = HostelForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/hostel")
            context = {
                "form": form,
                "records": records,
                "hostel": "active",
                "edit": True,
            }
            return render(request, "Hostel/hostel.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def hostel_view(request, pk):
    if request.user.is_superuser or "hostel_view" in request.permissions:
        try:
            records = Hostel.objects.all()
            record = Hostel.objects.get(id=pk)
            form = HostelForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "hostel": "active",
                "view": True,
            }
            return render(request, "Hostel/hostel.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def hostel_delete(request, pk):
    if request.user.is_superuser or "hostel_delete" in request.permissions:
        try:
            Hostel.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/hostel")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")  # Certificate
def student_certificate(request):
    if (
        request.user.is_superuser
        or "student_certificate_view" in request.permissions
        or "student_certificate_add" in request.permissions
    ):
        try:
            records = StudentCertificate.objects.all()
            form = StudentCertificateForm()
            if request.method == "POST":
                form = StudentCertificateForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/student_certificate")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "student_certificate": "active",
            }
            return render(request, "Certificate/student_certificate.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_certificate_edit(request, pk):
    if request.user.is_superuser or "student_certificate_edit" in request.permissions:
        try:
            records = StudentCertificate.objects.all()
            record = StudentCertificate.objects.get(id=pk)
            form = StudentCertificateForm(instance=record)
            if request.method == "POST":
                form = StudentCertificateForm(
                    request.POST, request.FILES, instance=record
                )
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/student_certificate")
            context = {
                "form": form,
                "records": records,
                "student_certificate": "active",
                "edit": True,
            }
            return render(request, "Certificate/student_certificate.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_certificate_view(request, pk):
    if request.user.is_superuser or "student_certificate_view" in request.permissions:
        try:
            records = StudentCertificate.objects.all()
            record = StudentCertificate.objects.get(id=pk)
            form = StudentCertificateForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "student_certificate": "active",
                "view": True,
            }
            return render(request, "Certificate/student_certificate.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_certificate_delete(request, pk):
    StudentCertificate.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/student_certificate")


@login_required
@user_type_required("Staff")
def student_id_card(request):
    if (
        request.user.is_superuser
        or "student_id_card_view" in request.permissions
        or "student_id_card_add" in request.permissions
    ):
        try:
            records = StudentId.objects.all()
            form = StudentIdForm()
            if request.method == "POST":
                form = StudentIdForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/student_id_card")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "student_id_card": "active"}
            return render(request, "Certificate/student_id_card.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_id_card_edit(request, pk):
    if request.user.is_superuser or "student_id_card_edit" in request.permissions:
        try:
            records = StudentId.objects.all()
            record = StudentId.objects.get(id=pk)
            form = StudentIdForm(instance=record)
            if request.method == "POST":
                form = StudentIdForm(request.POST, request.FILES, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/student_id_card")
            context = {
                "form": form,
                "records": records,
                "student_id_card": "active",
                "record": record,
                "edit": True,
            }
            return render(request, "Certificate/student_id_card.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_id_card_view(request, pk):
    if request.user.is_superuser or "student_id_card_view" in request.permissions:
        try:
            records = StudentId.objects.all()
            record = StudentId.objects.get(id=pk)
            form = StudentIdForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "student_id_card": "active",
                "view": True,
                "record": record,
            }
            return render(request, "Certificate/student_id_card.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_id_card_delete(request, pk):
    StudentId.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/student_id_card")


@login_required
@user_type_required("Staff")
def event_view(request, pk):
    records = Event.objects.all()
    record = Event.objects.get(id=pk)
    form = EventForm(instance=record)
    context = {"form": form, "records": records, "event": "active", "view": True}
    return render(request, "Front_cms/event_edit.html", context)


@login_required
@user_type_required("Staff")
def event_delete(request, pk):
    Event.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/event")


@login_required
@user_type_required("Staff")
def media_manager(request):
    records = MediaManager.objects.all()
    form = MediaManagerForm()
    if request.method == "POST":
        form = MediaManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/media_manager")
        else:
            print(form.errors)
    context = {"form": form, "records": records, "media_manager": "active"}
    return render(request, "Front_cms/media_manager.html", context)


@login_required
@user_type_required("Staff")
def media_manager_edit(request, pk):
    records = MediaManager.objects.all()
    record = MediaManager.objects.get(id=pk)
    form = MediaManagerForm(instance=record)
    if request.method == "POST":
        form = MediaManagerForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/media_manager")
    context = {"form": form, "records": records, "media_manager": "active"}
    return render(request, "Front_cms/media_manager_edit.html", context)


@login_required
@user_type_required("Staff")
def media_manager_view(request, pk):
    records = MediaManager.objects.all()
    record = MediaManager.objects.get(id=pk)
    form = MediaManagerForm(instance=record)
    context = {
        "form": form,
        "records": records,
        "media_manmenusager": "active",
        "view": True,
    }
    return render(request, "Front_cms/media_manager_edit.html", context)


@login_required
@user_type_required("Staff")
def media_manager_delete(request, pk):
    MediaManager.objects.get(id=pk).delete()
    return HttpResponseRedirect("/media_manager")


@login_required
@user_type_required("Staff")
def menus(request):
    records = Menu.objects.all()
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/menus")
        else:
            print(form.errors)
    context = {"form": form, "records": records, "menus": "active"}
    return render(request, "Front_cms/menus.html", context)


@login_required
@user_type_required("Staff")
def menus_edit(request, pk):
    records = Menu.objects.all()
    record = Menu.objects.get(id=pk)
    form = MenuForm(instance=record)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/menus")
    context = {"form": form, "records": records, "menus": "active"}
    return render(request, "Front_cms/menus_edit.html", context)


@login_required
@user_type_required("Staff")
def menus_view(request, pk):
    records = Menu.objects.all()
    record = Menu.objects.get(id=pk)
    form = MenuForm(instance=record)
    context = {"form": form, "records": records, "menus": "active", "view": True}
    return render(request, "Front_cms/menus_edit.html", context)


@login_required
@user_type_required("Staff")
def menus_delete(request, pk):
    Menu.objects.get(id=pk).delete()
    return HttpResponseRedirect("/menus")


@login_required
@user_type_required("Staff")
def alumni_events(request):
    if (
        "Alumni_events_view" in request.permissions
        or "Alumni_events_add" in request.permissions
        or request.user.is_superuser
    ):
        try:
            records = AlumniEvent.objects.all()
            form = AlumniEventForm()
            if request.method == "POST":
                form = AlumniEventForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")

                    return HttpResponseRedirect("/alumni_events")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "alumni_events": "active"}
            return render(request, "Alumni/alumni_events.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def alumni_events_add(request):
    if request.user.is_superuser or "Alumni_events_add" in request.permissions:
        try:
            form = AlumniEventForm()
            context = {
                "form": form,
            }
            return render(request, "Alumni/alumni_events_add.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def alumni_events_edit(request, pk):
    if (
        request.user.is_superuser
        or "Alumni_events_edit" in request.permissions
        or "Alumni_events_add" in request.permissions
    ):
        try:
            records = AlumniEvent.objects.all()
            record = AlumniEvent.objects.get(id=pk)
            form = AlumniEventForm(instance=record)
            if request.method == "POST":
                form = AlumniEventForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/alumni_events")
            context = {
                "form": form,
                "records": records,
                "alumni_events": "active",
                "record": record,
            }
            return render(request, "Alumni/alumni_events_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def alumni_events_view(request, pk):
    if request.user.is_superuser or "Alumni_events_view" in request.permissions:
        try:
            records = AlumniEvent.objects.all()
            record = AlumniEvent.objects.get(id=pk)
            form = AlumniEventForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "alumni_events": "active",
                "view": True,
            }
            return render(request, "Alumni/alumni_events_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def alumni_events_delete(request, pk):
    if request.user.is_superuser or "Alumni_events_delete" in request.permissions:
        try:
            AlumniEvent.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/alumni_events")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def session(request):
    records = Session.objects.all()
    form = SessionForm()
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Saved Successfully")
            return HttpResponseRedirect("/session")
        else:
            print(form.errors)
    context = {"form": form, "records": records, "session": "active"}
    return render(request, "System_setting/session.html", context)


@login_required
@user_type_required("Staff")
def session_edit(request, pk):
    records = Session.objects.all()
    record = Session.objects.get(id=pk)
    form = SessionForm(instance=record)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.warning(request, "Record Updated Successfully")
            return HttpResponseRedirect("/session")
    context = {"form": form, "records": records, "session": "active", "edit": True}
    return render(request, "System_setting/session.html", context)


@login_required
@user_type_required("Staff")
def session_view(request, pk):
    records = Session.objects.all()
    record = Session.objects.get(id=pk)
    form = SessionForm(instance=record)
    context = {"form": form, "records": records, "session": "active", "view": True}
    return render(request, "System_setting/session.html", context)


@login_required
@user_type_required("Staff")
def session_delete(request, pk):
    Session.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/session")


@login_required
@user_type_required("Staff")
def role(request):
    records = Role.objects.all()
    form = RoleForm()
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Saved Successfully")

            return HttpResponseRedirect("/role")
        else:
            print(form.errors)
    context = {"form": form, "records": records, "role": "active"}
    return render(request, "System_setting/role.html", context)


@login_required
@user_type_required("Staff")
def assign_permission(request, pk):
    record = Role.objects.get(id=pk)
    if request.method == "POST":
        record.permissions = request.POST.getlist("access")
        record.save()
        return redirect("/role")
    context = {
        "role": "active",
        "record": record,
    }
    return render(request, "System_setting/assign_permission.html", context)


@login_required
@user_type_required("Staff")
def role_edit(request, pk):
    records = Role.objects.all()
    record = Role.objects.get(id=pk)
    form = RoleForm(instance=record)
    if request.method == "POST":
        form = RoleForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.warning(request, "Record Updated Successfully")

            return HttpResponseRedirect("/role")
    context = {"form": form, "records": records, "role": "active", "edit": True}
    return render(request, "System_setting/role.html", context)


@login_required
@user_type_required("Staff")
def role_view(request, pk):
    records = Role.objects.all()
    record = Role.objects.get(id=pk)
    form = RoleForm(instance=record)
    context = {"form": form, "records": records, "role": "active", "view": True}
    return render(request, "System_setting/role.html", context)


@login_required
@user_type_required("Staff")
def role_delete(request, pk):
    Role.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/role")


@login_required
@user_type_required("Staff")
def student_list_view(request, pk):
    toady_date = datetime.now().date()
    fees_records = FeesAssign.objects.filter(student=pk, session=request.Session)
    # fees_discount=FeesTypeDiscount.objects.all()
    fees_discount = DiscountAssign.objects.filter(student=pk, session=request.Session)
    paid_record = StudentFess.objects.filter(student=pk, session=request.Session)

    student = StudentAdmission.objects.get(id=pk)
    custom = CustomFields.objects.filter(field_belongs_to="Student")
    custom_fields = []
    for data in custom:
        obj = StudentCustomFieldValues.objects.filter(field=data, student=pk).last()
        dict = {}
        dict["custome_fields"] = data.field_name
        if obj:
            dict["value"] = obj.value
        else:
            dict["value"] = ""
        custom_fields.append(dict)

    records = Timeline.objects.filter(student=pk)
    document_records = StudentDocuments.objects.filter(student=pk)
    reason = DisableReason.objects.all()
    login_records = LoginCredentials.objects.filter(
        student__admission_no=student.admission_no,
        student__Class=student.Class,
        student__section=student.section,
        student__date_of_birth=student.date_of_birth,
    ).last()
    form = TimelineForm()
    document_form = StudentDocumentsForm()
    if request.method == "POST":
        if request.POST.get("doc_btn"):
            print("aaa")
            document_form = StudentDocumentsForm(request.POST, request.FILES)
            if document_form.is_valid():
                doc_obj = document_form.save(commit=False)
                doc_obj.student_id = pk
                doc_obj.session = request.Session
                doc_obj.created_by = request.user
                doc_obj.save()
                return HttpResponseRedirect(f"/student_list_view/{pk}")
            else:
                print(document_form.errors)
        else:
            form = TimelineForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.student_id = pk
                obj.session = request.Session
                obj.created_by = request.user
                obj.save()
                return HttpResponseRedirect(f"/student_list_view/{pk}")

    context = {
        "form": form,
        "records": records,
        "student_details": "active",
        "student": student,
        "reason": reason,
        "login_records": login_records,
        "custom_fields": custom_fields,
        "document_form": document_form,
        "document_records": document_records,
        "fees_records": fees_records,
        "toady_date": toady_date,
        "fees_discount": fees_discount,
        "paid_record": paid_record,
    }
    return render(request, "Student_information/student_list_view.html", context)


@login_required
@user_type_required("Staff")
def student_list_delete(request, pk):
    Timeline.objects.get(id=pk).delete()
    return HttpResponseRedirect("/student_list_view")


@login_required
@user_type_required("Staff")
def student_doc_delete(request, pk):
    StudentDocuments.objects.get(id=pk).delete()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
@user_type_required("Staff")  # Report
def student_information_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            category_records = StudentCategory.objects.all()

            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                category = request.POST.get("category")
                gender = request.POST.get("gender")
                rte = request.POST.get("rte")

                filters = {}

                if classs:
                    filters["Class_id"] = classs

                if section:
                    filters["section_id"] = section

                if category:
                    filters["category_id"] = category

                if gender:
                    filters["gender"] = gender

                if rte:
                    filters["rte"] = rte

                records = StudentAdmission.objects.filter(**filters)

                context = {
                    "student_information_report": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                    "category_records": category_records,
                }

                return render(
                    request, "Reports/student_information_report.html", context
                )

            context = {
                "student_information_report": "active",
                "class_records": class_records,
                "section_records": section_records,
                "category_records": category_records,
            }

            return render(request, "Reports/student_information_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def guardian_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()

            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                filters = {}
                if classs:
                    filters["Class_id"] = classs

                if section:
                    filters["section_id"] = section

                records = StudentAdmission.objects.filter(**filters)

                context = {
                    "student_information_report": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                }

                return render(request, "Reports/guardian_report.html", context)

            context = {
                "student_information_report": "active",
                "class_records": class_records,
                "section_records": section_records,
            }

            return render(request, "Reports/guardian_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_history_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            today = datetime.today()
            year = today.year
            print(year)

            if request.method == "POST":
                classs = request.POST.get("class")
                yearr = request.POST.get("yearr")
                filters = {}
                if classs:
                    filters["Class_id"] = classs

                if yearr:
                    filters["admission_date__year"] = yearr

                records = StudentAdmission.objects.filter(**filters)

                context = {
                    "student_information_report": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                    "year": year,
                }

                return render(request, "Reports/student_history_report.html", context)

            context = {
                "student_information_report": "active",
                "class_records": class_records,
                "section_records": section_records,
                "year": year,
            }

            return render(request, "Reports/student_history_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def disable_enable(request):
    id = request.POST.get("student_id")
    reason = request.POST.get("reason")
    disable_date = request.POST.get("disable_date")
    disable_note = request.POST.get("disable_note")
    record = StudentAdmission.objects.get(id=id)
    if record.status == "Enable":
        record.status = "Disable"
        record.disable_date = disable_date
        record.diable_reson_id = reason
        record.disable_note = disable_note
        DisableHistroy.objects.create(
            student_id=id,
            disable_date=disable_date,
            diable_reson_id=reason,
            disable_note=disable_note,
        )
    elif record.status == "Disable":
        record.status = "Enable"
    record.save()

    return HttpResponseRedirect(f"/student_list_view/{id}")


@login_required
@user_type_required("Staff")
def addexamlist(request, pk):
    exam_group = examGroup.objects.get(id=pk)
    records = AddExam.objects.filter(exam_group=exam_group, session=request.Session)
    form = AddExamForm()
    if request.method == "POST":
        form = AddExamForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.exam_group = exam_group
            data.save()
            return HttpResponseRedirect(f"/addexamlist/{pk}")
        else:
            print(form.errors)
    context = {
        "form": form,
        "addexamlist": "active",
        "records": records,
        "exam_groups": exam_group,
        "exam_group": "active",
    }
    return render(request, "Examinations/addexamlist.html", context)


@login_required
@user_type_required("Staff")
def addexamlist_edit(request, pk):
    record = AddExam.objects.get(id=pk)
    form = AddExamForm(instance=record)
    if request.method == "POST":
        form = AddExamForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/addexamlist/{record.exam_group.id}")
    context = {"form": form, "addexamlist_edit": "active"}
    return render(request, "Examinations/addexamlist_edit.html", context)


@login_required
@user_type_required("Staff")
def addexamlist_delete(request, pk):
    Timeline.objects.get(id=pk).delete()
    return HttpResponseRedirect("/addexamlist")


@login_required
@user_type_required("Staff")
def assign_view_student(request, pk):
    exam = AddExam.objects.get(id=pk)
    class_records = Class.objects.all()
    section_records = Section.objects.all()
    if request.POST.get("search_btn") == "search_btn":
        classs = request.POST.get("class")
        section = request.POST.get("section")
        exam_student = ExamStudent.objects.filter(
            Class_id=classs,
            section_id=section,
            exam=exam,
            student__session=request.Session,
        )
        records = StudentAdmission.objects.filter(
            Class_id=classs, section_id=section, session=request.Session
        ).exclude(id__in=exam_student.values("student_id"))

        context = {
            "exam_group": "active",
            "records": records,
            "class_records": class_records,
            "section_records": section_records,
            "exam_student": exam_student,
        }
        return render(request, "Examinations/assign_view_student.html", context)
    if request.POST.get("save_btn") == "save_btn":
        ids = request.POST.getlist("student_ids")
        for id in ids:
            stu = StudentAdmission.objects.get(id=id)
            ExamStudent.objects.get_or_create(
                exam_id=pk,
                student_id=id,
                Class=stu.Class,
                section=stu.section,
            )
        rem_ids = request.POST.getlist("rem_ids")
        exits_ids = request.POST.getlist("exits_ids")
        temp = [x for x in exits_ids if x not in rem_ids]
        ExamStudent.objects.filter(id__in=temp).delete()
    context = {
        "exam_group": "active",
        "class_records": class_records,
        "section_records": section_records,
    }
    return render(request, "Examinations/assign_view_student.html", context)


@login_required
@user_type_required("Staff")
# def addexamsubject(request):
#     subject_records=Subjects.objects.all()
#     context={
#         'subject_records':subject_records,
#     }

#     return render(request,'Examinations/addexamsubject.html',context)


@login_required
@user_type_required("Staff")
def addexamsubject(request, pk):
    exam_record = AddExam.objects.get(id=pk)
    subject_records = Subjects.objects.all()
    exam_subjects_records = AddExamSubject.objects.filter(exam=exam_record)

    if request.method == "POST":
        subject_data = request.POST.getlist("subject")
        date_data = request.POST.getlist("date")
        time_data = request.POST.getlist("time")
        duration_data = request.POST.getlist("duration")
        credit_hours_data = request.POST.getlist("credit_hours")
        room_number_data = request.POST.getlist("room_number")
        marks_max_data = request.POST.getlist("marks_max")
        marks_min_data = request.POST.getlist("marks_min")

        # Process the form data as needed
        for i in range(len(subject_data)):
            subject = subject_data[i]
            date = date_data[i]
            time = time_data[i]
            duration = duration_data[i]
            credit_hours = credit_hours_data[i]
            room_number = room_number_data[i]
            marks_max = marks_max_data[i]
            marks_min = marks_min_data[i]

            AddExamSubject.objects.create(
                subject_id=subject,
                date=date,
                time=time,
                duration=duration,
                credit_hours=credit_hours,
                room_number=room_number,
                marks_max=marks_max,
                marks_min=marks_min,
                exam=exam_record,
            )
        messages.success(request, "Record Saved Successfully")
        return HttpResponseRedirect(f"/addexamsubject/{pk}")

    context = {
        "exam_group": "active",
        "subject_records": subject_records,
        "exam_record": exam_record,
        "exam_subjects_records": exam_subjects_records,
    }
    return render(request, "Examinations/addexamsubject.html", context)


@login_required
@user_type_required("Staff")
def delete_exam_subjects(request, pk):
    records = AddExamSubject.objects.get(id=pk)
    exam = records.exam.id
    records.delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect(f"/addexamsubject/{exam}")


@login_required
@user_type_required("Staff")
def addexammark(request, pk):
    records = AddExamSubject.objects.filter(exam=pk)
    return render(
        request,
        "Examinations/addexammark.html",
        {"records": records, "exam_group": "active"},
    )


@login_required
@user_type_required("Staff")
def enter_mark(request, pk):
    exam_subject = AddExamSubject.objects.get(id=pk)
    class_records = Class.objects.all()
    section_records = Section.objects.all()
    session_records = Session.objects.all()
    if request.POST.get("search") == "search":
        classs = request.POST.get("class")
        section = request.POST.get("sectionn")
        session = request.POST.get("session")
        exist_records = EntryMarks.objects.filter(
            student__Class_id=classs,
            student__section_id=section,
            exam_subject=exam_subject,
            student__session=session,
        )
        records = ExamStudent.objects.filter(
            student__Class_id=classs,
            student__section_id=section,
            exam=exam_subject.exam,
            student__session=session,
        )
        context = {
            "exam_group": "active",
            "records": records,
            "class_records": class_records,
            "session_records": session_records,
            "section_records": section_records,
            "exam_subject": exam_subject,
            "pk": pk,
            "exist_records": exist_records,
        }
        return render(request, "Examinations/enter_mark.html", context)
    context = {
        "exam_group": "active",
        "class_records": class_records,
        "session_records": session_records,
        "section_records": section_records,
        "exam_subject": exam_subject,
    }
    return render(request, "Examinations/enter_mark.html", context)


@login_required
@user_type_required("Staff")
def mark_save(request, pk):
    exam_subject = AddExamSubject.objects.get(id=pk)
    student_list = request.POST.getlist("student_id")
    assign_list = request.POST.getlist("assign_list")
    mark_id_list = request.POST.getlist("mark_id")
    marks_list = request.POST.getlist("marks")
    notes_list = request.POST.getlist("notes")
    count = request.POST.get("count")
    attendance_list = []
    for i in range(1, int(count) + 1):
        if f"attendance{i}" in request.POST:
            attendance_list.append(True)
        else:
            attendance_list.append(False)
    if len(mark_id_list) > 0:
        for i in range(len(mark_id_list)):
            data = EntryMarks.objects.get(id=mark_id_list[i])
            data.attendance = attendance_list[i]
            data.marks = marks_list[i]
            data.note = notes_list[i]
            data.save()
    else:
        for i in range(len(student_list)):
            EntryMarks.objects.get_or_create(
                exam=exam_subject.exam,
                exam_subject=exam_subject,
                exam_student_id=assign_list[i],
                subject=exam_subject.subject,
                student_id=student_list[i],
                attendance=attendance_list[i],
                marks=marks_list[i],
                note=notes_list[i],
            )
    return HttpResponseRedirect(f"/enter_mark/{pk}")


@login_required
# @user_type_required("Staff")
def staff_directory(request):
    if (
        request.user.is_superuser
        or "staff_view" in request.permissions
        or "staff_add" in request.permissions
    ):
        try:
            roels = Role.objects.all()
            # User.objects.all().last().delete()
            records = AddStaff.objects.all()
            if request.method == "POST":
                role = request.POST.get("role")
                records = AddStaff.objects.filter(roles=role)
                context = {
                    "records": records,
                    "staff_directory": "active",
                    "roels": roels,
                }
                return render(request, "Human_Resource/staff_directory.html", context)
            context = {"roels": roels, "staff_directory": "active", "records": records}
            return render(request, "Human_Resource/staff_directory.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def Staff_details_show(request, pk):
    record = AddStaff.objects.get(id=pk)
    # payroll
    payroll_records = PayrollSummary.objects.filter(Frist_name=pk)
    total_net_salary = payroll_records.aggregate(Sum("net_salary"))["net_salary__sum"]
    total_gross_salary = payroll_records.aggregate(Sum("gross_salary"))[
        "gross_salary__sum"
    ]
    total_earning = payroll_records.aggregate(Sum("earning"))["earning__sum"]
    total_deduction = payroll_records.aggregate(Sum("deduction"))["deduction__sum"]
    staff_leaves = ApproveLeave.objects.filter(name=pk)
    available_leaves = AvailableLeave.objects.filter(
        staff_leave__staff__id=pk, session=request.Session
    )
    custom = CustomFields.objects.filter(field_belongs_to="Staff")
    custom_fields = []
    for data in custom:
        obj = StaffCustomFieldValues.objects.filter(field=data, staff=pk).last()
        dict = {}
        dict["custome_fields"] = data.field_name
        if obj:
            dict["value"] = obj.value
        else:
            dict["value"] = ""
        custom_fields.append(dict)
    #  document upload
    document_records = StaffDocument.objects.filter(staff=pk)
    document_form = StaffDocumentForm()
    if request.POST.get("doc_btn"):
        document_form = StaffDocumentForm(request.POST, request.FILES)
        if document_form.is_valid():
            obj = document_form.save(commit=False)
            obj.staff_id = pk
            obj.created_by = request.user
            obj.save()
            return redirect(f"/Staff_details_show/{pk}")
    #  Timeline
    timeline_records = StaffTimeline.objects.filter(staff=pk)
    timeline_form = StaffTimelineForm()
    if request.POST.get("timeline_btn"):
        timeline_form = StaffTimelineForm(request.POST, request.FILES)
        if timeline_form.is_valid():
            obj = timeline_form.save(commit=False)
            obj.staff_id = pk
            obj.created_by = request.user
            obj.save()
            return redirect(f"/Staff_details_show/{pk}")
        else:
            print(timeline_form.errors)
    context = {
        "record": record,
        "staff_directory": "active",
        "custom_fields": custom_fields,
        "payroll_records": payroll_records,
        "document_records": document_records,
        "document_form": document_form,
        "staff_leaves": staff_leaves,
        "available_leaves": available_leaves,
        "timeline_records": timeline_records,
        "timeline_form": timeline_form,
        "total_net_salary": total_net_salary,
        "total_gross_salary": total_gross_salary,
        "total_earning": total_earning,
        "total_deduction": total_deduction,
    }
    return render(request, "Human_Resource/Staff_details_show.html", context)


@login_required
@user_type_required("Staff")
def delete_staff_document(request, pk):
    StaffDocument.objects.get(id=pk).delete()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
@user_type_required("Staff")
def delete_staff_timeline(request, pk):
    StaffTimeline.objects.get(id=pk).delete()
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
@user_type_required("Staff")
def staff_disable_enable(request):
    pk = request.POST.get("staff_id")
    record = AddStaff.objects.get(id=pk)
    if record.status == "Disable":
        record.status = "Enable"
    else:
        record.status = "Disable"
        record.disable_date = request.POST.get("disable_date")
    record.save()
    return HttpResponseRedirect(f"/Staff_details_show/{pk}")


@login_required
@user_type_required("Staff")
def add_staffs_edit(request, pk):
    system_fields = SystemFields.objects.last().staff_fields
    custom_fields = CustomFields.objects.filter(field_belongs_to="Staff")
    staff_custom = StaffCustomFieldValues.objects.filter(staff=pk)
    custom_fileds_records = []
    for data in custom_fields:
        dict = {}
        dict["custom_fields"] = data
        dict["student_custom"] = staff_custom.filter(field=data.id).last()
        custom_fileds_records.append(dict)
    print(custom_fileds_records)
    record = AddStaff.objects.get(id=pk)
    form = AddStaffForm(instance=record)
    leave_type = AddLeaveType.objects.all()
    staff_leave_records = StaffLeave.objects.filter(staff=pk)
    leave_list = []
    for data in leave_type:
        dict = {}
        obj = staff_leave_records.filter(leave_type=data).last()
        if obj:
            dict["name"] = data.name
            dict["count"] = obj.total_leave
        else:
            dict["name"] = data.name
            dict["count"] = ""
        leave_list.append(dict)
    if request.method == "POST":
        form = AddStaffForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            for data in leave_type:
                leave_count = request.POST.get(data.name)
                assign_leave = staff_leave_records.filter(leave_type=data).last()
                if assign_leave:
                    assign_leave.total_leave = int(leave_count)
                    assign_leave.save()
                    available_leaves = AvailableLeave.objects.filter(
                        session=request.Session
                    )
                    if available_leaves:
                        available_leave = available_leaves.filter(
                            staff_leave=assign_leave
                        ).last()
                        if available_leave:
                            add_leave = int(leave_count) - available_leave.total_leave
                            available_leave.available_leave = (
                                available_leave.available_leave + add_leave
                            )
                            available_leave.total_leave = int(leave_count)
                            available_leave.save()
                        else:
                            AvailableLeave.objects.create(
                                staff_leave=assign_leave,
                                available_leave=leave_count,
                                total_leave=leave_count,
                                session=request.Session,
                            )
                else:
                    if leave_count:
                        StaffLeave.objects.create(
                            staff_id=record.id, leave_type=data, total_leave=leave_count
                        )

            #  customs fields
            for data in custom_fields:
                if data.field_type == "multiselect":
                    value = request.POST.getlist(f"{data.field_name}")
                else:
                    value = request.POST.get(f"{data.field_name}")
                if value:
                    edit = staff_custom.filter(field=data.id).last()
                    if edit:
                        edit.value = value
                        edit.save()
                    else:
                        StaffCustomFieldValues.objects.create(
                            field=data, staff_id=pk, value=value
                        )
            messages.warning(request, "Record Updated Successfully")
            return HttpResponseRedirect("/staff_directory")
    context = {
        "form": form,
        "records": record,
        "add_staff": "active",
        "leave_list": leave_list,
        "custom_fields": custom_fields,
        "student_custom": staff_custom,
        "custom_fileds_records": custom_fileds_records,
        "system_fields": system_fields,
    }
    return render(request, "Human_Resource/add_staffs_edit.html", context)


@login_required
@user_type_required("Staff")
def staff_attendance_view(request):
    if request.user.is_superuser or "staff_attendance_view" in request.permissions:
        try:
            roless = Role.objects.all()
            if request.POST.get("search") == "search":
                roles = request.POST.get("role")
                attendance_datee = request.POST.get("from_date")
                records = AddStaff.objects.filter(roles=roles)
                record = StaffAttendance.objects.filter(
                    staff_id__in=records.values("id"), attendance_date=attendance_datee
                )
                print("records", records)
                print("record", record)

                context = {
                    "staff_attendance_view": "active",
                    "records": records,
                    "record": record,
                    "attendance_datee": attendance_datee,
                    "roles": roless,
                }
                return render(
                    request, "Human_Resource/staff_attendance_view.html", context
                )

            if request.POST.get("all_save") == "all_save":
                staff_id = request.POST.getlist("staff_id")
                for data in staff_id:
                    holiday = request.POST.get("holiday")
                    if request.POST.get(f"attendance{data}") or holiday:
                        edit_staff = StaffAttendance.objects.filter(
                            staff_id=data,
                            attendance_date=request.POST.get("attendance_datee"),
                        ).last()
                        if holiday:
                            attendance_status = "Holiday"
                        else:
                            attendance_status = request.POST.get(f"attendance{data}")

                        if edit_staff:
                            edit_staff.attendance_status = attendance_status
                            edit_staff.note = request.POST.get(f"note{data}")
                            edit_staff.save()
                        else:
                            StaffAttendance.objects.create(
                                staff_id=data,
                                attendance_status=attendance_status,
                                attendance_date=request.POST.get("attendance_datee"),
                                note=request.POST.get(f"note{data}"),
                            )
                return redirect("staff_attendance_view")
            context = {"staff_attendance_view": "active", "roles": roless}
            return render(request, "Human_Resource/staff_attendance_view.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def payroll(request):
    teacher = request.POST.get("class")
    months = request.POST.get("months")
    years = request.POST.get("years")
    request.session["months"] = months
    request.session["years"] = years
    header = PrintHeaderFooter.objects.all().first()
    record = PayrollSummary.objects.filter(Months=months, year=years)
    roles = Role.objects.all()
    listt = []
    for data in record:
        listt.append(data.Frist_name.id)
    if request.method == "POST":
        records = AddStaff.objects.filter(roles=teacher).exclude(id__in=listt)
        context = {
            "records": records,
            "record": record,
            "roles": roles,
            "payroll": "active",
            "header": header,
        }
        return render(request, "Human_Resource/payroll.html", context)
    context = {"payroll": "active", "roles": roles}
    return render(request, "Human_Resource/payroll.html", context)


@login_required
@user_type_required("Staff")
def payroll_view(request, pk):
    months = request.session["months"]
    years = request.session["years"]
    record = AddStaff.objects.get(id=pk)
    month = 3
    month_2 = 4
    month_3 = 5
    staff = StaffAttendance.objects.filter(
        attendance_date__month__gte=month, staff_id=record.id
    )
    staff = StaffAttendance.objects.filter(
        attendance_date__month__gte=month_2, staff_id=record.id
    )
    staff = StaffAttendance.objects.filter(
        attendance_date__month__gte=month_3, staff_id=record.id
    )

    staffs = staff.filter(attendance_status="present")
    staffss = staff.filter(attendance_status="Late")
    staffsss = staff.filter(attendance_status="Absent")
    half = staff.filter(attendance_status="half")

    present_2 = staff.filter(attendance_status="present")
    Late_2 = staff.filter(attendance_status="Late")
    Absent_2 = staff.filter(attendance_status="Absent")
    half = staff.filter(attendance_status="half")

    present_3 = staff.filter(attendance_status="present")
    Late_3 = staff.filter(attendance_status="Late")
    Absent_3 = staff.filter(attendance_status="Absent")
    half = staff.filter(attendance_status="half")

    if request.method == "POST":
        PayrollSummary.objects.create(
            basic_salary=request.POST.get("basicsalary"),
            earning=float(request.POST.get("earning")),
            gross_salary=float(request.POST.get("gross_salary")),
            deduction=float(request.POST.get("deduction")),
            Tax=float(request.POST.get("tax")),
            net_salary=float(request.POST.get("net_salary")),
            status="Generated",
            Frist_name_id=pk,
            Months=months,
            year=years,
        )
        return HttpResponseRedirect("/payroll")

    context = {
        "record": record,
        "payroll_view": "active",
        "view": True,
        "staff": staff,
        "staffs": staffs.count(),
        "staffss": staffss.count(),
        "staffsss": staffsss.count(),
        "present_2": present_2.count(),
        "Late_2": Late_2.count(),
        "Absent_2": Absent_2.count(),
        "Absent_2": Absent_2.count(),
        "present_3": present_3.count(),
        "Late_3": Late_3.count(),
        "Absent_3": Absent_3.count(),
        "half": half.count(),
        "payroll": "active",
    }
    return render(request, "Human_Resource/payroll_view.html", context)


@login_required
@user_type_required("Staff")
def payroll_piad(request, pk):
    records = PayrollSummary.objects.get(id=pk)
    if request.method == "POST":
        records.payment_date = request.POST.get("from_date")
        records.Payment_mode = request.POST.get("staffs")
        records.status = "Paid"
        records.save()
        return HttpResponseRedirect("/payroll")
    context = {"records": records, "payroll": "active"}
    return render(request, "Human_Resource/payroll_piad.html", context)


@login_required
@user_type_required("Staff")
def Payroll_payslip(request, pk):
    record = PayrollSummary.objects.get(id=pk)
    context = {"records": record, "payroll": "active"}
    return render(request, "Human_Resource/Payroll_payslip.html", context)


@login_required
@user_type_required("Staff")
def Human_Resource(request):
    if request.user.is_superuser or "human_resource_report_view" in request.permissions:
        try:
            designation_records = Designation.objects.all()
            records = AddStaff.objects.all()
            roles_records = Role.objects.all()
            if request.method == "POST":
                roles = request.POST.get("roles")
                date_from = request.POST.get("from_date")
                date_to = request.POST.get("to_date")
                desingation = request.POST.get("designation")
                status = request.POST.get("status")
                filters = {}
                if date_from and date_to:
                    filters["date_of_joining__range"] = [date_from, date_to]
                if date_from:
                    filters["date_of_joining__gte"] = date_from
                if date_to:
                    filters["date_of_joining__lte"] = date_to
                if desingation:
                    filters["designation_id"] = desingation
                if status:
                    filters["status"] = status
                if roles:
                    filters["roles"] = roles

                records = AddStaff.objects.filter(**filters)
                print(records)
                context = {
                    "records": records,
                    "designation_records": designation_records,
                    "roles_records": roles_records,
                    "Human_Resource_report": "active",
                }
                return render(request, "Human_Resource/Human_Resource.html", context)
            context = {
                "records": records,
                "Human_Resource_report": "active",
                "designation_records": designation_records,
                "roles_records": roles_records,
            }
            return render(request, "Human_Resource/Human_Resource.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
@user_type_required("Staff")
def payroll_report(request):
    roles_records = Role.objects.all()
    if request.POST.get("search") == "search":
        teacher = request.POST.get("class")
        months = request.POST.get("months")
        years = request.POST.get("years")
        filters = {}
        if teacher:
            filters["Frist_name__roles"] = teacher
        if months:
            filters["Months"] = months
        records = PayrollSummary.objects.filter(**filters, year=years)
        context = {
            "records": records,
            "roles_records": roles_records,
            "Human_Resource_report": "active",
        }
        return render(request, "Human_Resource/payroll_report.html", context)

    context = {"roles_records": roles_records, "Human_Resource_report": "active"}
    return render(request, "Human_Resource/payroll_report.html", context)


@login_required
@user_type_required("Staff")
def mange_alumini(request):
    if request.user.is_superuser or "manage_alumni_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            session_recods = Session.objects.all()

            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                session = request.POST.get("session")
                recordss = Managealumini.objects.filter(students_id=session)
                list = []
                for data in recordss:
                    list.append(data.students_id.id)
                record = StudentAdmission.objects.filter(
                    Class_id=classs, section_id=section, session=session
                ).exclude(id__in=list)

                context = {
                    "class_records": class_records,
                    "section_records": section_records,
                    "mange_alumini": "active",
                    "record": record,
                    "recordss": recordss,
                    "session_recods": session_recods,
                }
                return render(request, "Alumni/Mange_alumini.html", context)

            context = {
                "class_records": class_records,
                "section_records": section_records,
                "mange_alumini": "active",
                "session_recods": session_recods,
            }
            return render(request, "Alumni/Mange_alumini.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def Mange_alumini_add(request, pk):
    if request.user.is_superuser or "manage_alumni_add" in request.permissions:
        try:
            record = StudentAdmission.objects.get(id=pk)
            form = ManagealuminiForm()
            if request.method == "POST":
                form = ManagealuminiForm(request.POST, request.FILES)
                if form.is_valid():
                    student = form.save(commit=False)
                    student.students_id = record
                    student.save()
                    return HttpResponseRedirect("/mange_alumini")
                else:
                    print(form.errors)
            context = {"form": form, "view": True, "record": record}
            return render(request, "Alumni/Mange_alumini_add.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def Mange_alumini_edit(request, pk):
    if request.user.is_superuser or "manage_alumni_edit" in request.permissions:
        try:
            records = Managealumini.objects.all()
            record = Managealumini.objects.get(id=pk)
            form = ManagealuminiForm(instance=record)
            if request.method == "POST":
                form = ManagealuminiForm(request.POST, request.FILES, instance=record)
                if form.is_valid():
                    student = form.save()
                    return HttpResponseRedirect("/mange_alumini")
            context = {
                "form": form,
                "records": records,
            }
            return render(request, "Alumni/Mange_alumini_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def Mange_alumini_delete(request, pk):
    Managealumini.objects.get(id=pk).delete()
    return HttpResponseRedirect("/mange_alumini")


@login_required
@user_type_required("Staff")
def mange_alumini_report(request):
    if request.user.is_superuser or "Alumini_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            session_records = Session.objects.all()
            recordss = Managealumini.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                session = request.POST.get("session")
                print(classs, section)
                filters = {}
                if classs:
                    filters["Class_id"] = classs
                if section:
                    filters["section_id"] = section
                if session:
                    filters["session_id"] = session
                record = StudentAdmission.objects.filter(**filters).values("id")
                records = Managealumini.objects.filter(students_id__in=record)
                context = {
                    "class_records": class_records,
                    "section_records": section_records,
                    "records": records,
                    "mange_alumini_report": "active",
                    "session_records": session_records,
                }
                return render(request, "Reports/Mange_alumini_report.html", context)

            context = {
                "mange_alumini_report": "active",
                "session_records": session_records,
                "class_records": class_records,
                "section_records": section_records,
                "recordss": recordss,
            }
            return render(request, "Reports/Mange_alumini_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def hostel_repoert(request):
    if request.user.is_superuser or "hostel_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            hostel_room = Hostel.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                hostell = request.POST.get("hostel_room")
                filters = {}
                if classs:
                    filters["Class_id"] = classs
                if section:
                    filters["section_id"] = section
                if hostell:
                    filters["hostel_id"] = hostell

                record = StudentAdmission.objects.filter(
                    **filters, hostel__isnull=False
                )

                context = {
                    "hostel_repoert": "active",
                    "class_records": class_records,
                    "section_records": section_records,
                    "record": record,
                    "hostel_room": hostel_room,
                }
                return render(request, "Reports/hostel_repoert.html", context)
            context = {
                "hostel_room": hostel_room,
                "hostel_repoert": "active",
                "class_records": class_records,
                "section_records": section_records,
            }
            return render(request, "Reports/hostel_repoert.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
@user_type_required("Staff")
def transport_report(request):
    if request.user.is_superuser or "transport_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            route = Route.objects.all()
            vehicle = Vehicle.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section_id = request.POST.get("section")
                route_id = request.POST.get("route")
                vechicle_id = request.POST.get("vechicle")
                filters = {}
                if vechicle_id:
                    filters["vehicle_number_id"] = vechicle_id
                if classs:
                    filters["Class_id"] = classs
                if section_id:
                    filters["section_id"] = section_id
                if route_id:
                    filters["route_list_id"] = route_id
                record = StudentAdmission.objects.filter(
                    **filters, route_list__isnull=False
                )
                context = {
                    "hostel_repoert": "active",
                    "class_records": class_records,
                    "section_records": section_records,
                    "record": record,
                    "route": route,
                    "vehicle": vehicle,
                }
                return render(request, "Reports/transport_report.html", context)

            context = {
                "view": True,
                "transport_report": "active",
                "route": route,
                "vehicle": vehicle,
                "section_records": section_records,
                "class_records": class_records,
            }
            return render(request, "Reports/transport_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
@user_type_required("Staff")
def library(request):
    if request.user.is_superuser or "library_report_view" in request.permissions:
        try:
            context = {"libary_report": "active"}
            return render(request, "Reports/library.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
@user_type_required("Staff")
def book_isseu_report(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        member_type = request.POST.get("staffs")
        filters = {}
        if from_date and to_date:
            print("=====2")
            filters["issued_date__range"] = [from_date, to_date]
        if from_date:
            print("=====3")
            filters["issued_date__gte"] = from_date
        if to_date:
            print("=====4")
            filters["issued_date__lte"] = to_date
        if member_type:
            filters["member__member_type__icontains"] = member_type
        print(filters)
        records = IssueBook.objects.filter(**filters)
        context = {"records": records, "libary_report": "active"}
        return render(request, "Reports/book_isseu_report.html", context)
    context = {"libary_report": "active"}
    return render(request, "Reports/book_isseu_report.html", context)


@login_required
@user_type_required("Staff")
def book_inventory_report(request):
    records = AddBook.objects.all()

    context = {"libary_report": "active", "records": records}
    return render(request, "Reports/book_inventory_report.html", context)


@login_required
@user_type_required("Staff")
def book_due_report(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        member_type = request.POST.get("staffs")
        filters = {}
        if from_date and to_date:
            filters["due_return_date__range"] = [from_date, to_date]
        if member_type:
            filters["member__member_type__icontains"] = member_type

        records = IssueBook.objects.filter(**filters)
        print("re", records)
        context = {"records": records, "libary_report": "active"}
        return render(request, "Reports/book_due_report.html", context)
    context = {"libary_report": "active"}
    return render(request, "Reports/book_due_report.html", context)


@login_required
@user_type_required("Staff")
def book_issue_return_report(request):
    record = IssueBook.objects.filter(return_date__isnull=False)
    context = {"libary_report": "active", "record": record}
    return render(request, "Reports/book_issue_return_report.html", context)


@login_required
@user_type_required("Staff")
def Inventory(request):
    if request.user.is_superuser or "inventory_report_view" in request.permissions:
        try:
            context = {"issue_item_report": "active"}
            return render(request, "Reports/Inventory.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
@user_type_required("Staff")
def stock_report(request):
    records = ItemStockDeatail.objects.all()
    context = {"records": records, "issue_item_report": "active"}
    return render(request, "Reports/stock_report.html", context)


@login_required
@user_type_required("Staff")
def issue_item_report(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        filters = {}
        if from_date and to_date:
            filters["issue_date__range"] = [from_date, to_date]
        elif from_date:
            filters["issue_date__gte"] = from_date
        elif to_date:
            filters["issue_date__lte"] = to_date

        records = IssueItem.objects.filter(**filters)
        print("re", records)
        context = {"records": records, "issue_item_report": "active"}
        return render(request, "Reports/issue_item_report.html", context)

    context = {"issue_item_report": "active"}
    return render(request, "Reports/issue_item_report.html", context)


@login_required
@user_type_required("Staff")
def Add_item_report(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        filters = {}
        if from_date and to_date:
            filters["date__range"] = [from_date, to_date]
        elif from_date:
            filters["date__gte"] = from_date
        elif to_date:
            filters["date__lte"] = to_date

        records = ItemStock.objects.filter(**filters)
        context = {"records": records, "issue_item_report": "active"}
        return render(request, "Reports/Add_item_report.html", context)

    context = {"issue_item_report": "active"}
    return render(request, "Reports/Add_item_report.html", context)


@login_required
@user_type_required("Staff")
def attendence(request):
    if request.user.is_superuser or "attendance_report_view" in request.permissions:
        try:
            context = {"attendence_report": "active"}
            return render(request, "Reports/attendence.html", context)

        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
@user_type_required("Staff")
def date_iter(year, month):
    from datetime import date

    for i in range(1, calendar.monthlen(year, month) + 1):
        yield date(year, month, i)


@login_required
@user_type_required("Staff")
def attendence_report(request):
    class_records = Class.objects.all()
    section_records = Section.objects.all()
    if request.method == "POST":
        classs = request.POST.get("class")
        section = request.POST.get("section")
        months = request.POST.get("months")
        years = request.POST.get("years")
        if classs and section and months and years:
            records = StudentAttendance.objects.filter(
                student__Class=classs,
                student__section=section,
                attendance_date__month=months,
                attendance_date__year=years,
            )
            header = []
            body = []
            print(int(months), int(years))
            cal = calendar.monthcalendar(int(years), int(months))
            # List of day names for header
            days = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            student_rcords = StudentAdmission.objects.filter(
                Class=classs, section=section, session=request.Session
            )
            # Iterate through each week in the calendar
            count = 0
            for student in student_rcords:
                count += 1
                records = StudentAttendance.objects.filter(
                    student=student,
                    student__Class=classs,
                    student__section=section,
                    attendance_date__month=months,
                    attendance_date__year=years,
                )
                day_list = []
                dict = {}
                for week in cal:
                    # Iterate through each day in the week
                    for day in week:
                        # If the day is 0, it means it's a day outside the month, so skip it
                        if day == 0:
                            continue
                        else:
                            # Get the day name for the current date
                            day_name = days[
                                calendar.weekday(int(years), int(months), day)
                            ]
                            # Display the date and day
                            if count == 1:
                                header.append(f"{day} {day_name[:3]}")
                            student_attn = records.filter(
                                attendance_date__day=day
                            ).last()
                            if student_attn:
                                day_list.append(
                                    student_attn.attendance_status[:1].capitalize()
                                )
                            else:
                                day_list.append("")
                dict["attendace"] = day_list
                dict["student"] = student
                dict["present"] = records.filter(attendance_status="present").count()
                dict["absent"] = records.filter(attendance_status="Absent").count()
                dict["late"] = records.filter(attendance_status="Late").count()
                dict["half_day"] = records.filter(attendance_status="Half Day").count()
                body.append(dict)
            context = {"header": header, "body": body, "attendence_report": "active"}
            return render(request, "Reports/attendence_report.html", context)
    context = {
        "class_records": class_records,
        "section_records": section_records,
        "attendence_report": "active",
    }
    return render(request, "Reports/attendence_report.html", context)


@login_required
@user_type_required("Staff")
def daily_attendance_report(request):
    if request.user.is_superuser or "attendance_by_date_view" in request.permissions:
        try:
            if request.POST.get("search") == "search":
                attendance_date = request.POST.get("attendance_date")
                attendance_records = StudentAttendance.objects.filter(
                    attendance_date=attendance_date
                )

                if not attendance_records:
                    context = {
                        "attendence_report": "active",
                        "attendance_records": attendance_records,
                        "attendance_date": attendance_date,
                        "error_message": "No attendance records found for the selected date.",
                    }
                    return render(
                        request, "Reports/daily_attendance_report.html", context
                    )

                class_totals = {}
                total_present = 0
                total_absent = 0
                total_students = 0

                for record in attendance_records:
                    student = record.student
                    class_key = f"{student.Class} ({student.section})"

                    if class_key not in class_totals:
                        class_totals[class_key] = {
                            "total_present": 0,
                            "total_absent": 0,
                            "total_students": 0,
                        }

                    class_totals[class_key]["total_students"] += 1

                    if record.attendance_status in ["present", "Late"]:
                        class_totals[class_key]["total_present"] += 1
                        total_present += 1
                    elif record.attendance_status == "Absent":
                        class_totals[class_key]["total_absent"] += 1
                        total_absent += 1

                    total_students += 1

                overall_present_percentage = (total_present / total_students) * 100
                overall_absent_percentage = (total_absent / total_students) * 100

                # Format the percentages
                overall_present_percentage_formatted = floatformat(
                    overall_present_percentage, 2
                )
                overall_absent_percentage_formatted = floatformat(
                    overall_absent_percentage, 2
                )

                for class_total in class_totals.values():
                    class_total["present_percentage"] = floatformat(
                        (class_total["total_present"] / class_total["total_students"])
                        * 100,
                        2,
                    )
                    class_total["absent_percentage"] = floatformat(
                        (class_total["total_absent"] / class_total["total_students"])
                        * 100,
                        2,
                    )

                context = {
                    "attendence_report": "active",
                    "attendance_records": attendance_records,
                    "attendance_date": attendance_date,
                    "class_totals": class_totals,
                    "total_present": total_present,
                    "total_absent": total_absent,
                    "total_students": total_students,
                    "overall_present_percentage": overall_present_percentage_formatted,
                    "overall_absent_percentage": overall_absent_percentage_formatted,
                }
                return render(request, "Reports/daily_attendance_report.html", context)

            context = {
                "attendence_report": "active",
                "attendance_records": [],
            }
            return render(request, "Reports/daily_attendance_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "error.html")


@login_required
@user_type_required("Staff")
def student_attendance_type_report(request):
    class_records = Class.objects.all()
    section_records = Section.objects.all()
    if request.method == "POST":
        classs = request.POST.get("class")
        section = request.POST.get("section")
        presentt = request.POST.get("present")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        filters = {}
        if section:
            filters["student__section"] = section
        if from_date and to_date:
            filters["attendance_date__range"] = [from_date, to_date]
        if from_date:
            filters["attendance_date__gte"] = from_date
        if to_date:
            filters["attendance_date__lte"] = to_date

        records = StudentAttendance.objects.filter(
            student__Class=classs, attendance_status=presentt, **filters
        )

        context = {
            "record": records,
            "class_records": class_records,
            "section_records": section_records,
            "attendence_report": "active",
        }
        return render(request, "Reports/student_attendance_type_report.html", context)

    context = {
        "class_records": class_records,
        "section_records": section_records,
        "attendence_report": "active",
    }
    return render(request, "Reports/student_attendance_type_report.html", context)


@login_required
@user_type_required("Staff")
def staff_attendance_report(request):
    roles_records = Role.objects.all()
    if request.method == "POST":
        roles = request.POST.get("roles")
        months = request.POST.get("months")
        years = request.POST.get("years")
        if roles and months and years:
            header = []
            body = []
            print(int(months), int(years))
            cal = calendar.monthcalendar(int(years), int(months))
            # List of day names for header
            days = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            student_rcords = AddStaff.objects.filter(roles=roles)
            # Iterate through each week in the calendar
            print("student_rcords", student_rcords)
            count = 0
            for student in student_rcords:
                count += 1
                records = StaffAttendance.objects.filter(
                    staff__id=student.id,
                    attendance_date__month=months,
                    attendance_date__year=years,
                )
                day_list = []
                dict = {}
                for week in cal:
                    # Iterate through each day in the week
                    for day in week:
                        # If the day is 0, it means it's a day outside the month, so skip it
                        if day == 0:
                            continue
                        else:
                            # Get the day name for the current date
                            day_name = days[
                                calendar.weekday(int(years), int(months), day)
                            ]
                            # Display the date and day
                            if count == 1:
                                header.append(f"{day} {day_name[:3]}")
                            student_attn = records.filter(
                                attendance_date__day=day
                            ).last()
                            if student_attn:
                                day_list.append(
                                    student_attn.attendance_status[:1].capitalize()
                                )
                            else:
                                day_list.append("")
                dict["attendace"] = day_list
                dict["student"] = student
                dict["present"] = records.filter(attendance_status="present").count()
                dict["absent"] = records.filter(attendance_status="Absent").count()
                dict["late"] = records.filter(attendance_status="Late").count()
                dict["half_day"] = records.filter(attendance_status="Half Day").count()
                body.append(dict)
        context = {
            "roles_records": roles_records,
            "header": header,
            "body": body,
            "attendence_report": "active",
        }
        return render(request, "Reports/staff_attendance_report.html", context)
    context = {"roles_records": roles_records, "attendence_report": "active"}
    return render(request, "Reports/staff_attendance_report.html", context)


@login_required
@user_type_required("Staff")
def general_setting(request):
    records = GeneralSetting.objects.all()
    if records:
        record = GeneralSetting.objects.all().last()
        form = GeneralSettingForm(instance=record)
        if request.method == "POST":
            form = GeneralSettingForm(request.POST, request.FILES, instance=record)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/general_setting")
            else:
                print(form.errors)
        context = {"record": record, "general_setting_ac": "active", "form": form}
        return render(request, "System_setting/general.html", context)

    else:
        form = GeneralSettingForm()
        if request.method == "POST":
            form = GeneralSettingForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/general_setting")

    context = {"records": records, "general_setting_ac": "active", "form": form}
    return render(request, "System_setting/general.html", context)


@login_required
def student_js(request):
    class_id = request.GET.get("class_id")
    section_id = request.GET.get("id_section")
    student = StudentAdmission.objects.filter(
        Class=class_id, section=section_id, session=request.Session
    )
    return JsonResponse(
        data=list(student.values("id", "first_name", "last_name")), safe=False
    )


@login_required
@user_type_required("Staff")
def manage_syllabus_status(request):
    if (
        request.user.is_superuser
        or "manage_syllabus_status_view" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            if request.POST.get("search") == "search":
                classs = request.POST.get("Class")
                section = request.POST.get("section")
                subject_groups = request.POST.get("subject_group")
                subject = request.POST.get("subject")
                record = topic.objects.filter(
                    Class_id=classs,
                    section_id=section,
                    subject_group_id=subject_groups,
                    subject_id=subject,
                )
                context = {
                    "manage_syllabus_status": "active",
                    "class_records": class_records,
                    "record": record,
                }
                return render(
                    request, "Lesson_plan/manage_syllabus_status.html", context
                )

            if request.POST.get("save") == "save":
                date_save = request.POST.get("from_date")
                date_idd = request.POST.get("date_id")
                record = topic.objects.get(id=date_idd)
                record.date_save = date_save
                record.status = "complete"
                record.save()
            context = {
                "manage_syllabus_status": "active",
                "class_records": class_records,
            }
            return render(request, "Lesson_plan/manage_syllabus_status.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "error.html", {"error": error})


# ----------------------------------------- website part----------------------------------------


@login_required
@user_type_required("Staff")
def web_index(request):
    records = BasicWebPageDetails.objects.all()
    carosel_records = CaroselImage.objects.all()
    infrastructure_record = Infrastructure.objects.all()
    school_staff_record = SchoolStaff.objects.all()
    school_heads = SchoolHeads.objects.all()
    events_record = Events.objects.all()
    news_record = News.objects.all()
    offers_record = Offers.objects.all()
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        web_enquiry_form = WebEnquiryForm(request.POST)
        if contact_form.is_valid() and web_enquiry_form.is_valid():
            print("1")
            contact_form.save()
            web_enquiry_form.save()
            print("2")
            messages.success(
                request, "Thank you for your message! We will get back to you soon."
            )
            return redirect(
                "/web_index#contact"
            )  # Redirect to the same page after successful submission
        else:
            print("3", web_enquiry_form.errors)
            messages.error(
                request,
                "Failed to submit the form. Please check the details and try again.",
            )
            return redirect("/web_index#contact")
    else:
        contact_form = ContactForm()
        web_enquiry_form = WebEnquiryForm()

    context = {
        "records": records,
        "carosel_records": carosel_records,
        "events_record": events_record,
        "infrastructure_record": infrastructure_record,
        "school_staff_record": school_staff_record,
        "school_heads": school_heads,
        "news_record": news_record,
        "offers_record": offers_record,
        "contact_form": contact_form,
        "web_enquiry_form": web_enquiry_form,
    }

    return render(request, "Website/web_index.html", context)


@login_required
@user_type_required("Staff")
# def web_index(request):
#     records=BasicWebPageDetails.objects.all()
#     carosel_records=CaroselImage.objects.all()
#     infrastructure_record=Infrastructure.objects.all()
#     school_staff_record=SchoolStaff.objects.all()
#     school_heads=SchoolHeads.objects.all()
#     events_record=Events.objects.all()
#     news_record=News.objects.all()
#     offers_record=Offers.objects.all()
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Thank you for your message! We will get back to you soon.')
#             return redirect('/web_index#contact')
#         else:
#             messages.error(request, 'Failed to submit the form. Please Check the Details and try Again ')
#             return redirect('/web_index#contact')
#     else:
#         form = ContactForm()

#     context = {
#         'records': records,
#         'carosel_records': carosel_records,
#         'events_record': events_record,
#         'infrastructure_record': infrastructure_record,
#         'school_staff_record': school_staff_record,
#         'school_heads': school_heads,
#         'news_record': news_record,
#         'offers_record': offers_record,
#         'form': form,
#     }

#     return render(request, 'Website/web_index.html', context)


# if request.method == 'POST':
#     form = ContactForm(request.POST)
#     if form.is_valid():
#         print('1')
#         form.save()
#         print('2')
#         return redirect('success')  # Redirect to success page
# else:
#     form = ContactForm()
#     print('3')
# context={
#         'records':records,'carosel_records':carosel_records,
#         'events_record':events_record,'infrastructure_record':infrastructure_record,
#         'school_staff_record':school_staff_record,'school_heads':school_heads,
#         'news_record':news_record,'offers_record':offers_record
#         }
# return render(request,'Website/web_index.html',context)


@login_required
@user_type_required("Staff")
def basic_detail(request):
    if (
        request.user.is_superuser
        or "banner_image_view" in request.permissions
        or "banner_image_add" in request.permissions
    ):
        try:
            records = BasicWebPageDetails.objects.all()
            if records:
                record = BasicWebPageDetails.objects.all().last()
                form = BasicWebPageDetailsForm(instance=record)
                if request.method == "POST":
                    form = BasicWebPageDetailsForm(
                        request.POST, request.FILES, instance=record
                    )
                    if form.is_valid():
                        form.save()
                        messages.warning(request, "Record Updated Successfully")
                        return HttpResponseRedirect("/basic_detail")
                context = {"record": record, "basic_detail": "active", "form": form}
                return render(request, "Front_cms/basic_detail.html", context)

            else:
                form = BasicWebPageDetailsForm()
                if request.method == "POST":
                    form = BasicWebPageDetailsForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save()
                        messages.warning(request, "Record Updated Successfully")
                        return HttpResponseRedirect("/basic_detail")

                context = {"records": records, "basic_detail": "active", "form": form}
                return render(request, "Front_cms/basic_detail.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def carousel(request):
    if (
        request.user.is_superuser
        or "carosel_view" in request.permissions
        or "carosel_add" in request.permissions
    ):
        try:
            records = CaroselImage.objects.all()
            if request.method == "POST":
                form = CaroselImageForm(request.POST, request.FILES)

                carosel_images = request.FILES.getlist("carosel_image")
                for carosel_imagee in carosel_images:
                    CaroselImage.objects.create(carosel_image=carosel_imagee)
                return redirect("carousel")
            else:
                form = CaroselImageForm()
            return render(
                request,
                "Front_cms/carousel.html",
                {"form": form, "carousel": "active", "records": records},
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def carousel_edit(request, pk):
    if request.user.is_superuser or "carosel_view" in request.permissions:
        try:
            record = CaroselImage.objects.get(id=pk)
            record.image_title = request.POST.get("image_title")
            record.image_description = request.POST.get("image_description")
            record.save()
            return redirect("carousel")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def carousel_delete(request, pk):
    CaroselImage.objects.get(id=pk).delete()
    return HttpResponseRedirect("/carousel")


@login_required
@user_type_required("Staff")
def infrastructure(request):
    if (
        request.user.is_superuser
        or "banner_image_view" in request.permissions
        or "banner_image_add" in request.permissions
    ):
        try:
            records = Infrastructure.objects.all()
            form = InfrastructureForm()
            if request.method == "POST":
                form = InfrastructureForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/infrastructure")
            context = {"infrastructure": "active", "form": form, "records": records}
            return render(request, "Front_cms/infrastructure.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def infrastructure_edit(request, pk):
    if (
        request.user.is_superuser
        or "banner_image_view" in request.permissions
        or "banner_image_add" in request.permissions
    ):
        try:
            records = Infrastructure.objects.all()
            record = Infrastructure.objects.get(id=pk)
            form = InfrastructureForm(instance=record)
            if request.method == "POST":
                form = InfrastructureForm(request.POST, request.FILES, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/infrastructure")
            context = {"form": form, "records": records, "infrastructure": "active"}
            return render(request, "Front_cms/infrastructure_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def infrastructure_delete(request, pk):
    Infrastructure.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/infrastructure")


@login_required
@user_type_required("Staff")
def event(request):
    if (
        request.user.is_superuser
        or "event_view" in request.permissions
        or "event_add" in request.permissions
    ):
        try:
            records = Events.objects.all()
            form = EventsForm()
            if request.method == "POST":
                form = EventsForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/event")

                else:
                    print(form.errors)
            context = {"form": form, "records": records, "event": "active"}
            return render(request, "Front_cms/event.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def event_edit(request, pk):
    if (
        request.user.is_superuser
        or "event_view" in request.permissions
        or "event_add" in request.permissions
    ):
        try:
            records = Events.objects.all()
            record = Events.objects.get(id=pk)
            form = EventsForm(instance=record)
            if request.method == "POST":
                form = EventsForm(request.POST, request.FILES, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/event")
            context = {"form": form, "records": records, "event": "active"}
            return render(request, "Front_cms/event_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def event_view(request, pk):
    if (
        request.user.is_superuser
        or "event_view" in request.permissions
        or "event_add" in request.permissions
    ):
        try:
            records = Events.objects.all()
            record = Events.objects.get(id=pk)
            form = EventsForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "event": "active",
                "view": True,
            }
            return render(request, "Front_cms/event.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def event_delete(request, pk):
    Events.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/event")


@login_required
@user_type_required("Staff")
def add_event(request):
    if request.user.is_superuser or "event_add" in request.permissions:
        try:
            records = Events.objects.all()
            form = EventsForm()
            if request.method == "POST":
                form = EventsForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/event")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "add_event": "active"}
            return render(request, "Front_cms/add_event.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_staff(request):
    if (
        request.user.is_superuser
        or "school_staff_view" in request.permissions
        or "school_staff_add" in request.permissions
    ):
        try:
            records = SchoolStaff.objects.all()
            form = SchoolStaffForm()
            if request.method == "POST":
                form = SchoolStaffForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/school_staff")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "school_staff": "active"}
            return render(request, "Front_cms/school_staff.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_staff_edit(request, pk):
    if (
        request.user.is_superuser
        or "school_staff_view" in request.permissions
        or "school_staff_add" in request.permissions
    ):
        try:
            records = SchoolStaff.objects.all()
            record = SchoolStaff.objects.get(id=pk)
            form = SchoolStaffForm(instance=record)
            if request.method == "POST":
                form = SchoolHeadsForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/school_staff")
            context = {"form": form, "records": records, "school_head": "active"}
            return render(request, "Front_cms/school_staff_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_staff_delete(request, pk):
    SchoolStaff.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/school_staff")


@login_required
@user_type_required("Staff")
def school_head(request):
    if (
        request.user.is_superuser
        or "school_head_view" in request.permissions
        or "school_head_add" in request.permissions
    ):
        try:
            records = SchoolHeads.objects.all()
            form = SchoolHeadsForm()
            if request.method == "POST":
                form = SchoolHeadsForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/school_head")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "school_head": "active"}
            return render(request, "Front_cms/school_head.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_head_edit(request, pk):
    if (
        request.user.is_superuser
        or "school_head_view" in request.permissions
        or "banner_image_add" in request.permissions
    ):
        try:
            records = SchoolHeads.objects.all()
            record = SchoolHeads.objects.get(id=pk)
            form = SchoolHeadsForm(instance=record)
            if request.method == "POST":
                form = SchoolHeadsForm(request.POST, request.FILES, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/school_head")
            context = {"form": form, "records": records, "school_head": "active"}
            return render(request, "Front_cms/school_head_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_head_delete(request, pk):
    SchoolHeads.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/school_head")


@login_required
@user_type_required("Staff")
def news(request):
    if (
        request.user.is_superuser
        or "news_view" in request.permissions
        or "news_add" in request.permissions
    ):
        try:
            records = News.objects.all()
            form = NewsForm()
            if request.method == "POST":
                form = NewsForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("news")
                else:
                    print(form.errors)

            context = {"form": form, "records": records, "news": "active"}

            return render(request, "Front_cms/news.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
# def news_edit(request,pk):
#     news = News.objects.get(id=pk)
#     return HttpResponseRedirect('/news')


@login_required
@user_type_required("Staff")
def news_edit(request, pk):
    if (
        request.user.is_superuser
        or "news_view" in request.permissions
        or "news_add" in request.permissions
    ):
        try:
            records = News.objects.all()
            record = News.objects.get(id=pk)
            form = NewsForm(instance=record)
            if request.method == "POST":
                form = NewsForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/news")
            context = {"form": form, "records": records, "news": "active"}
            return render(request, "Front_cms/news_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def news_delete(request, pk):
    News.objects.get(id=pk).delete()
    messages.error(request, "Record Deleted Successfully")
    return HttpResponseRedirect("/news")


@login_required
@user_type_required("Staff")
def offers(request):
    if request.user.is_superuser or "offers_view" in request.permissions:
        try:
            records = Offers.objects.all()
            if records:
                record = Offers.objects.all().last()
                form = OffersForm(instance=record)
                if request.method == "POST":
                    form = OffersForm(request.POST, request.FILES, instance=record)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect("/offers")
                context = {"record": record, "offers": "active", "form": form}
                return render(request, "Front_cms/offers.html", context)

            else:
                form = OffersForm()
                if request.method == "POST":
                    form = OffersForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect("/offers")

            context = {"records": records, "offers": "active", "form": form}
            return render(request, "Front_cms/offers.html")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def offers_edit(request, pk):
    if (
        request.user.is_superuser
        or "offers_view" in request.permissions
        or "offers_add" in request.permissions
    ):
        try:
            records = Offers.objects.all()
            record = Offers.objects.get(id=pk)
            form = OffersForm(instance=record)
            if request.method == "POST":
                form = OffersForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/offers")
            context = {"form": form, "records": records, "offers": "active"}
            return render(request, "Front_cms/offers.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def offers_delete(request, pk):
    Offers.objects.get(id=pk).delete()
    return HttpResponseRedirect("/offers")


# -------------------------------  website part end ---------------------------------------


@login_required
@user_type_required("Staff")
def subject_group(request):
    if (
        request.user.is_superuser
        or "subject_group_view" in request.permissions
        or "subject_group_add" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            subject_all = Subjects.objects.all()
            records = SubjectGroup.objects.all()
            form = SubjectGroupForm()
            if request.method == "POST":
                form = SubjectGroupForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/subject_group")
                else:
                    print(form.errors)
            context = {
                "form": form,
                "records": records,
                "subject_group": "active",
                "subject_all": subject_all,
                "class_records": class_records,
            }
            return render(request, "Academics/subject_group.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def subject_group_edit(request, pk):
    if (
        request.user.is_superuser
        or "subject_group_edit" in request.permissions
        or "subject_group_view" in request.permissions
    ):
        if True:
            class_records = Class.objects.all()
            subject_all = Subjects.objects.all()
            records = SubjectGroup.objects.all()
            record = SubjectGroup.objects.get(id=pk)
            lists = record.subject.all()
            list = [data.id for data in lists]
            print("lists", list)
            form = SubjectGroupForm(instance=record)
            if request.method == "POST":
                form = SubjectGroupForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/subject_group")
            context = {
                "form": form,
                "record": record,
                "records": records,
                "subject_group": "active",
                "edit": True,
                "lists": list,
                "subject_all": subject_all,
                "class_records": class_records,
            }
            return render(request, "Academics/subject_group.html", context)
        # except Exception as error:
        #    return render(request,'error.html',{'error':error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def subject_group_view(request, pk):
    if request.user.is_superuser or "subject_group_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            subject_all = Subjects.objects.all()
            records = SubjectGroup.objects.all()
            record = SubjectGroup.objects.get(id=pk)
            lists = record.subject.all()
            list = [data.id for data in lists]
            form = SubjectGroupForm(instance=record)
            context = {
                "subject_all": subject_all,
                "form": form,
                "records": records,
                "record": record,
                "lists": list,
                "SubjectGroup": "active",
                "view": True,
                "class_records": class_records,
            }
            return render(request, "Academics/subject_group.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def subject_group_delete(request, pk):
    if request.user.is_superuser or "subject_group_delete" in request.permissions:
        try:
            SubjectGroup.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/subject_group")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def subjects(request):
    if (
        request.user.is_superuser
        or "subject_view" in request.permissions
        or "subject_add" in request.permissions
    ):
        try:
            records = Subjects.objects.all()
            form = SubjectsForm()
            if request.method == "POST":
                form = SubjectsForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/subjects")
            context = {"form": form, "records": records, "subjects": "active"}
            return render(request, "Academics/subjects.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def subjects_edit(request, pk):
    if request.user.is_superuser or "subject_edit" in request.permissions:
        try:
            records = Subjects.objects.all()
            record = Subjects.objects.get(id=pk)
            form = SubjectsForm(instance=record)
            if request.method == "POST":
                form = SubjectsForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/subjects")
            context = {
                "form": form,
                "records": records,
                "subjects": "active",
                "edit": True,
            }
            return render(request, "Academics/subjects.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def subjects_view(request, pk):
    if request.user.is_superuser or "subject_view" in request.permissions:
        try:
            records = Subjects.objects.all()
            record = Subjects.objects.get(id=pk)
            form = SubjectsForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "subjects": "active",
                "view": True,
            }
            return render(request, "Academics/subjects.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def subjects_delete(request, pk):
    if request.user.is_superuser or "subject_delete" in request.permissions:
        try:
            Subjects.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/subjects")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def Classes(request):
    if (
        request.user.is_superuser
        or "class_view" in request.permissions
        or "class_add" in request.permissions
    ):
        try:
            section_records = Section.objects.all()
            records = Class.objects.all()
            form = ClassForm()

            if request.method == "POST":
                form = ClassForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/Classes")
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "section_records": section_records,
            }
            return render(request, "Academics/Classes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def Classes_edit(request, pk):
    if request.user.is_superuser or "class_edit" in request.permissions:
        try:
            section_records = Section.objects.all()
            records = Class.objects.all()
            record = Class.objects.get(id=pk)
            form = ClassForm(instance=record)
            lists = record.section.all()
            list = [data.id for data in lists]
            if request.method == "POST":
                form = ClassForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/Classes")
            context = {
                "form": form,
                "list": list,
                "records": records,
                "Classes": "active",
                "edit": True,
                "section_records": section_records,
                "record": record,
            }
            return render(request, "Academics/Classes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def Classes_view(request, pk):
    if request.user.is_superuser or "class_view" in request.permissions:
        try:
            records = Class.objects.all()
            record = Class.objects.get(id=pk)
            form = ClassForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "view": True,
            }
            return render(request, "Academics/Classes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def Classes_delete(request, pk):
    if request.user.is_superuser or "class_delete" in request.permissions:
        try:
            Class.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/Classes")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def sections(request):
    if (
        request.user.is_superuser
        or "section_view" in request.permissions
        or "section_add" in request.permissions
    ):
        try:
            records = Section.objects.all()
            print(records)
            form = SectionForm()
            if request.method == "POST":
                form = SectionForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/sections")
                else:
                    print(form.errors)
            context = {"form": form, "sections": "active", "records": records}
            return render(request, "Academics/sections.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def sections_edit(request, pk):
    if request.user.is_superuser or "section_edit" in request.permissions:
        try:
            records = Section.objects.all()
            record = Section.objects.get(id=pk)
            form = SectionForm(instance=record)
            if request.method == "POST":
                form = SectionForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/sections")
            context = {
                "form": form,
                "records": records,
                "sections": "active",
                "edit": True,
            }
            return render(request, "Academics/sections.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def sections_view(request, pk):
    if request.user.is_superuser or "section_view" in request.permissions:
        try:
            records = Section.objects.all()
            record = Section.objects.get(id=pk)
            form = SectionForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "sections": "active",
                "view": True,
            }
            return render(request, "Academics/sections.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def sections_delete(request, pk):
    if request.user.is_superuser or "section_delete" in request.permissions:
        try:
            Section.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/sections")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")

    # class_register


@login_required
@user_type_required("Staff")
def class_register(request):
    if (
        request.user.is_superuser
        or "class_view" in request.permissions
        or "class_add" in request.permissions
    ):
        try:
            section_records = Section.objects.all()
            staff_records = AddStaff.objects.all()
            class_records = Class.objects.all()
            records = ClassRegister.objects.all()
            form = ClassRegisterForm()

            if request.method == "POST":
                form = ClassRegisterForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/class_register")
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "section_records": section_records,
                "staff_records": staff_records,
                "class_records": class_records,
            }
            return render(request, "Academics/Classes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def class_register_edit(request, pk):
    if request.user.is_superuser or "class_edit" in request.permissions:
        try:
            section_records = Section.objects.all()
            records = Class.objects.all()
            record = Class.objects.get(id=pk)
            form = ClassForm(instance=record)
            lists = record.section.all()
            list = [data.id for data in lists]
            if request.method == "POST":
                form = ClassForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/Classes")
            context = {
                "form": form,
                "list": list,
                "records": records,
                "Classes": "active",
                "edit": True,
                "section_records": section_records,
                "record": record,
            }
            return render(request, "Academics/Classes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def class_register_view(request, pk):
    if request.user.is_superuser or "class_view" in request.permissions:
        try:
            records = ClassRegister.objects.all()
            record = ClassRegister.objects.get(id=pk)
            form = ClassRegisterForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "view": True,
            }
            return render(request, "Academics/Classes.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def class_register_delete(request, pk):
    if request.user.is_superuser or "class_delete" in request.permissions:
        try:
            Class.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/Classes")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# School Composition
# @login_required
# @user_type_required("Staff")
# def school_compositions(request):
#     compositions = SchoolComposition.objects.all()
#     return render(
#         request, "Academics/school_composition.html", {"compositions": compositions}
#     )


# School Composition Views
# shool composition
# @login_required
# @user_type_required("Staff")
def school_compositions(request):
    if (
        request.user.is_superuser
        or "school_view" in request.permissions
        or "school_add" in request.permissions
    ):
        form = SchoolCompositionForm()
        school_composition = SchoolCompositions.objects.all()
        if request.method == "POST":
            form = SchoolCompositionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Saved Successfully")
                return redirect("school_compositions")
            else:
                messages.success(request, "Record Saved Successfully")
                return redirect("school_compositions")
        context = {
            "form": form,
            "school_composition": school_composition,
            "school_compositions": "active",
        }
        return render(request, "Structure/school_composition.html", context)

        return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_composition1(request):
    if (
        request.user.is_superuser
        or "class_view" in request.permissions
        or "class_add" in request.permissions
    ):
        try:
            branch_records = Branch.objects.all()
            staff_records = AddStaff.objects.all()
            records = Department.objects.all()
            form = DepartmentForm()

            if request.method == "POST":
                form = DepartmentForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/schools")
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "staff_records": staff_records,
                "branch_records": branch_records,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_composition_edit(request, pk):
    if request.user.is_superuser or "school_edit" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = SchoolForm(instance=record)

            if request.method == "POST":
                form = SchoolForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return redirect("schools")

            context = {
                "form": form,
                "records": School.objects.all(),
                "schools": "active",
                "edit": True,
                "record": record,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_composition_view(request, pk):
    if request.user.is_superuser or "school_view" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = DepartmentForm(instance=record)
            context = {
                "form": form,
                "records": School.objects.all(),
                "school": "active",
                "view": True,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_composition_delete(request, pk):
    if request.user.is_superuser or "school_composition_delete" in request.permissions:
        try:
            School.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/schools")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")

    # level of Education


# @login_required
# @user_type_required("Staff")
def education_levels(request):
    if (
        request.user.is_superuser
        or "education_level_view" in request.permissions
        or "education_levels" in request.permissions
    ):
        form = EducationLevelForm()
        education_level = EducationLevel.objects.all()
        composition = SchoolCompositions.objects.all()
        if request.method == "POST":
            form = EducationLevelForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Saved Successfully")
                return redirect("education_levels")
            else:
                messages.success(request, "Record Saved Successfully")
                return redirect("education_levels")
        context = {
            "form": form,
            "education_level": education_level,
            "composition": composition,
            "school_compositions": "active",
        }
        return render(request, "Structure/education_level.html", context)

        return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def education_level1(request):
    if (
        request.user.is_superuser
        or "class_view" in request.permissions
        or "class_add" in request.permissions
    ):
        try:
            branch_records = Branch.objects.all()
            staff_records = AddStaff.objects.all()
            records = Department.objects.all()
            form = DepartmentForm()

            if request.method == "POST":
                form = DepartmentForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/education_levels")
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "staff_records": staff_records,
                "branch_records": branch_records,
            }
            return render(request, "Structure/education_level.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def education_level_edit(request, pk):
    if request.user.is_superuser or "school_edit" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = SchoolForm(instance=record)

            if request.method == "POST":
                form = SchoolForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return redirect("education_levels")

            context = {
                "form": form,
                "records": School.objects.all(),
                "schools": "active",
                "edit": True,
                "record": record,
            }
            return render(request, "Structure/education_level.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def education_level_view(request, pk):
    if request.user.is_superuser or "school_view" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = DepartmentForm(instance=record)
            context = {
                "form": form,
                "records": School.objects.all(),
                "school": "active",
                "view": True,
            }
            return render(request, "Structure/education_level.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def education_level_delete(request, pk):
    if request.user.is_superuser or "education_level_delete" in request.permissions:
        try:
            School.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/schools")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Structure
# dept
# @login_required
# @user_type_required("Staff")
# def departments(request):
#     if (
#         request.user.is_superuser
#         or "department_view" in request.permissions
#         or "department_add" in request.permissions
#     ):
#         try:
#             records = Department.objects.all()
#             form = DepartmentForm()

#             if request.method == "POST":
#                 form = DepartmentForm(request.POST)
#                 if form.is_valid():
#                     form.save()
#                     messages.success(request, "Record Saved Successfully")
#                     return redirect("departments")

#             context = {"form": form, "records": records, "departments": "active"}
#             return render(request, "Structure/departments.html", context)
#         except Exception as error:
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")


# @login_required
# @user_type_required("Staff")
# def department1(request):
#     if (
#         request.user.is_superuser
#         or "class_view" in request.permissions
#         or "class_add" in request.permissions
#     ):
#         try:
#             branch_records = Branch.objects.all()
#             staff_records = AddStaff.objects.all()
#             records = Department.objects.all()
#             form = DepartmentForm()

#             if request.method == "POST":
#                 form = DepartmentForm(request.POST)
#                 if form.is_valid():
#                     form.save()
#                     messages.success(request, "Record Saved Successfully")
#                     return HttpResponseRedirect("/Classes")
#             context = {
#                 "form": form,
#                 "records": records,
#                 "Classes": "active",
#                 "staff_records": staff_records,
#                 "branch_records": branch_records,
#             }
#             return render(request, "Structure/department1.html", context)
#         except Exception as error:
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")


# @login_required
# @user_type_required("Staff")
# def department_edit(request, pk):
#     if request.user.is_superuser or "department_edit" in request.permissions:
#         try:
#             record = get_object_or_404(Department, id=pk)
#             form = DepartmentForm(instance=record)

#             if request.method == "POST":
#                 form = DepartmentForm(request.POST, instance=record)
#                 if form.is_valid():
#                     form.save()
#                     messages.warning(request, "Record Updated Successfully")
#                     return redirect("departments")

#             context = {
#                 "form": form,
#                 "records": Department.objects.all(),
#                 "departments": "active",
#                 "edit": True,
#                 "record": record,
#             }
#             return render(request, "Structure/departments.html", context)
#         except Exception as error:
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")


# @login_required
# @user_type_required("Staff")
# def department_view(request, pk):
#     if request.user.is_superuser or "department_view" in request.permissions:
#         try:
#             record = get_object_or_404(Department, id=pk)
#             form = DepartmentForm(instance=record)
#             context = {
#                 "form": form,
#                 "records": Department.objects.all(),
#                 "departments": "active",
#                 "view": True,
#             }
#             return render(request, "Structure/departments.html", context)
#         except Exception as error:
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")


# @login_required
# @user_type_required("Staff")
# def department_delete(request, pk):
#     if request.user.is_superuser or "department_delete" in request.permissions:
#         try:
#             Department.objects.get(id=pk).delete()
#             messages.error(request, "Record Deleted Successfully")
#             return HttpResponseRedirect("/departments")
#         except Exception as error:
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")

# Branch


@login_required
@user_type_required("Staff")
def branch(request):
    if (
        request.user.is_superuser
        or "branch_view" in request.permissions
        or "branch_add" in request.permissions
    ):
        try:
            form = BranchForm()
            branches = Branch.objects.all()
            if request.method == "POST":
                form = BranchForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("branch")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("branch")
            context = {"form": form, "branches": branches, "branch": "active"}
            return render(request, "Structure/branch.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def branch1(request):
    if (
        request.user.is_superuser
        or "department_view" in request.permissions
        or "department_add" in request.permissions
    ):
        try:
            records = Branch.objects.all()
            form = BranchForm()

            if request.method == "POST":
                form = BranchForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("branch")

            context = {"form": form, "records": records, "departments": "active"}
            return render(request, "Structure/departments.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def branch_edit(request, pk):
    if request.user.is_superuser or "department_edit" in request.permissions:
        try:
            record = get_object_or_404(Branch, id=pk)
            form = BranchForm(instance=record)

            if request.method == "POST":
                form = BranchForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return redirect("branch")

            context = {
                "form": form,
                "records": Branch.objects.all(),
                "branch": "active",
                "edit": True,
                "record": record,
            }
            return render(request, "Structure/branch.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def branch_view(request, pk):
    if request.user.is_superuser or "department_view" in request.permissions:
        try:
            record = get_object_or_404(Department, id=pk)
            form = DepartmentForm(instance=record)
            context = {
                "form": form,
                "records": Department.objects.all(),
                "departments": "active",
                "view": True,
            }
            return render(request, "Structure/departments.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def branch_delete(request, pk):
    if request.user.is_superuser or "department_delete" in request.permissions:
        try:
            Department.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/branch")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")

    # school


# @login_required
# @user_type_required("Staff")
# def schools(request):
#     if (
#         request.user.is_superuser
#         or "school_view" in request.permissions
#         or "school_add" in request.permissions
#     ):
#         try:
#             form = SchoolForm()
#             schools = School.objects.all()
#             if request.method == "POST":
#                 form = SchoolForm(request.POST)
#                 if form.is_valid():
#                     form.save()
#                     messages.success(request, "Record Saved Successfully")
#                     return redirect("schools")
#                 else:
#                     messages.success(request, "Record Saved Successfully")
#                     return redirect("schools")
#             context = {"form": form, "schools": schools, "school": "active"}
#             return render(request, "Structure/school.html", context)
#         except Exception as error:
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")


# views.py
@login_required
@user_type_required("Staff")
def schools(request):
    try:
        form = SchoolForm()
        schools = School.objects.all()
        school_account = None
        if request.method == "POST":
            form = SchoolForm(request.POST)
            if form.is_valid():
                school_instance = form.save()
                school_account = create_school_account(school_instance)

                messages.success(request, "Record Saved Successfully")
                return redirect("schools")
            else:
                messages.success(request, "Record Saved Successfully")
                return redirect("schools")

        context = {
            "form": form,
            "schools": schools,
            "school_account": school_account,
            "school": "active",
        }
        return render(request, "Structure/school.html", context)

    except Exception as error:
        return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school1(request):
    if (
        request.user.is_superuser
        or "class_view" in request.permissions
        or "class_add" in request.permissions
    ):
        try:
            branch_records = Branch.objects.all()
            staff_records = AddStaff.objects.all()
            records = Department.objects.all()
            form = DepartmentForm()

            if request.method == "POST":
                form = DepartmentForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/schools")
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "staff_records": staff_records,
                "branch_records": branch_records,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_edit(request, pk):
    if request.user.is_superuser or "school_edit" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = SchoolForm(instance=record)

            if request.method == "POST":
                form = SchoolForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return redirect("schools")

            context = {
                "form": form,
                "records": School.objects.all(),
                "schools": "active",
                "edit": True,
                "record": record,
            }
            return render(request, "Structure/school_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_view(request, pk):
    if request.user.is_superuser or "school_view" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = School(instance=record)
            context = {
                "form": form,
                "records": School.objects.all(),
                "school": "active",
                "view": True,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_delete(request, pk):
    if request.user.is_superuser or "school_delete" in request.permissions:
        try:
            School.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/schools")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")

    # shool year


@login_required
def school_years(request):
    if (
        request.user.is_superuser
        or "school_view" in request.permissions
        or "school_add" in request.permissions
    ):
        form = SchoolYearForm()
        school_years = SchoolYear.objects.all()
        school_terms = Term.objects.all()
        print(f"school years {school_years}")
        if request.method == "POST":
            form = SchoolYearForm(request.POST)
            print(f"data {form.data}")
            if form.is_valid():
                form.save()
                messages.success(request, "Record Saved Successfully")
                return redirect("school_years")
            else:
                messages.error(request, "Record not saved")
                return redirect("school_years")
        context = {
            "form": form,
            "school_years": school_years,
            "school_terms": school_terms,
            "school_year": "active",
        }
        return render(request, "Structure/school_year.html", context)

        # return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# @login_required
# @user_type_required("Staff")
# def school_year(request):
#     if (
#         request.user.is_superuser
#         or "class_view" in request.permissions
#         or "class_add" in request.permissions
#     ):
#         try:
#             branch_records = Branch.objects.all()
#             staff_records = AddStaff.objects.all()
#             records = Department.objects.all()
#             form = DepartmentForm()

#             if request.method == "POST":
#                 form = DepartmentForm(request.POST)
#                 if form.is_valid():
#                     form.save()
#                     messages.success(request, "Record Saved Successfully")
#                     return HttpResponseRedirect("/school_years")
#             context = {
#                 "form": form,
#                 "records": records,
#                 "Classes": "active",
#                 "staff_records": staff_records,
#                 "branch_records": branch_records,
#             }
#             return render(request, "Structure/school.html", context)
#         except Exception as error:
#             return render(request, "error.html", {"error": error})
#     else:
#         return redirect("dashboard")


def school_year1(request):
    if (
        request.user.is_superuser
        or "school_view" in request.permissions
        or "school_add" in request.permissions
    ):
        form = SchoolYearForm()
        school_years_data = SchoolYear.objects.all()
        school_terms = Term.objects.all()

        if request.method == "POST":
            form = SchoolYearForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Saved Successfully")
                return redirect("school_years")
            else:
                messages.success(request, "Record Not Saved. Please check the form.")
                return redirect("school_years")

        context = {
            "form": form,
            "school_years": school_years_data,
            "school_terms": school_terms,
            "school_years_active": "active",
        }
        return render(request, "Structure/school_year1.html", context)
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_year_edit(request, pk):
    if request.user.is_superuser or "school_edit" in request.permissions:
        try:
            record = get_object_or_404(SchoolYear, id=pk)
            form = SchoolYearForm(instance=record)

            if request.method == "POST":
                form = SchoolYearForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return redirect("school_years")

            context = {
                "form": form,
                "records": SchoolYear.objects.all(),
                "schools": "active",
                "edit": True,
                "record": record,
            }
            return render(request, "Structure/school_year.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_year_view(request, pk):
    if request.user.is_superuser or "school_view" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = SchoolYearForm(instance=record)
            context = {
                "form": form,
                "records": SchoolYear.objects.all(),
                "school": "active",
                "view": True,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_year_delete(request, pk):
    if request.user.is_superuser or "school_year_delete" in request.permissions:
        try:
            SchoolYear.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/school_years")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")

    # shool year


@login_required
# @user_type_required("Staff")
def school_terms(request):
    if (
        request.user.is_superuser
        or "school_terms_view" in request.permissions
        or "school_terms_add" in request.permissions
    ):
        try:
            form = TermForm()
            school_term = Term.objects.all()
            if request.method == "POST":
                form = TermForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("school_terms")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("school_terms")
            context = {"form": form, "school_term": school_term, "school": "active"}
            return render(request, "Structure/school_term.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_term1(request):
    if (
        request.user.is_superuser
        or "class_view" in request.permissions
        or "class_add" in request.permissions
    ):
        try:
            branch_records = Branch.objects.all()
            staff_records = AddStaff.objects.all()
            records = Department.objects.all()
            form = DepartmentForm()

            if request.method == "POST":
                form = DepartmentForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/school_terms")
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "staff_records": staff_records,
                "branch_records": branch_records,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_term_edit(request, pk):
    if request.user.is_superuser or "school_edit" in request.permissions:
        try:
            record = get_object_or_404(Term, id=pk)
            form = TermForm(instance=record)

            if request.method == "POST":
                form = TermForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return redirect("school_terms")

            context = {
                "form": form,
                "records": Term.objects.all(),
                "school_terms": "active",
                "edit": True,
                "record": record,
            }
            return render(request, "Structure/school_term.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_term_view(request, pk):
    if request.user.is_superuser or "school_view" in request.permissions:
        try:
            record = get_object_or_404(Term, id=pk)
            form = TermForm(instance=record)
            context = {
                "form": form,
                "records": Term.objects.all(),
                "school": "active",
                "view": True,
            }
            return render(request, "Structure/school_term.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def school_term_delete(request, pk):
    if request.user.is_superuser or "school_delete" in request.permissions:
        try:
            Term.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/school_terms")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")

    # Grading System


@login_required
# @user_type_required("Staff")
def grading_systems(request):
    if (
        request.user.is_superuser
        or "school_view" in request.permissions
        or "school_add" in request.permissions
    ):
        try:
            form = GradingSystemForm()
            grading_system = GradingSystem.objects.all()
            if request.method == "POST":
                form = GradingSystemForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("grading_systems")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("grading_systems")
            context = {
                "form": form,
                "grading_system": grading_system,
                "school": "active",
            }
            return render(request, "Academics/grading_system.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def grading_system1(request):
    if (
        request.user.is_superuser
        or "class_view" in request.permissions
        or "class_add" in request.permissions
    ):
        try:
            branch_records = Branch.objects.all()
            staff_records = AddStaff.objects.all()
            records = Department.objects.all()
            form = DepartmentForm()

            if request.method == "POST":
                form = DepartmentForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/schools")
            context = {
                "form": form,
                "records": records,
                "Classes": "active",
                "staff_records": staff_records,
                "branch_records": branch_records,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def grading_system_edit(request, pk):
    if request.user.is_superuser or "school_edit" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = SchoolForm(instance=record)

            if request.method == "POST":
                form = SchoolForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return redirect("school_term")

            context = {
                "form": form,
                "records": School.objects.all(),
                "schools": "active",
                "edit": True,
                "record": record,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def grading_system_view(request, pk):
    if request.user.is_superuser or "school_view" in request.permissions:
        try:
            record = get_object_or_404(School, id=pk)
            form = DepartmentForm(instance=record)
            context = {
                "form": form,
                "records": School.objects.all(),
                "school": "active",
                "view": True,
            }
            return render(request, "Structure/school.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def grading_system_delete(request, pk):
    if request.user.is_superuser or "school_delete" in request.permissions:
        try:
            School.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/schools")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Education Level Views
@login_required
@user_type_required("Staff")
def EducationLevelsListView(request):
    levels = EducationLevel.objects.all()
    return render(request, "Academics/education_levels_list.html", {"levels": levels})


@login_required
@user_type_required("Staff")
def EducationLevelDetailView(request, pk):
    level = get_object_or_404(EducationLevel, pk=pk)
    return render(request, "Academics/education_level_detail.html", {"level": level})


@login_required
@user_type_required("Staff")
def EducationLevelCreateView(request):
    if request.method == "POST":
        form = EducationLevelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Education Level added successfully.")
            return HttpResponseRedirect("/education_levels")
    else:
        form = EducationLevelForm()

    return render(request, "Academics/education_level_form.html", {"form": form})


@login_required
@user_type_required("Staff")
def EducationLevelUpdateView(request, pk):
    level = get_object_or_404(EducationLevel, pk=pk)

    if request.method == "POST":
        form = EducationLevelForm(request.POST, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, "Education Level updated successfully.")
            return HttpResponseRedirect("/education_levels")
    else:
        form = EducationLevelForm(instance=level)

    return render(request, "Academics/education_level_form.html", {"form": form})


@login_required
@user_type_required("Staff")
def EducationLevelDeleteView(request, pk):
    level = get_object_or_404(EducationLevel, pk=pk)

    if request.method == "POST":
        level.delete()
        messages.success(request, "Education Level deleted successfully.")
        return HttpResponseRedirect("/education_levels")

    return render(
        request, "Academics/education_level_confirm_delete.html", {"level": level}
    )


@login_required
@user_type_required("Staff")  # Download Center
def upload_content(request):
    if (
        request.user.is_superuser
        or "upload_content_view" in request.permissions
        or "upload_content_add" in request.permissions
    ):
        try:
            class_records = Class.objects.all()
            form = UploadContentForm()
            contents = UploadContent.objects.all()
            if request.method == "POST":
                form = UploadContentForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    print(form.errors)
                    messages.success(request, "Record Saved Successfully")
                    return redirect("upload_content")
                else:
                    messages.success(request, "Record Saved Successfully")
                    return redirect("upload_content")
            context = {
                "form": form,
                "contents": contents,
                "upload_content": "active",
                "class_records": class_records,
            }
            return render(request, "Download_center/upload_content.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def upload_content_edit(request, pk):
    if request.user.is_superuser or "upload_content_edit" in request.permissions:
        try:
            class_records = Class.objects.all()
            contents = UploadContent.objects.all()
            content = UploadContent.objects.get(id=pk)
            form = UploadContentForm(instance=content)
            if request.method == "POST":
                form = UploadContentForm(request.POST, instance=content)
                if form.is_valid():
                    form.save()

                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/upload_content")
            context = {
                "form": form,
                "contents": contents,
                "upload_content": "active",
                "content": content,
                "edit": True,
                "class_records": class_records,
            }
            return render(request, "Download_center/upload_content.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def upload_content_delete(request, pk):
    if request.user.is_superuser or "upload_content_delete" in request.permissions:
        try:
            UploadContent.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/upload_content")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


#  home work


@login_required
@user_type_required("Staff")
def add_homework(request):
    if (
        request.user.is_superuser
        or "homework_view" in request.permissions
        or "homework_add" in request.permissions
    ):
        try:
            records = AddHomeWork.objects.all()
            form = AddHomeWorkForm()
            if request.method == "POST":
                form = AddHomeWorkForm(request.POST, request.FILES)
                if form.is_valid():
                    homework = form.save(commit=False)
                    homework.created_by = request.user
                    homework.save()
                    student = StudentAdmission.objects.filter(
                        Class=request.POST.get("Class"),
                        section=request.POST.get("section"),
                        session=request.Session,
                    )
                    for data in student:
                        AssingHomeWork.objects.get_or_create(
                            home_work_id=homework.pk,
                            student_id=data.id,
                            status="Pending",
                        )
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/add_homework")
                else:
                    print(form.errors)
            context = {"form": form, "records": records, "add_homework": "active"}
            return render(request, "Home_work/add_homework.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_homework_view(request, pk):
    if request.user.is_superuser or "homework_view" in request.permissions:
        try:
            records = AddHomeWork.objects.all()
            record = AddHomeWork.objects.get(id=pk)
            recordss = AssingHomeWork.objects.filter(home_work=pk)
            if request.POST.get("save") == "save":
                record.evaluation_date = request.POST.get("evaluation_date")
                student_list = request.POST.getlist("student_ids")
                for data in student_list:
                    obj = recordss.get(id=data)
                    obj.evaluation_date = request.POST.get("evaluation_date")
                    obj.status = "Submitted"
                    obj.save()
                record.save()
                return HttpResponseRedirect("/add_homework")
            context = {
                "record": record,
                "records": records,
                "homework": "active",
                "recordss": recordss,
                "view": True,
            }
            return render(request, "Home_work/add_homework_view.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_homework_edit(request, pk):
    if request.user.is_superuser or "homework_edit" in request.permissions:
        try:
            records = AddHomeWork.objects.all()
            record = AddHomeWork.objects.get(id=pk)
            form = AddHomeWorkForm(instance=record)
            if request.method == "POST":
                form = AddHomeWorkForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/add_homework")
            context = {"form": form, "records": records, "homework": "active"}

            return render(request, "Home_work/add_homework_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def add_homework_delete(request, pk):
    if request.user.is_superuser or "homework_delete" in request.permissions:
        try:
            AddHomeWork.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/add_homework")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


# Front office


@login_required
@user_type_required("Staff")
def visitor_book(request):
    if (
        request.user.is_superuser
        or "visitor_book_view" in request.permissions
        or "visitor_book_add" in request.permissions
    ):
        try:
            records = VisitorBook.objects.all()
            form = VisitorBookForm()
            if request.method == "POST":
                form = VisitorBookForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/visitor_book")
            context = {"form": form, "records": records, "visitor_book": "active"}

            return render(request, "Front_Office/visitor_book.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def visitor_book_edit(request, pk):
    if request.user.is_superuser or "visitor_book_edit" in request.permissions:
        try:
            records = VisitorBook.objects.all()
            record = VisitorBook.objects.get(id=pk)
            form = VisitorBookForm(instance=record)
            if request.method == "POST":
                form = VisitorBookForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/visitor_book")
            context = {
                "form": form,
                "records": records,
                "visitor_book": "active",
                "edit": True,
            }

            return render(request, "Front_Office/visitor_book.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def visitor_book_view(request, pk):
    if request.user.is_superuser or "visitor_book_view" in request.permissions:
        try:
            records = VisitorBook.objects.all()
            record = VisitorBook.objects.get(id=pk)
            form = VisitorBookForm(instance=record)
            context = {
                "form": form,
                "records": records,
                "visitor_book": "active",
                "view": True,
            }
            return render(request, "Front_Office/visitor_book.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def visitor_book_delete(request, pk):
    if request.user.is_superuser or "visitor_book_delete" in request.permissions:
        try:
            VisitorBook.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/visitor_book")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def disabled_staff(request):
    if request.user.is_superuser or "disable_staff_view" in request.permissions:
        try:
            roles = Role.objects.all()
            records = AddStaff.objects.filter(status="Disable")
            if request.method == "POST":
                records = AddStaff.objects.filter(
                    roles=request.POST.get("roles"), status="Disable"
                )
            context = {
                "disabled_staff": "active",
                "roles": roles,
                "records": records,
            }
            return render(request, "Human_Resource/disabled_staff.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def generate_ID_card(request):
    if request.user.is_superuser or "generate_id_card_view" in request.permissions:
        try:
            ID_card_records = StudentId.objects.all()
            class_records = Class.objects.all()
            if request.method == "POST":
                section_records = Section.objects.all()
                classs = request.POST.get("class")
                section = request.POST.get("section")
                id_card = request.POST.get("ID_card")
                records = StudentAdmission.objects.filter(
                    Class=classs,
                    section=section,
                    session=request.Session,
                )
                context = {
                    "generate_ID_card": "active",
                    "ID_card_records": ID_card_records,
                    "class_records": class_records,
                    "classs": int(classs),
                    "section": int(section),
                    "id_card": int(id_card),
                    "records": records,
                    "section_records": section_records,
                }
                return render(request, "Certificate/generate_ID_card.html", context)
            context = {
                "generate_ID_card": "active",
                "ID_card_records": ID_card_records,
                "class_records": class_records,
            }
            return render(request, "Certificate/generate_ID_card.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def print_ID_card(request):
    id_card = StudentId.objects.get(id=request.POST.get("id_card"))
    records = StudentAdmission.objects.filter(id__in=request.POST.getlist("checkbox"))
    context = {"generate_ID_card": "active", "data": id_card, "records": records}
    return render(request, "Certificate/print_ID_card.html", context)


@login_required
@user_type_required("Staff")
def admission_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            if request.method == "POST":
                from_date = request.POST.get("from_date")
                to_date = request.POST.get("to_date")
                filters = {}
                if from_date and to_date:
                    filters["admission_date__range"] = [from_date, to_date]

                records = StudentAdmission.objects.filter(**filters)
                context = {
                    "records": records,
                }
                return render(request, "Reports/admission_report.html", context)

            context = {"student_information_report": "active"}
            return render(request, "Reports/admission_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def balances_fees_report(request):
    if request.user.is_superuser or "search_due_fees_view" in request.permissions:
        try:
            Classs = Class.objects.all()
            if request.method == "POST":
                records = FeesAssign.objects.filter(
                    session=request.Session,
                    student__Class=request.POST.get("class"),
                    student__section=request.POST.get("section"),
                    student__session=request.Session,
                ).exclude(status="fully paid")

                context = {"fees_type": fees_type, "Classs": Classs, "records": records}
                return render(request, "Reports/balances_fees_report.html", context)
            context = {"Classs": Classs, "Finances_report": "active"}
            return render(request, "Reports/balances_fees_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def class_subject_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()

            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                filters = {}
                if classs:
                    filters["Class_id"] = classs

                if section:
                    filters["section_id"] = section

                records = TimeTable.objects.filter(**filters)

                context = {
                    "student_information_report": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                }

                return render(request, "Reports/class_subject_report.html", context)

            context = {
                "student_information_report": "active",
                "class_records": class_records,
                "section_records": section_records,
            }

            return render(request, "Reports/class_subject_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def examinations_report(request):
    if request.user.is_superuser or "exanmination_report_view" in request.permissions:
        try:
            exam_group = examGroup.objects.all()
            class_records = Class.objects.all()
            session_records = Session.objects.all()
            if request.method == "POST":
                exams = AddExamSubject.objects.filter(exam=request.POST.get("exam"))
                student = ExamStudent.objects.filter(
                    Class=request.POST.get("class"),
                    section=request.POST.get("section"),
                    exam=request.POST.get("exam"),
                    exam__session=request.POST.get("session"),
                )
                records = EntryMarks.objects.filter(
                    student__Class=request.POST.get("class"),
                    student__section=request.POST.get("section"),
                    exam=request.POST.get("exam"),
                )
                listt = []
                for data in student:
                    total_mark = 0
                    total = 0
                    mark_list = []
                    results = []
                    for sub in exams:
                        dict = {}
                        mark = EntryMarks.objects.filter(
                            exam_subject=sub, exam_student=data
                        ).last()
                        dic = {}
                        if mark:
                            dic["subject"] = mark.subject
                            total_mark += mark.marks
                            if mark.marks <= sub.marks_min:
                                results.append("Fail")
                                dic["marks"] = f"{mark.marks} (F)"
                            else:
                                results.append("Pass")
                                dic["marks"] = mark.marks
                        else:
                            dic["subject"] = sub.subject
                            dic["marks"] = ""
                            results.append(None)
                        total += sub.marks_max
                        mark_list.append(dic)

                    dict["mark_list"] = mark_list
                    dict["obj"] = data
                    dict["total"] = f"{total_mark}/{int(total)}"
                    dict["percentage"] = int(total_mark * 100 / int(total))
                    dict["result"] = results
                    listt.append(dict)
                context = {
                    "examinations_report": "active",
                    "exam_group": exam_group,
                    "class_records": class_records,
                    "session_records": session_records,
                    "exams": exams,
                    "records": records,
                    "listt": listt,
                }
                return render(request, "Reports/examinations_report.html", context)
            context = {
                "examinations_report": "active",
                "exam_group": exam_group,
                "class_records": class_records,
                "session_records": session_records,
            }
            return render(request, "Reports/examinations_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
@user_type_required("Staff")
def expense_group_report(request):
    if (
        request.user.is_superuser
        or "expense_group_report_view" in request.permissions
        or request.permissions
    ):
        try:
            expense_head_records = ExpenseHead.objects.all()
            if request.method == "POST":
                from_date = request.POST.get("from_date")
                to_date = request.POST.get("to_date")
                expense_head = request.POST.get("expense_head")
                filters = {}
                if from_date and to_date:
                    filters["date__range"] = [from_date, to_date]
                elif from_date:
                    filters["date__gte"] = from_date
                elif to_date:
                    filters["date__lte"] = to_date
                if expense_head:
                    filters["expense_head__id"] = expense_head

                records = AddExpense.objects.filter(**filters)

                expense_totals = {}
                for record in records:
                    expense_head = record.expense_head
                    amount = record.amount
                    if expense_head in expense_totals:
                        expense_totals[expense_head] += amount
                    else:
                        expense_totals[expense_head] = amount

                total_amount = sum(expense_totals.values())

                context = {
                    "expense_head_records": expense_head_records,
                    "expense_group_report": "active",
                    "records": records,
                    "expense_totals": expense_totals,
                    "total_amount": total_amount,
                }
                return render(request, "Reports/expense_group_report.html", context)

            context = {
                "expense_head_records": expense_head_records,
                "Finances_report": "active",
            }
            return render(request, "Reports/expense_group_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def expense_report(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        # Filter expenses based on date range
        expenses = AddExpense.objects.filter(date__range=[from_date, to_date])

        # Calculate grand total
        grand_total = expenses.aggregate(total_amount=models.Sum("amount")).get(
            "total_amount", 0
        )

        context = {
            "expenses": expenses,
            "from_date": from_date,
            "to_date": to_date,
            "grand_total": grand_total,
            "Finances_report": "active",
        }
        return render(request, "Reports/expense_report.html", context)

    return render(request, "Reports/expense_report.html")


@login_required
@user_type_required("Staff")
def fees_collection_report(request):
    roles_rcords = AddStaff.objects.all()
    class_records = Class.objects.all()
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        role = request.POST.get("role")
        filters = {}
        if role:
            filters["created_by"] = role
        if from_date and to_date:
            filters["created_at__range"] = [from_date, to_date]
        if from_date:
            filters["created_at__gte"] = from_date
        if to_date:
            filters["created_at__lte"] = to_date
        records = StudentFess.objects.filter(**filters)
        total_amount = records.aggregate(Sum("paid_amount"))["paid_amount__sum"]
        total_dicount = records.aggregate(Sum("amount_discount"))[
            "amount_discount__sum"
        ]
        total_fine = records.aggregate(Sum("amount_fine"))["amount_fine__sum"]
        print("records", records)
        context = {
            "records": records,
            "class_records": class_records,
            "roles_rcords": roles_rcords,
            "total_amount": total_amount,
            "total_dicount": total_dicount,
            "total_fine": total_fine,
        }
        return render(request, "Reports/fees_collection_report.html", context)

    context = {
        "class_records": class_records,
        "fees_collection_report": "active",
        "Finances_report": "active",
        "roles_rcords": roles_rcords,
    }
    return render(request, "Reports/fees_collection_report.html", context)


@login_required
@user_type_required("Staff")
def Finances_report(request):
    if request.user.is_superuser or "finance_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            if request.method == "POST":
                student_name = request.POST.get("student_name")
                print("student_name", student_name)
                record = StudentAdmission.objects.get(id=student_name)

                fees_records = FeesAssign.objects.filter(
                    student_id=request.POST.get("student_name")
                )
                # fees_discount=FeesTypeDiscount.objects.all()
                fees_discount = DiscountAssign.objects.filter(
                    student=request.POST.get("student_name")
                )

                paid_record = StudentFess.objects.filter(
                    student=request.POST.get("student_name")
                )

                context = {
                    "records": record,
                    "Finances_report": "active",
                    "fees_records": fees_records,
                    "fees_discount": fees_discount,
                    "paid_record": paid_record,
                    "class_records": class_records,
                }
                return render(request, "Reports/Finances_report.html", context)

            context = {"Finances_report": "active", "class_records": class_records}
            return render(request, "Reports/Finances_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
@user_type_required("Staff")
def homework_evaluation_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            if request.method == "POST":
                classs = request.POST.get("Class")
                section = request.POST.get("section")
                subject_groups = request.POST.get("subject_group")
                subject = request.POST.get("subject")
                records = AddHomeWork.objects.filter(
                    Class_id=classs,
                    section_id=section,
                    subject_group_id=subject_groups,
                    subject_id=subject,
                )
                list = []
                for data in records:
                    dict = {}
                    assign_homework = AssingHomeWork.objects.filter(home_work=data)
                    complete = assign_homework.filter(
                        evaluation_date__isnull=False
                    ).count()
                    incompelete = assign_homework.filter(
                        evaluation_date__isnull=True
                    ).count()
                    total_student = assign_homework.count()
                    percentage = int(complete * 100 / total_student)
                    dict["obj"] = data
                    dict["complete"] = complete
                    dict["incomplete"] = incompelete
                    dict["percentage"] = percentage
                    list.append(dict)
                    print(dict)
                print(list)
                context = {
                    "records": records,
                    "class_records": class_records,
                    "list": list,
                }
                return render(
                    request, "Reports/homework_evaluation_report.html", context
                )
            context = {
                "class_records": class_records,
                "student_information_report": "active",
            }
            return render(request, "Reports/homework_evaluation_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def income_group_report(request):
    if (
        request.user.is_superuser
        or "income_group_report_view" in request.permissions
        or request.permissions
    ):
        try:
            income_head_records = Incomehead.objects.all()
            if request.method == "POST":
                from_date = request.POST.get("from_date")
                to_date = request.POST.get("to_date")
                income_head_id = request.POST.get("Income_head")
                filters = {}
                if from_date and to_date:
                    filters["date__range"] = [from_date, to_date]
                elif from_date:
                    filters["date__gte"] = from_date
                elif to_date:
                    filters["date__lte"] = to_date
                if income_head_id:
                    filters["Income_head__id"] = income_head_id

                records = AddIncome.objects.filter(**filters)

                income_totals = {}
                for record in records:
                    income_head = record.Income_head
                    amount = record.amount
                    if income_head in income_totals:
                        income_totals[income_head] += int(amount)
                    else:
                        income_totals[income_head] = int(amount)

                total_amount = sum(income_totals.values())

                context = {
                    "income_head_records": income_head_records,
                    "income_group_report": "active",
                    "records": records,
                    "income_totals": income_totals,
                    "total_amount": total_amount,
                }
                return render(request, "Reports/income_group_report.html", context)

            context = {
                "income_head_records": income_head_records,
                "Finances_report": "active",
            }
            return render(request, "Reports/income_group_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def income_report(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        income = AddIncome.objects.filter(date__range=[from_date, to_date])

        grand_total = income.aggregate(total_amount=models.Sum("amount")).get(
            "total_amount", 0
        )

        context = {
            "income": income,
            "from_date": from_date,
            "to_date": to_date,
            "grand_total": grand_total,
            "Finances_report": "active",
        }
        return render(request, "Reports/income_report.html", context)

    return render(request, "Reports/income_report.html")


# @login_required
# @user_type_required("Staff")
# def net_profit_loss_report(request):
#     if request.method == "POST":
#         from_date = request.POST.get("from_date")
#         to_date = request.POST.get("to_date")

#         income = AddIncome.objects.filter(date__range=[from_date, to_date])
#         net_result = calculate_net_gains_losses()

#         grand_total = income.aggregate(total_amount=models.Sum("amount")).get(
#             "total_amount", 0
#         )

#         context = {
#             "income": income,
#             "net_result": net_result,
#             "from_date": from_date,
#             "to_date": to_date,
#             "grand_total": grand_total,
#             "Finances_report": "active",
#             "Net_Gains_Losses_report": "active",
#         }
#         return render(request, "Reports/net_profit_loss.html", context)

#     return render(request, "Reports/net_profit_loss.html")

def net_profit_loss_report(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        # Call the function with the date range
        income_total, expense_total, net_result = calculate_net_gains_losses(
            from_date=from_date, to_date=to_date
        )

        context = {
            "income_total": income_total,
            "expense_total": expense_total,
            "net_result": net_result,
            "from_date": from_date,
            "to_date": to_date,
        }
        return render(request, "Reports/net_profit_loss.html", context)

    return render(request, "Reports/net_profit_loss.html")


@login_required
@user_type_required("Staff")
def Report_payroll_report(request):
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        filters = {}
        if from_date and to_date:
            filters["payment_date__range"] = [from_date, to_date]
        records = PayrollSummary.objects.filter(**filters)

        grand_total_basic_salary = records.aggregate(
            total_amount=models.Sum("basic_salary")
        ).get("total_amount", 0)
        grand_total_net_salary = records.aggregate(
            total_amount=models.Sum("net_salary")
        ).get("total_amount", 0)
        grand_total_earning = records.aggregate(total_amount=models.Sum("earning")).get(
            "total_amount", 0
        )
        grand_total_deduction = records.aggregate(
            total_amount=models.Sum("deduction")
        ).get("total_amount", 0)
        grand_total_gross_salary = records.aggregate(
            total_amount=models.Sum("gross_salary")
        ).get("total_amount", 0)
        grand_total_Tax = records.aggregate(total_amount=models.Sum("Tax")).get(
            "total_amount", 0
        )

        context = {
            "records": records,
            "grand_total_basic_salary": grand_total_basic_salary,
            "grand_total_net_salary": grand_total_net_salary,
            "grand_total_earning": grand_total_earning,
            "grand_total_deduction": grand_total_deduction,
            "grand_total_gross_salary": grand_total_gross_salary,
            "grand_total_Tax": grand_total_Tax,
        }
        return render(request, "Reports/Report_payroll_report.html", context)
    context = {"Finances_report": "active"}
    return render(request, "Reports/Report_payroll_report.html", context)


@login_required
@user_type_required("Staff")
def sibling_report(request):
    if request.user.is_superuser or "sibling_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            section_records = Section.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                filters = {}
                if classs:
                    filters["Class_id"] = classs
                if section:
                    filters["section_id"] = section
                records = StudentAdmission.objects.filter(**filters)
                context = {
                    "student_details": "active",
                    "records": records,
                    "class_records": class_records,
                    "section_records": section_records,
                }
                return render(request, "Reports/sibling_report.html", context)
            context = {
                "student_information_report": "active",
                "class_records": class_records,
                "section_records": section_records,
            }
            return render(request, "Reports/sibling_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_gender_ratio_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            # Retrieve the student admission data
            student_admissions = StudentAdmission.objects.all()
            # Perform aggregation to calculate the counts of boys and girls per class/section
            gender_counts = student_admissions.values("Class", "section").annotate(
                total_boys=Count("id", filter=Q(gender="Male")),
                total_girls=Count("id", filter=Q(gender="Female")),
                total_students=Count("id"),
            )

            # Calculate the boys-girls ratio for each class/section
            print(gender_counts)

            # Calculate the grand total
            grand_total_boys = gender_counts.aggregate(Sum("total_boys"))[
                "total_boys__sum"
            ]
            grand_total_girls = gender_counts.aggregate(Sum("total_girls"))[
                "total_girls__sum"
            ]
            grand_total_students = gender_counts.aggregate(Sum("total_students"))[
                "total_students__sum"
            ]

            context = {
                "student_information_report": "active",
                "gender_counts": gender_counts,
                "grand_total_boys": grand_total_boys,
                "grand_total_girls": grand_total_girls,
                "grand_total_students": grand_total_students,
            }

            return render(request, "Reports/student_gender_ratio_report.html", context)

        except Exception as error:
            return render(request, "error.html", {"error": error})

    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def student_teacher_ratio_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            # Retrieve the student admission data
            student_admissions = StudentAdmission.objects.all()

            # Perform aggregation to calculate the counts of students per class/section
            student_counts = student_admissions.values("Class", "section").annotate(
                total_students=Count("id")
            )

            # Retrieve the assigned teachers data
            assigned_teachers = AssignClassTeacher.objects.all()

            # Perform aggregation to calculate the counts of assigned teachers per class/section
            teacher_counts = assigned_teachers.values("Class", "section").annotate(
                total_assigned_teachers=Count("class_teacher", distinct=True)
            )

            # Combine the student and teacher counts per class/section
            class_section_counts = {}
            grand_total = {"total_students": 0, "total_assigned_teachers": 0}

            for student_count in student_counts:
                class_key = (student_count["Class"], student_count["section"])
                class_section_counts[class_key] = {
                    "Class": student_count["Class"],
                    "section": student_count["section"],
                    "total_students": student_count["total_students"],
                    "total_assigned_teachers": 0,
                }
                grand_total["total_students"] += student_count["total_students"]

            for teacher_count in teacher_counts:
                class_key = (teacher_count["Class"], teacher_count["section"])
                if class_key in class_section_counts:
                    class_section_counts[class_key][
                        "total_assigned_teachers"
                    ] = teacher_count["total_assigned_teachers"]
                else:
                    class_section_counts[class_key] = {
                        "Class": teacher_count["Class"],
                        "section": teacher_count["section"],
                        "total_students": 0,
                        "total_assigned_teachers": teacher_count[
                            "total_assigned_teachers"
                        ],
                    }
                grand_total["total_assigned_teachers"] += teacher_count[
                    "total_assigned_teachers"
                ]

            # Calculate the student-teacher ratio for each class/section
            for count in class_section_counts.values():
                total_students = count["total_students"]
                total_assigned_teachers = count["total_assigned_teachers"]
                if total_assigned_teachers > 0:
                    count[
                        "student_teacher_ratio"
                    ] = f"{total_students}:{total_assigned_teachers}"
                else:
                    count["student_teacher_ratio"] = "N/A"

            # Calculate the grand total ratio
            grand_total_students = grand_total["total_students"]
            grand_total_assigned_teachers = grand_total["total_assigned_teachers"]
            if grand_total_assigned_teachers > 0:
                grand_total[
                    "student_teacher_ratio"
                ] = f"{grand_total_students}:{grand_total_assigned_teachers}"
            else:
                grand_total["student_teacher_ratio"] = "N/A"

            context = {
                "class_section_counts": class_section_counts,
                "grand_total": grand_total,
                "student_information_report": "active",
            }

            return render(request, "Reports/student_teacher_ratio_report.html", context)

        except Exception as error:
            return render(request, "error.html", {"error": error})

    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def student_profile_report(request):
    if request.user.is_superuser or "student_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            if request.method == "POST":
                from_date = request.POST.get("from_date")
                to_date = request.POST.get("to_date")
                classs = request.POST.get("class")
                section = request.POST.get("section")

                filters = {}
                if from_date and to_date:
                    filters["admission_date__range"] = [from_date, to_date]

                elif classs:
                    filters["Class_id"] = classs

                elif section:
                    filters["section_id"] = section

                records = StudentAdmission.objects.filter(**filters)
                context = {
                    "records": records,
                    "class_records": class_records,
                }
                return render(request, "Reports/student_profile_report.html", context)

            context = {
                "class_records": class_records,
                "student_information_report": "active",
            }
            return render(request, "Reports/student_profile_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def send_email(request):
    if request.user.is_superuser or "email_view" in request.permissions:
        try:
            form = SendEmailForm()
            forms = Role.objects.all()
            classes = Class.objects.all()
            sections = Section.objects.all()
            email = SendEmail.objects.all()
            emails = None  # Initialize classs variable
            roles_records = Role.objects.all()

            if request.method == "POST":
                # Get the form data
                title = request.POST.get("title")
                message = request.POST.get("message")
                recipients = request.POST.getlist("noties_all[]")
                attachments = request.FILES.getlist("attachment")
                class_id = request.POST.get("class_id")
                selected_sections = request.POST.getlist("sectionss")
                print("selected_sections", selected_sections)
                individual_send_by = request.POST.get("individual_send_by")

                # Print the values for debugging
                print("Class ID:", class_id)
                print("Selected Sections:", selected_sections)

                # selected_class = Class.objects.get(id=class_id)
                # Retrieve selected class and sections

                # classs = Class.objects.get(id=class_id)
                # Construct the email subject and message
                email_subject = "Title: {}".format(title)
                email_message = """
                Message: {}
                Regards,
                Yours bharathbrands
                """.format(
                    message
                )

                if recipients and recipients[0].isdigit():
                    EmailSmsLog.objects.create(
                        Title=title,
                        send_by="Email",
                        sent_to="Group",
                        created_by=request.user,
                    )
                    for i in recipients:
                        if i.isdigit():
                            user_email = AddStaff.objects.filter(
                                roles=int(i)
                            ).values_list("email", flat=True)
                            send_email_notification(
                                email_subject, email_message, user_email, attachments
                            )
                else:
                    for recipient in recipients:
                        EmailSmsLog.objects.create(
                            Title=title,
                            send_by="Email",
                            sent_to="Group",
                            created_by=request.user,
                        )
                        if recipient == "student":
                            # Retrieve student email addresses and add them to recipient_emails
                            emails = (
                                StudentAdmission.objects.exclude(email__isnull=True)
                                .exclude(email__exact="")
                                .values_list("email", flat=True)
                            )
                            send_email_notification(
                                email_subject, email_message, emails, attachments
                            )
                        elif recipient == "parent":
                            # Retrieve parent email addresses and add them to recipient_emails
                            emails = (
                                StudentAdmission.objects.exclude(
                                    guardian_email__isnull=True
                                )
                                .exclude(guardian_email__exact="")
                                .values_list("guardian_email")
                            )

                            send_email_notification(
                                email_subject, email_message, emails, attachments
                            )
                if class_id and selected_sections:
                    EmailSmsLog.objects.create(
                        Title=title,
                        send_by="Email",
                        sent_to="Class",
                        created_by=request.user,
                    )
                    emails = (
                        StudentAdmission.objects.filter(
                            Class=class_id, section__in=selected_sections
                        )
                        .exclude(email__isnull=True)
                        .exclude(email__exact="")
                        .values_list("email", flat=True)
                    )
                    send_email_notification(
                        email_subject, email_message, emails, attachments
                    )

                return redirect("/send_email")

            context = {
                "form": form,
                "forms": forms,
                "classes": classes,
                # 'classs':classs,
                "sections": sections,
                "email": email,
                "roles_records": roles_records,
                "send_email": "active"
                # 'selected_sections': selected_sections,
                # 'selected_class': selected_class
            }
            return render(request, "Communicate/send_email.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def indvidula_send_mail(request):
    if request.user.is_superuser or "email_view" in request.permissions:
        try:
            if request.method == "POST":
                title = request.POST.get("individual_title")
                message = request.POST.get("individual_message")
                attachments = request.FILES.getlist("individual_attachment")
                subject = "Title: {}".format(title)
                message = """
                Message: {}
                Regards,
                Yours bharathbrands
                """.format(
                    message
                )
                mail_for = MailSearchTemp.objects.all()
                emails = []
                for data in mail_for:
                    if data.type == "Student":
                        emails.append(data.Student.email)
                    elif data.type == "Guardian":
                        emails.append(data.Student.guardian_email)
                    elif data.type == "Staff":
                        emails.append(data.Staff.email)
                send_email_notification(subject, message, emails, attachments)

                return redirect("/indvidula_send_mail")
            roles_records = Role.objects.all()
            MailSearchTemp.objects.all().delete()
            context = {"roles_records": roles_records, "send_email": "active"}
            return render(request, "Communicate/indvidula_send_mail.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def get_sections(request):
    class_id = request.GET.get("class_id")
    sections = Section.objects.filter(class__id=class_id)
    section_list = []

    for section_obj in sections:
        section_data = {"id": section_obj.id, "section_name": section_obj.section_name}
        section_list.append(section_data)

    return JsonResponse(section_list, safe=False)


@login_required
@user_type_required("Staff")
def syllabus_status_report(request):
    if request.user.is_superuser or "lesson_plan_report_view" in request.permissions:
        try:
            class_records = Class.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                subject_groups = request.POST.get("subject_group")
                subject = SubjectGroup.objects.filter(id=subject_groups).last()
                records = []
                chart_percent = []
                for sub in subject.subject.all():
                    subj = {}
                    lesson_records = Lesson.objects.filter(
                        Class_id=classs, section_id=section, subject=sub.id
                    )
                    record = []
                    total = 0
                    percent = 1
                    for data in lesson_records:
                        dict = {}
                        topic_records = topic.objects.filter(lesson_name=data.id)
                        if topic_records.count() > 0:
                            percentage = int(
                                topic_records.filter(status="complete").count()
                                * 100
                                / topic_records.count()
                            )
                            percent *= percentage / 100
                            total += 1
                            dict["percentage"] = f"{percentage}% Complete"
                        else:
                            dict["percentage"] = "No Status"
                        dict["lesson"] = data
                        dict["topic"] = topic_records
                        record.append(dict)
                    if total > 0:
                        chart_percent.append([percent * 100, sub.subject_name])
                        subj["percentage"] = f"{percent*100}% Complete"
                    else:
                        chart_percent.append([0, sub.subject_name])
                        subj["percentage"] = "0% Complete"
                    subj["subject"] = sub
                    subj["record"] = record
                    records.append(subj)
                context = {
                    "lesson_paln_report": "active",
                    "class_records": class_records,
                    "records": records,
                    "chart_percent": chart_percent,
                }
                return render(request, "Reports/syllabus_status_report.html", context)
            context = {"lesson_paln_report": "active", "class_records": class_records}
            return render(request, "Reports/syllabus_status_report.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html", {"error": error})


@login_required
def student_report_finances_js(request):
    classs = request.GET.get("class_id")
    suction_id = request.GET.get("section_id")
    subject = StudentAdmission.objects.filter(
        Class_id=classs, section_id=suction_id, session=request.Session
    )
    return JsonResponse(data=list(subject.values("id", "first_name")), safe=False)


@login_required
@user_type_required("Staff")
def import_student(request):
    form = StudentAdmissionForm()
    records = StudentAdmission.objects.all()
    if request.method == "POST" and request.FILES["file"]:
        file = request.FILES["file"]
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            admission_no_name = row["admission_no"]
            roll_number = row["roll_number"]
            first_name_1 = row["first_name"]
            Classs = row["Class"]
            section_id = row["section"]
            Father_name_1 = row["Father_name"]
            gender = row["gender"]
            category_1 = row["category"]
            mobile_number = row["mobile_number"]
            student_house = row["student_house"]
            room_number = row["room_number"]
            date_of_birth = row["date_of_birth"]
            hostel = row["hostel"]
            route_list = row["route_list"]
            vehicle_number = row["vehicle_number"]
            last_name_1 = row["last_name"]
            email_1 = row["email"]
            guardian_name_1 = row["guardian_name"]
            guardian_email_1 = row["guardian_email"]
            religion = row["religion"]
            Caste = row["Caste"]
            admission_date = row["admission_date"]
            Blood_group = row["Blood_group"]
            height = row["height"]
            weight = row["weight"]
            as_on_date = row["as_on_date"]
            Father_phone = row["Father_phone"]
            Father_occupation = row["Father_occupation"]
            mother_name = row["mother_name"]
            mother_phone = row["mother_phone"]
            mother_occupation = row["mother_occupation"]
            if_guardian_is = row["if_guardian_is"]
            guardian_relation = row["guardian_relation"]
            guardian_phone = row["guardian_phone"]
            guardian_occupation = row["guardian_occupation"]
            guardian_address = row["guardian_address"]
            current_address = row["current_address"]
            permanent_address = row["permanent_address"]
            bank_account_number = row["bank_account_number"]
            bank_name = row["bank_name"]
            ifsc_code = row["ifsc_code"]
            national_identification_number = row["national_identification_number"]
            local_identification_number = row["local_identification_number"]
            previous_school_detail = row["previous_school_detail"]
            note = row["note"]
            title_1 = row["title_1"]
            title_2 = row["title_2"]
            title_3 = row["title_3"]
            title_4 = row["title_4"]
            diable_reson = row["diable_reson"]
            status = row["status"]
            session = row["session"]

            # date_time_str = datetime.strptime(date_of_birth,"%Y-%m-%d %H:%M:%S")
            # as_on_date_str = datetime.strptime(as_on_date,"%Y %m %d %H:%M:%S")
            # admission_date_str = datetime.strptime(admission_date,"%Y %m %d %H:%M:%S")
            if first_name_1:
                password_student = generate_password()
                password_parent = generate_password()
                last_name = last_name_1
                if not last_name:
                    last_name = ""

                # Create a user account for the student
                username_student = f"student{records.count()}"
                user_student = User.objects.create_user(
                    username=username_student,
                    first_name=first_name_1,
                    last_name=last_name_1,
                    email=email_1,
                    password=password_student,
                    user_type="Student",
                )
                user_student.save()
                print(user_student.first_name)

                # Create a user account for the parent
                username_parent = f"parent{records.count()}"
                user_parent = User.objects.create_user(
                    username=username_parent,
                    first_name=guardian_name_1,
                    email=guardian_email_1,
                    password=password_parent,
                    user_type="Parent",
                )
                user_parent.save()

                student_obj = StudentAdmission.objects.create(
                    session=request.Session,
                    user_student_id=user_student.pk,
                    user_parent_id=user_parent.pk,
                    created_by=request.user,
                    admission_no=admission_no_name,
                    roll_number=roll_number,
                    first_name=first_name_1,
                    Class_id=Classs,
                    section_id=section_id,
                    Father_name=Father_name_1,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    category_id=category_1,
                    mobile_number=mobile_number,
                    student_house_id=student_house,
                    vehicle_number_id=vehicle_number,
                    route_list_id=route_list,
                    hostel_id=hostel,
                    room_number_id=room_number,
                    last_name=last_name_1,
                    email=email_1,
                    guardian_name=guardian_name_1,
                    guardian_email=guardian_email_1,
                    religion=religion,
                    Caste=Caste,
                    Blood_group=Blood_group,
                    height=height,
                    weight=weight,
                    Father_phone=Father_phone,
                    Father_occupation=Father_occupation,
                    mother_name=mother_name,
                    mother_phone=mother_phone,
                    mother_occupation=mother_occupation,
                    if_guardian_is=if_guardian_is,
                    guardian_relation=guardian_relation,
                    guardian_phone=guardian_phone,
                    guardian_occupation=guardian_occupation,
                    guardian_address=guardian_address,
                    current_address=current_address,
                    permanent_address=permanent_address,
                    bank_account_number=bank_account_number,
                    bank_name=bank_name,
                    ifsc_code=ifsc_code,
                    national_identification_number=national_identification_number,
                    local_identification_number=local_identification_number,
                    previous_school_detail=previous_school_detail,
                    note=note,
                    title_1=title_1,
                    title_2=title_2,
                    title_3=title_3,
                    title_4=title_4,
                    diable_reson_id=diable_reson,
                    status=status,
                    session_id=session,
                    as_on_date=as_on_date,
                    admission_date=admission_date,
                )

                LoginCredentials.objects.create(
                    student_id=student_obj.pk,
                    student_username=username_student,
                    student_password=password_student,
                    parent_username=username_parent,
                    parent_passwod=password_parent,
                )

                StudentSession.objects.create(
                    session=request.Session,
                    student_id=student_obj.pk,
                    status="Active",
                )

                StudentClass.objects.create(
                    session=request.Session,
                    student_id=student_obj.pk,
                    Class_id=Classs,
                    section_id=section_id,
                    status="Active",
                )
        return HttpResponseRedirect("/import_student")
    else:
        print(form.errors)
    context = {}
    return render(request, "Student_information/import_student.html", context)


@login_required
@user_type_required("Staff")
def import_staff(request):
    form = AddStaffForm()
    if request.method == "POST" and request.FILES["staff_add_file"]:
        file = request.FILES["staff_add_file"]
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            user_name = row["user"]
            epf_no_name = row["epf_no"]
            phone_no_num = row["phone_no"]
            basic_salary = row["basic_salary"]
            contract_type = row["contract_type"]
            work_shift = row["work_shift"]
            location = row["location"]
            instagram = row["instagram"]
            linkedin = row["linkedin"]
            twitter = row["twitter"]
            facebook = row["facebook"]
            bank_name = row["bank_name"]
            branch_name = row["branch_name"]
            ifsc_code = row["ifsc_code"]
            account_no = row["account_no"]
            bank_title = row["bank_title"]
            staff_id = row["staff_id"]
            roles = row["roles"]
            designation = row["designation"]
            department = row["department"]
            first_name = row["first_name"]
            last_name = row["last_name"]
            father_name = row["father_name"]
            mother_name = row["mother_name"]
            email = row["email"]
            gender = row["gender"]
            date_of_birth = row["date_of_birth"]
            date_of_joining = row["date_of_joining"]
            phone_no = row["phone_no"]
            emergency_contact = row["emergency_contact"]
            marital_status = row["marital_status"]
            current_address = row["current_address"]
            permanent_address = row["permanent_address"]
            qualification = row["qualification"]
            work_experience = row["work_experience"]
            note = row["note"]
            status = row["status"]
            resume = row["resume"]

            dob1 = pd.to_datetime(date_of_birth).to_pydatetime()
            doj = pd.to_datetime(date_of_joining).to_pydatetime()

            password_staff = generate_password()
            user = User.objects.create(
                username=user_name,
                email=email,
                first_name=first_name,
                last_name=last_name,
                dob=dob1,
                phone_number=phone_no,
                user_type="Staff",
                password=password_staff,
            )

            # dob1 = datetime.strptime(formatted_date,"%Y-%m-%d %H:%M:%S")

            AddStaff.objects.create(
                user_id=user.pk,
                epf_no=epf_no_name,
                phone_no=phone_no_num,
                basic_salary=basic_salary,
                contract_type=contract_type,
                work_shift=work_shift,
                location=location,
                bank_title=bank_title,
                account_no=account_no,
                ifsc_code=ifsc_code,
                branch_name=branch_name,
                bank_name=bank_name,
                facebook=facebook,
                twitter=twitter,
                linkedin=linkedin,
                instagram=instagram,
                staff_id=staff_id,
                roles_id=roles,
                designation_id=designation,
                department_id=department,
                first_name=first_name,
                last_name=last_name,
                father_name=father_name,
                mother_name=mother_name,
                email=email,
                gender=gender,
                date_of_birth=dob1,
                date_of_joining=doj,
                emergency_contact=emergency_contact,
                marital_status=marital_status,
                current_address=current_address,
                permanent_address=permanent_address,
                qualification=qualification,
                work_experience=work_experience,
                note=note,
                status=status,
                resume=resume,
            )
        return HttpResponseRedirect("/import_staff")
    else:
        print(form.errors)
    context = {"add_staff": "active"}
    return render(request, "Human_Resource/import_staff.html", context)


@login_required
@user_type_required("Staff")
def student_login_credentials(request):
    class_records = Class.objects.all()

    if request.method == "POST":
        classs = request.POST.get("class")
        section = request.POST.get("section")
        filters = {}
        if classs:
            filters["Class_id"] = classs
        if section:
            filters["section_id"] = section

        record = StudentAdmission.objects.filter(**filters).values("id")
        records = LoginCredentials.objects.filter(student__id__in=record)
        context = {
            "student_information_report": "active",
            "records": records,
            "class_records": class_records,
        }
        return render(request, "Reports/student_login_credentials.html", context)

    context = {
        "student_information_report": "active",
        "class_records": class_records,
    }

    return render(request, "Reports/student_login_credentials.html", context)


@login_required
@user_type_required("Staff")
def subject_lesson_paln_report(request):
    class_records = Class.objects.all()
    if request.method == "POST":
        classs = request.POST.get("class")
        suction = request.POST.get("section")
        subject_grp = request.POST.get("subject_group")
        subject = request.POST.get("subject")
        subjects_name = Subjects.objects.get(id=subject)
        Lesson_plan = LessonPlan.objects.filter(
            time_table__Class=classs,
            time_table__section=suction,
            time_table__subject_group=subject_grp,
            time_table__subject=subject,
        )

        lesson_records = Lesson.objects.filter(
            Class_id=classs, section_id=suction, subject=subject
        )
        total = 0
        percent = 1
        for data in lesson_records:
            topic_records = topic.objects.filter(lesson_name=data.id)
            if topic_records.count() > 0:
                percentage = int(
                    topic_records.filter(status="complete").count()
                    * 100
                    / topic_records.count()
                )
                percent *= percentage / 100
                total += 1
        if total > 0:
            percentage = f"{subjects_name.subject_name} Complete {percent*100}%"
        context = {
            "class_records": class_records,
            "Lesson_plan": Lesson_plan,
            "lesson_paln_report": "active",
            "percentage": percentage,
        }
        return render(request, "Reports/subject_lesson_paln_report.html", context)
    context = {"class_records": class_records, "lesson_paln_report": "active"}
    return render(request, "Reports/subject_lesson_paln_report.html", context)


@login_required
@user_type_required("Staff")
def generate_student_certificate(request):
    if (
        request.user.is_superuser
        or "generate_certificate_view" in request.permissions
        or "generate_certificate_add" in request.permissions
    ):
        try:
            student_certificate_records = StudentCertificate.objects.all()
            class_records = Class.objects.all()
            if request.method == "POST":
                classs = request.POST.get("class")
                section = request.POST.get("section")
                certificate_name = request.POST.get("certificate_name")
                records = StudentAdmission.objects.filter(
                    Class=classs,
                    section=section,
                    session=request.Session,
                )
                context = {
                    "generate_student_certificate": "active",
                    "student_certificate_records": student_certificate_records,
                    "class_records": class_records,
                    "classs": int(classs),
                    "section": int(section),
                    "certificate_name": int(certificate_name),
                    "records": records,
                }
                return render(
                    request, "Certificate/generate_student_certificate.html", context
                )
            context = {
                "generate_student_certificate": "active",
                "student_certificate_records": student_certificate_records,
                "class_records": class_records,
            }
            return render(
                request, "Certificate/generate_student_certificate.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def printing_student_certificate(request):
    cretificate_obj = StudentCertificate.objects.get(
        id=request.POST.get("certificate_name")
    )
    records = StudentAdmission.objects.filter(id__in=request.POST.getlist("checkbox"))
    print(records)
    body_text = []
    string = cretificate_obj.body_text
    for data in records:
        new_string = string

        new_string = (
            new_string.replace("[name]", data.first_name)
            if data.first_name
            else new_string.replace("[name]", "")
        )
        new_string = (
            new_string.replace("[admission_no]", data.admission_no)
            if data.admission_no
            else new_string.replace("[admission_no]", "")
        )
        new_string = (
            new_string.replace("[dob]", str(data.date_of_birth))
            if data.date_of_birth
            else new_string.replace("[dob]", "")
        )
        new_string = (
            new_string.replace("[guardian]", data.guardian_name)
            if data.guardian_name
            else new_string.replace("[guardian]", "")
        )
        new_string = (
            new_string.replace("[created_at]", str(data.created_at.date()))
            if data.created_at.date()
            else new_string.replace("[created_at]", "")
        )
        new_string = (
            new_string.replace("[roll_no]", data.roll_number)
            if data.roll_number
            else new_string.replace("[roll_no]", "")
        )
        new_string = (
            new_string.replace("[class]", data.Class.Class)
            if data.Class
            else new_string.replace("[class]", "")
        )
        new_string = (
            new_string.replace("[section]", data.section.section_name)
            if data.section
            else new_string.replace("[section]", "")
        )
        new_string = (
            new_string.replace("[gender]", data.gender)
            if data.gender
            else new_string.replace("[gender]", "")
        )
        new_string = (
            new_string.replace("[admission_date]", str(data.as_on_date))
            if data.as_on_date
            else new_string.replace("[admission_date]", "")
        )
        new_string = (
            new_string.replace("[category]", data.category.category)
            if data.category
            else new_string.replace("[category]", "")
        )
        new_string = (
            new_string.replace("[email]", data.email)
            if data.email
            else new_string.replace("[email]", "")
        )
        new_string = (
            new_string.replace("[phone]", data.mobile_number)
            if data.mobile_number
            else new_string.replace("[phone]", "")
        )
        new_string = (
            new_string.replace("[present_address]", data.permanent_address)
            if data.permanent_address
            else new_string.replace("[present_address]", "")
        )
        new_string = (
            new_string.replace("[cast]", data.Caste)
            if data.Caste
            else new_string.replace("[cast]", "")
        )

        if data.Father_name:
            new_string = new_string.replace("[father_name]", data.Father_name)
        else:
            new_string = new_string.replace("[father_name]", "")

        if data.mother_name:
            new_string = new_string.replace("[mother_name]", data.mother_name)
        else:
            new_string = new_string.replace("[mother_name]", "")
        if data.religion:
            new_string = new_string.replace("[religion]", data.religion)
        else:
            new_string = new_string.replace("[religion]", "")
        body_text.append(new_string)

    context = {
        "generate_student_certificate": "active",
        "data": cretificate_obj,
        "body_text": body_text,
    }
    return render(request, "Certificate/printing_student_certificate.html", context)


@login_required
@user_type_required("Staff")  # To change Password
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request, user
            )  # Update the session with the new password
            messages.success(request, "Password changed successfully.")
            return redirect(reverse("/"))  # Redirect to the dashboard page
    else:
        form = PasswordChangeForm(request.user)
    print(form.errors)  # Debug statement
    return render(request, "change_password.html", {"form": form})


@login_required
@user_type_required("Staff")
def profile(request):
    record = AddStaff.objects.get(user=request.user)
    context = {"record": record}
    return render(request, "System_setting/profile.html", context)


def send_mail_search_js(request):
    value = request.GET.get("selected_val")
    if value == "Students":
        records = StudentAdmission.objects.filter(session=request.Session)
        data = list(records.values("first_name", "admission_no", "id"))
    elif value == "Guardians":
        records = StudentAdmission.objects.filter(session=request.Session)
        data = list(records.values("guardian_name", "id"))
    else:
        staff = AddStaff.objects.filter(roles=value)
        data = list(staff.values("first_name", "id"))
    return JsonResponse(data, safe=False)


@login_required
def mail_search_save_js(request):
    id = request.GET.get("id")
    type = request.GET.get("type")
    if type == "Staff":
        MailSearchTemp.objects.get_or_create(
            Staff_id=id,
            type=type,
        )
    else:
        MailSearchTemp.objects.get_or_create(
            Student_id=id,
            type=type,
        )
    data = list(
        MailSearchTemp.objects.values(
            "id",
            "Staff__first_name",
            "Student__first_name",
            "Student__guardian_name",
            "type",
        )
    )
    return JsonResponse(data, safe=False)


@login_required
def mail_search_delete_js(request):
    id = request.GET.get("id")
    MailSearchTemp.objects.get(id=id).delete()
    data = list(
        MailSearchTemp.objects.values(
            "id",
            "Staff__first_name",
            "Student__first_name",
            "Student__guardian_name",
            "type",
        )
    )
    return JsonResponse(data, safe=False)


@login_required
@user_type_required("Staff")
def online_class(request):
    if (
        request.user.is_superuser
        or "online_live_class_view" in request.permissions
        or "online_live_class_add" in request.permissions
    ):
        try:
            records = OnlineClass.objects.all()

            if request.method == "POST":
                form = OnlineClassForm(request.POST)
                if form.is_valid():
                    form.save()
                    obj = form.save(commit=False)
                    obj.created_by = request.user
                    obj.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect(
                        "/online_class"
                    )  # Redirect to a view showing the list of all online classes
            else:
                form = OnlineClassForm()

            context = {"records": records, "form": form, "online_class": "active"}

            return render(request, "Livesession/online_class.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def online_class_edit(request, pk):
    if (
        request.user.is_superuser
        or "online_live_class_edit" in request.permissions
        or "online_live_class_view" in request.permissions
    ):
        try:
            records = OnlineClass.objects.all()
            online_classs = OnlineClass.objects.all()
            online_class = OnlineClass.objects.get(id=pk)
            form = OnlineClassForm(instance=online_class)
            if request.method == "POST":
                form = OnlineClassForm(request.POST, instance=online_class)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/online_class")
            context = {
                "form": form,
                "online_classs": online_classs,
                "records": records,
                "online_class": "active",
                "edit": True,
            }
            return render(request, "Livesession/online_class_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def online_class_delete(request, pk):
    if request.user.is_superuser or "online_live_class_delete" in request.permissions:
        try:
            online_class = OnlineClass.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/online_class")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def staff_meeting(request):
    if (
        request.user.is_superuser
        or "staff_meeting_view" in request.permissions
        or "staff_meeting_add" in request.permissions
    ):
        try:
            addstaff = AddStaff.objects.all()
            records = StaffMeeting.objects.all()
            if request.method == "POST":
                form = StaffMeetingForm(request.POST)
                if form.is_valid():
                    form.save()

                    obj = form.save(commit=False)
                    obj.created_by = request.user
                    obj.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect(
                        "/staff_meeting"
                    )  # Redirect to a view showing the list of all online classes
            else:
                form = StaffMeetingForm()
                print(form.errors)
            context = {
                "records": records,
                "form": form,
                "staff_meeting": "active",
                "addstaff": addstaff,
            }

            return render(request, "Livesession/staff_meeting.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def staff_meeting_edit(request, pk):
    if request.user.is_superuser or "staff_meeting_edit" in request.permissions:
        try:
            addstaff = AddStaff.objects.all()
            records = StaffMeeting.objects.all()
            staff_meetings = StaffMeeting.objects.all()
            data = StaffMeeting.objects.get(id=pk)
            form = StaffMeetingForm(instance=data)
            if request.method == "POST":
                form = StaffMeetingForm(request.POST, instance=data)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/staff_meeting")
            context = {
                "form": form,
                "staff_meetings": staff_meetings,
                "staff_meeting": "active",
                "edit": True,
                "addstaff": addstaff,
                "data": data,
                "records": records,
            }
            return render(request, "Livesession/staff_meeting_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def staff_meeting_delete(request, pk):
    # if request.user.is_superuser or 'staff_meeting_delete' in request.permissions:
    try:
        staff_meeting = StaffMeeting.objects.get(id=pk).delete()
        messages.error(request, "Record Deleted Successfully")
        return HttpResponseRedirect("/staff_meeting")
    except Exception as error:
        return render(request, "error.html", {"error": error})


@login_required
@user_type_required("Staff")
def parent_meeting(request):
    if (
        request.user.is_superuser
        or "parent_meeting_view" in request.permissions
        or "parent_meeting_add" in request.permissions
    ):
        try:
            section_record = Section.objects.all()
            class_record = Class.objects.all()
            addstaff = AddStaff.objects.all()
            addstudent = StudentAdmission.objects.all()
            records = ParentMeeting.objects.all()
            form1 = StudentAdmissionForm()

            if request.method == "POST":
                form = ParentMeetingForm(request.POST)
                if form.is_valid():
                    form.save()

                    obj = form.save(commit=False)
                    obj.created_by = request.user
                    obj.save()
                    messages.success(request, "Record Saved Successfully")
                    return redirect("/parent_meeting")
            else:
                form = ParentMeetingForm()
                print(form.errors)
            context = {
                "records": records,
                "form": form,
                "form1": form1,
                "parent_meeting": "active",
                "addstaff": addstaff,
                "section_record": section_record,
                "addstudent": addstudent,
                "class_record": class_record,
            }

            return render(request, "Livesession/parent_meeting.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def parent_meeting_edit(request, pk):
    if request.user.is_superuser or "parent_meeting_edit" in request.permissions:
        try:
            records = ParentMeeting.objects.all()
            section_record = Section.objects.all()
            class_record = Class.objects.all()
            addstaff = AddStaff.objects.all()
            addstudent = StudentAdmission.objects.all()
            parent_meeting = ParentMeeting.objects.all()
            data = ParentMeeting.objects.get(id=pk)
            form = ParentMeetingForm(instance=data)
            form1 = StudentAdmissionForm(instance=data)

            if request.method == "POST":
                form = ParentMeetingForm(request.POST, instance=data)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/parent_meeting")
            context = {
                "form": form,
                "parent_meeting": parent_meeting,
                "parent_meeting": "active",
                "addstaff": addstaff,
                "data": data,
                "section_record": section_record,
                "class_record": class_record,
                "addstudent": addstudent,
                "form1": form1,
                "edit": True,
                "records": records,
            }
            return render(request, "Livesession/parent_meeting_edit.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def parent_meeting_delete(request, pk):
    # if request.user.is_superuser or 'parent_meeting_delete' in request.permissions:
    try:
        parent_meeting = ParentMeeting.objects.get(id=pk).delete()
        messages.error(request, "Record Deleted Successfully")
        return HttpResponseRedirect("/parent_meeting")
    except Exception as error:
        return render(request, "error.html", {"error": error})


@login_required
@user_type_required("Staff")
def staff_meetimg_backup(request, pk):
    records = StaffMeetingNote.objects.all()
    form = StaffMeetingNoteForm()
    record = StaffMeeting.objects.get(id=pk)
    if request.method == "POST":
        form = StaffMeetingNoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Saved Successfully")
            return HttpResponseRedirect("/staff_meeting")

    context = {
        "form": form,
        "records": records,
        "staff_meeting": "active",
        "record": record,
    }
    return render(request, "Livesession/staff_meetimg_backup.html", context)


@login_required
@user_type_required("Staff")
def staff_meeting_view(request, pk):
    if request.user.is_superuser or "staff_meeting_view" in request.permissions:
        try:
            records = StaffMeetingNote.objects.all()
            form = StaffMeetingNoteForm()
            record = StaffMeeting.objects.get(id=pk)

            context = {
                "form": form,
                "records": records,
                "staff_meeting": "active",
                "record": record,
            }
            return render(request, "Livesession/staff_meeting_view.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def student_details_edit(request, pk):
    if request.user.is_superuser or "student_information_edit" in request.permissions:
        try:
            system_fields = SystemFields.objects.last().student_fields
            custom_fields = CustomFields.objects.filter(field_belongs_to="Student")
            student_custom = StudentCustomFieldValues.objects.filter(student=pk)
            custom_fileds_records = []
            for data in custom_fields:
                dict = {}
                dict["custom_fields"] = data
                dict["student_custom"] = student_custom.filter(field=data.id).last()
                custom_fileds_records.append(dict)
            print(custom_fileds_records)
            records = StudentAdmission.objects.all()
            online_class = StudentAdmission.objects.get(id=pk)
            form = StudentAdmissionForm(instance=online_class)
            if request.method == "POST":
                form = StudentAdmissionForm(request.POST, instance=online_class)
                if form.is_valid():
                    form.save()

                    #  customs fields
                    for data in custom_fields:
                        if data.field_type == "multiselect":
                            value = request.POST.getlist(f"{data.field_name}")
                        else:
                            value = request.POST.get(f"{data.field_name}")
                        if value:
                            edit = student_custom.filter(field=data.id).last()
                            if edit:
                                edit.value = value
                                edit.save()
                            else:
                                StudentCustomFieldValues.objects.create(
                                    field=data, student_id=pk, value=value
                                )
                    messages.warning(request, "Record Updated Successfully")
                    return HttpResponseRedirect("/student_details")

            else:
                print(form.errors)
            context = {
                "form": form,
                "records": records,
                "student_details": "active",
                "edit": True,
                "custom_fields": custom_fields,
                "student_custom": student_custom,
                "custom_fileds_records": custom_fileds_records,
                "system_fields": system_fields,
            }
            return render(
                request, "Student_information/student_details_edit.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def student_details_delete(request, pk):
    if request.user.is_superuser or "student_information_delete" in request.permissions:
        try:
            StudentAdmission.objects.get(id=pk).delete()
            messages.error(request, "Record Deleted Successfully")
            return HttpResponseRedirect("/student_details")
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


@login_required
@user_type_required("Staff")
def payment_method(request):
    last_record = PaymentKeys.objects.all().last()
    if last_record:
        if request.POST.get("payment_gateway_btn") == "payment_gateway_btn":
            last_record.seleted_payment = request.POST.get("payment_gateway")
            last_record.save()
            return redirect("payment_method")
        else:
            if request.POST.get("btn_type") == "india":
                last_record.razorpay_key_id = request.POST.get("razorpay_key_id")
                last_record.razorpay_key_secret = request.POST.get(
                    "razorpay_key_secret"
                )
                last_record.save()
                return redirect("payment_method")
            elif request.POST.get("btn_type") == "kenya":
                last_record.mpesa_passkey = request.POST.get("mpesa_passkey")
                last_record.mpesa_consumer_key = request.POST.get("mpesa_consumer_key")
                last_record.mpesa_consumer_secret = request.POST.get(
                    "mpesa_consumer_secret"
                )
                last_record.save()
                return redirect("payment_method")

    else:
        if request.POST.get("payment_gateway_btn") == "payment_gateway_btn":
            PaymentKeys.objects.create(
                seleted_payment=request.POST.get("payment_gateway"),
            )
            return redirect("payment_method")
        else:
            if request.POST.get("btn_type") == "india":
                PaymentKeys.objects.create(
                    razorpay_key_id=request.POST.get("razorpay_key_id"),
                    razorpay_key_secret=request.POST.get("razorpay_key_secret"),
                )
                return redirect("payment_method")
            elif request.POST.get("btn_type") == "kenya":
                PaymentKeys.objects.create(
                    mpesa_passkey=request.POST.get("mpesa_passkey"),
                    mpesa_consumer_key=request.POST.get("mpesa_consumer_key"),
                    mpesa_consumer_secret=request.POST.get("mpesa_consumer_secret"),
                )
                return redirect("payment_method")
    context = {"payment_method": "active", "last_record": last_record}
    return render(request, "System_setting/payment_method.html", context)


@login_required
@user_type_required("Staff")
def email_setting(request):
    last_record = EmailSetting.objects.all().last()
    if request.method == "POST":
        if last_record:
            last_record.gmail = request.POST.get("gmail")
            last_record.password = request.POST.get("password")
            last_record.default_from_email = request.POST.get("default_from_email")
            last_record.email_port = request.POST.get("email_port")
            last_record.email_host = request.POST.get("email_host")
            last_record.save()
            return redirect("email_setting")
        else:
            EmailSetting.objects.create(
                gmail=request.POST.get("gmail"),
                password=request.POST.get("password"),
                default_from_email=request.POST.get("default_from_email"),
                email_port=request.POST.get("email_port"),
                email_host=request.POST.get("email_host"),
            )
            return redirect("email_setting")
    context = {"last_record": last_record, "email_setting": "active"}
    return render(request, "System_setting/email_setting.html", context)


@login_required
@user_type_required("Staff")  # =================================================
def chat_index(request):
    staff_records = AddStaff.objects.all()
    student_records = StudentAdmission.objects.filter(session=request.Session)
    contact_record = AddContact.objects.filter(user=request.user)
    records = []
    for data in contact_record:
        dict = {}
        count = ContanctMessage.objects.filter(status="sended", contact=data).count()
        dict["obj"] = data
        dict["unread_count"] = count
        records.append(dict)
    context = {
        "staff_records": staff_records,
        "student_records": student_records,
        "contact_record": contact_record,
        "records": records,
    }
    return render(request, "Chat/chat_index1.html", context)


@login_required
@user_type_required("Staff")
def save_contact(request):
    usertype = request.POST.get("usertype")
    user_id = request.POST.get("user_id")
    if usertype == "Staff":
        staff_obj = AddStaff.objects.get(id=user_id)
        AddContact.objects.get_or_create(
            user=request.user,
            staff_id=user_id,
            contact_user=staff_obj.user,
            usertype=usertype,
        )
        AddContact.objects.get_or_create(
            user=staff_obj.user,
            staff_id=user_id,
            contact_user=request.user,
            usertype="Staff",
        )
    else:
        if usertype == "Student":
            user_obj = StudentAdmission.objects.get(id=user_id)
            user_obj_id = user_obj.user_student
        elif usertype == "Parent":
            user_obj = StudentAdmission.objects.get(id=user_id)
            user_obj_id = user_obj.user_parent
        print("===", user_obj_id)
        AddContact.objects.get_or_create(
            user=request.user,
            student_id=user_id,
            contact_user=user_obj_id,
            usertype=usertype,
        )
        AddContact.objects.get_or_create(
            user=user_obj_id,
            student_id=user_id,
            contact_user=request.user,
            usertype="Staff",
        )
    return redirect("chat_index")


@login_required
@user_type_required("Staff")
def chat(request, pk):
    staff_records = AddStaff.objects.all()
    student_records = StudentAdmission.objects.filter(session=request.Session)
    contact_record = AddContact.objects.filter(user=request.user)
    contact_obj = AddContact.objects.get(id=pk)
    message_records = ContanctMessage.objects.filter(contact=contact_obj)
    message_records.filter(status="sended").update(status="readed")
    records = []
    for data in contact_record:
        dict = {}
        count = ContanctMessage.objects.filter(status="sended", contact=data).count()
        dict["obj"] = data
        dict["unread_count"] = count
        records.append(dict)
    context = {
        "staff_records": staff_records,
        "student_records": student_records,
        "contact_record": contact_record,
        "contact_obj": contact_obj,
        "pk": int(pk),
        "message_records": message_records,
        "records": records,
    }
    return render(request, "Chat/chat.html", context)


@login_required
def chat_msg_save_js(request):
    contact_obj = AddContact.objects.get(id=request.GET.get("pk"))
    to_contact = AddContact.objects.filter(
        user=contact_obj.contact_user, contact_user=contact_obj.user
    ).last()
    msg = request.GET.get("message")
    ContanctMessage.objects.create(
        contact_id=request.GET.get("pk"),
        from_message=msg,
        status="readed",
    )
    ContanctMessage.objects.create(
        contact=to_contact,
        to_message=msg,
        status="sended",
    )
    return JsonResponse(data="", safe=False)


@login_required
def chat_view_js(request):
    id = request.GET.get("pk")
    last_msg_id = request.GET.get("last_msg_id")
    if last_msg_id:
        record = ContanctMessage.objects.filter(contact=id, id__gt=last_msg_id).first()
        record.status = "readed"
        record.save()
        if record:
            data = {
                "id": record.id,
                "from_message": record.from_message,
                "to_message": record.to_message,
                "created_at": record.created_at.strftime("%I:%M %p"),
            }
        else:
            data = ""
    else:
        record = ContanctMessage.objects.filter(contact=id).first()
        record.status = "readed"
        record.save()
        if record:
            data = {
                "id": record.id,
                "from_message": record.from_message,
                "to_message": record.to_message,
                "created_at": record.created_at.strftime("%I:%M %p"),
            }
        else:
            data = ""
    return JsonResponse(data, safe=False)


#  ================ sms =============


@login_required
@user_type_required("Staff")
def sms_setting(request):
    last_record = SMSSetting.objects.all().last()
    print("======", last_record)

    if request.method == "POST":
        if request.POST.get("btn_type") == "twilio":
            if last_record:
                last_record.twilio_account_SID = request.POST.get("twilio_account_SID")
                last_record.twilio_auth_token = request.POST.get("twilio_auth_token")
                last_record.twilio_regeister_phone_no = request.POST.get(
                    "twilio_regeister_phone_no"
                )
                last_record.save()
                return redirect("sms_setting")

            else:
                SMSSetting.objects.create(
                    twilio_account_SID=request.POST.get("twilio_account_SID"),
                    twilio_auth_token=request.POST.get("twilio_auth_token"),
                    twilio_regeister_phone_no=request.POST.get(
                        "twilio_regeister_phone_no"
                    ),
                )
                return redirect("sms_setting")
    if request.POST.get("sms_gateway_btn") == "sms_gateway_btn":
        if last_record:
            last_record.status = request.POST.get("sms_gateway")
            last_record.save()
            return redirect("sms_setting")

        else:
            SMSSetting.objects.create(
                status=request.POST.get("sms_gateway"),
            )
            return redirect("sms_setting")
    context = {"last_record": last_record, "sms_setting": "active"}
    return render(request, "System_setting/sms_setting.html", context)


@login_required
@user_type_required("Staff")
def send_sms(request):
    form = SendEmailForm()
    forms = Role.objects.all()
    classes = Class.objects.all()
    sections = Section.objects.all()
    roles_records = Role.objects.all()

    if request.method == "POST":
        # Get the form data
        title = request.POST.get("title")
        message = request.POST.get("message")
        recipients = request.POST.getlist("noties_all[]")
        attachments = request.FILES.getlist("attachment")
        class_id = request.POST.get("class_id")
        selected_sections = request.POST.getlist("sectionss")

        email_subject = "Title: {}".format(title)
        email_message = """
        Message: {}
        Regards,
        Yours bharathbrands
        """.format(
            message
        )

        if recipients and recipients[0].isdigit():
            EmailSmsLog.objects.create(
                Title=title, send_by="SMS", sent_to="Group", created_by=request.user
            )
            for i in recipients:
                if i.isdigit():
                    user_phone_num = AddStaff.objects.filter(roles=int(i)).values_list(
                        "phone_no", flat=True
                    )
                    send_sms_notification(
                        email_subject,
                        email_message,
                        user_phone_num,
                    )
        else:
            EmailSmsLog.objects.create(
                Title=title, send_by="SMS", sent_to="Group", created_by=request.user
            )
            for recipient in recipients:
                if recipient == "student":
                    # Retrieve student email addresses and add them to recipient_emails
                    mobile_numbers = (
                        StudentAdmission.objects.exclude(mobile_number__isnull=True)
                        .exclude(mobile_number__exact="")
                        .values_list("mobile_number", flat=True)
                    )
                    send_sms_notification(
                        email_subject,
                        email_message,
                        mobile_numbers,
                    )
                elif recipient == "parent":
                    # Retrieve parent mobile_number addresses and add them to recipient_mobile_numbers
                    mobile_numbers = (
                        StudentAdmission.objects.exclude(guardian_phone__isnull=True)
                        .exclude(guardian_phone__exact="")
                        .values_list("guardian_phone")
                    )
                    send_sms_notification(
                        email_subject,
                        email_message,
                        mobile_numbers,
                    )
        if class_id and selected_sections:
            EmailSmsLog.objects.create(
                Title=title, send_by="SMS", sent_to="Class", created_by=request.user
            )
            mobile_numbers = (
                StudentAdmission.objects.filter(
                    Class=class_id, section__in=selected_sections
                )
                .exclude(mobile_number__isnull=True)
                .exclude(mmobile_number__exact="")
                .values_list("mobile_number", flat=True)
            )
            send_sms_notification(
                email_subject,
                email_message,
                mobile_numbers,
            )

        return redirect("/send_sms")

    context = {
        "form": form,
        "forms": forms,
        "classes": classes,
        "sections": sections,
        "roles_records": roles_records,
        "send_sms": "active",
    }

    return render(request, "Communicate/send_sms.html", context)


@login_required
@user_type_required("Staff")
def indvidula_send_sms(request):
    if request.user.is_superuser or "sms_view" in request.permissions:
        try:
            if request.method == "POST":
                title = request.POST.get("individual_title")
                message = request.POST.get("individual_message")
                email_subject = "Title: {}".format(title)
                email_message = """
                Message: {}
                Regards,
                Yours bharathbrands
                """.format(
                    message
                )
                EmailSmsLog.objects.create(
                    Title=title,
                    send_by="SMS",
                    sent_to="Individual",
                    created_by=request.user,
                )
                mail_for = MailSearchTemp.objects.all()
                phone_num = []
                for data in mail_for:
                    if data.type == "Student":
                        phone_num.append(data.Student.mobile_number)
                    elif data.type == "Guardian":
                        phone_num.append(data.Student.guardian_phone)
                    elif data.type == "Staff":
                        phone_num.append(data.Staff.phone_no)
                send_sms_notification(
                    email_subject,
                    email_message,
                    phone_num,
                )
                return redirect("/indvidula_send_sms")
            roles_records = Role.objects.all()
            MailSearchTemp.objects.all().delete()
            context = {"roles_records": roles_records, "send_sms": "active"}
            return render(request, "Communicate/indvidula_send_sms.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


def eventcalendar(request):
    if (
        request.user.is_superuser
        or "event_Calendar_view" in request.permissions
        or "event_Calendar_add" in request.permissions
    ):
        try:
            records = EventCalendar.objects.all()
            record = Calendarnofication.objects.all()
            form = CalendarnoficationForm()
            if request.method == "POST":
                form = CalendarnoficationForm(request.POST)
                if form.is_valid():
                    obj = form.save()

                    EventCalendar.objects.create(
                        title=obj.title,
                        description=" ",
                        startstime=datetime.combine(obj.date, time.min),
                        endtime=datetime.combine(obj.date, time.max),
                        created_by=request.user,
                    )
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/eventcalendar")
            context = {"form": form, "records": records, "record": record}
            return render(request, "System_setting/sample.html", context)
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return render(request, "page_not_found.html")


def eventcalendar_edit(request):
    id = request.GET.get("eventId")
    title = request.GET.get("eventTitle")
    description = request.GET.get("description")
    startstime = request.GET.get("start")
    endtime = request.GET.get("end")
    parsed_datetime = datetime.strptime(startstime, "%Y-%b-%d %H:%M:%S")
    parsed_datetime1 = datetime.strptime(endtime, "%Y-%b-%d %H:%M:%S")
    obj = EventCalendar.objects.get(id=id)
    obj.title = title
    obj.description = description
    obj.startstime = parsed_datetime
    obj.endtime = parsed_datetime1
    obj.save()

    return JsonResponse(data="", safe=False)


from django.utils import timezone


def event_calendar_save(request):
    title = request.GET.get("eventTitle")
    print("ddddd", title)
    description = request.GET.get("description")
    startstime = request.GET.get("start")
    endtime = request.GET.get("end")
    print("====", startstime)
    parsed_datetime = datetime.strptime(startstime, "%Y-%b-%d %H:%M:%S")
    parsed_datetime1 = datetime.strptime(endtime, "%Y-%b-%d %H:%M:%S")
    print("<<<<<<<<<<<startstime", startstime)
    EventCalendar.objects.create(
        title=title,
        description=description,
        startstime=parsed_datetime,
        endtime=parsed_datetime1,
        created_by=request.user,
    )

    return JsonResponse(data="", safe=False)


def event_calendar_delete(request):
    EventCalendar.objects.get(id=request.GET.get("id")).delete()
    return JsonResponse(data="", safe=False)


def calendarnofication_edit(request, pk):
    if (
        request.user.is_superuser
        or "event_Calendar_view" in request.permissions
        or "event_Calendar_add" in request.permissions
    ):
        try:
            records = Calendarnofication.objects.all()
            form = CalendarnoficationForm()
            record = Calendarnofication.objects.get(id=pk)
            form = CalendarnoficationForm(instance=record)
            if request.method == "POST":
                form = CalendarnoficationForm(request.POST, instance=record)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record Saved Successfully")
                    return HttpResponseRedirect("/eventcalendar")
            context = {
                "form": form,
                "records": records,
            }
            return render(
                request, "System_setting/calendarnofication_edit.html", context
            )
        except Exception as error:
            return render(request, "error.html", {"error": error})
    else:
        return redirect("dashboard")


@login_required
@user_type_required("Staff")
def calendarnofication_delete(request, pk):
    # if request.user.is_superuser or 'parent_meeting_delete' in request.permissions:
    try:
        Calendarnofication.objects.get(id=pk).delete()
        messages.error(request, "Record Deleted Successfully")
        return HttpResponseRedirect("/eventcalendar")
    except Exception as error:
        return render(request, "error.html", {"error": error})


@user_type_required("Staff")
def To_do_list(request):
    obj = Calendarnofication.objects.get(id=request.GET.get("id"))
    if obj.status == "completed":
        obj.status = "incompleted"
    else:
        obj.status = "completed"
        messages.success(request, "Task Completed Successfully")
    obj.save()
    return JsonResponse(data="", safe=False)


@login_required
@user_type_required("Staff")
def student_user(request):
    student_login_id = LoginCredentials.objects.all()
    staff_login_id = AddStaff.objects.all()

    context = {
        "student_user": "active",
        "student_login_id": student_login_id,
        "staff_login_id": staff_login_id,
    }
    return render(request, "System_setting/user.html", context)


def active_js(request):
    active_id = request.GET.get("active_id")
    student_login_id = LoginCredentials.objects.get(id=active_id)
    a = student_login_id.student.user_student
    b = User.objects.get(id=a.id)
    if b.is_active == True:
        b.is_active = False
        b.save()
    else:
        b.is_active == False
        b.is_active = True
        b.save()
    return JsonResponse(data="", safe=False)


def active_parent_js(request):
    active_id = request.GET.get("active_parent_id")
    student_login_id = LoginCredentials.objects.get(id=active_id)
    a = student_login_id.student.user_parent
    b = User.objects.get(id=a.id)
    if b.is_active == True:
        b.is_active = False
        b.save()
    else:
        b.is_active == False
        b.is_active = True
        b.save()
    return JsonResponse(data="", safe=False)


def active_staff_js(request):
    active_id = request.GET.get("active_staff_id")
    staff_login_id = AddStaff.objects.get(id=active_id)
    a = staff_login_id.user
    b = User.objects.get(id=a.id)
    if b.is_active == True:
        b.is_active = False
        b.save()
    else:
        b.is_active == False
        b.is_active = True
        b.save()
    return JsonResponse(data="", safe=False)


@login_required
@user_type_required("Staff")
def custom_fields(request):
    records = CustomFields.objects.all()
    form = CustomFieldsForm()
    if request.method == "POST":
        form = CustomFieldsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Saved Successfully")
            return HttpResponseRedirect("/custom_fields")
        else:
            print(form.errors)
    context = {"form": form, "records": records, "custom_fields": "active"}
    return render(request, "System_setting/custom_fields.html", context)


@login_required
@user_type_required("Staff")
def custom_fields_edit(request, pk):
    records = CustomFields.objects.all()
    obj = CustomFields.objects.get(id=pk)
    form = CustomFieldsForm(instance=obj)
    if request.method == "POST":
        form = CustomFieldsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated Successfully")
            return HttpResponseRedirect("/custom_fields")
        else:
            print(form.errors)
    context = {
        "form": form,
        "records": records,
        "custom_fields": "active",
        "obj": obj,
        "edit": True,
    }
    return render(request, "System_setting/custom_fields.html", context)


@login_required
@user_type_required("Staff")
def custom_fields_delete(request, pk):
    CustomFields.objects.get(id=pk).delete()
    messages.error(request, "Record delete Successfully")
    return HttpResponseRedirect("/custom_fields")


@login_required
@user_type_required("Staff")
def modules(request):
    print(request.system_modules)
    permissions = request.POST.getlist("modules_val")
    records = Modules.objects.all().first()
    if request.method == "POST":
        if records:
            records.system = permissions
            records.save()
            return HttpResponseRedirect("/modules")

        else:
            Modules.objects.create(
                system=permissions,
            )
            return HttpResponseRedirect("/modules")
    context = {"modules": "active", "records": records}
    return render(request, "System_setting/modules_system.html", context)


@login_required
@user_type_required("Staff")
def modules_parent(request):
    permissions_parent = request.POST.getlist("modules_val_parent")
    print(">>>>>>>>>>eeee<<<<<<<<<<<", permissions_parent)
    records = Modules.objects.all().first()
    if request.method == "POST":
        if records:
            records.parent = permissions_parent
            records.save()
            return HttpResponseRedirect("/modules_parent")

        else:
            permissions_parent = request.POST.getlist("modules_val_parent")
            print(">>>>>>>>>C<<<<<<<<<<", permissions_parent)
            Modules.objects.create(
                parent=permissions_parent,
            )
            return HttpResponseRedirect("/modules_parent")
    context = {"modules": "active", "records": records}
    return render(request, "System_setting/modules_parent.html", context)


@login_required
@user_type_required("Staff")
def modules_student(request):
    permissions_student = request.POST.getlist("modules_val_student")
    records = Modules.objects.all().first()
    if request.method == "POST":
        if records:
            records.student = permissions_student
            records.save()
            return HttpResponseRedirect("/modules_student")

        else:
            Modules.objects.create(
                student=permissions_student,
            )
            return HttpResponseRedirect("/modules_student")
    context = {"modules": "active", "records": records}
    return render(request, "System_setting/modules_student.html", context)


@login_required
@user_type_required("Staff")
def student_profile_update(request):
    permissions_fields = request.POST.getlist("fields_val")
    status_get = request.POST.get("status")
    records = Studentprofileupdate.objects.all().first()
    if request.method == "POST":
        if records:
            records.fieldshide = permissions_fields
            records.status = status_get
            records.save()
            return HttpResponseRedirect("/student_profile_update")
        else:
            Studentprofileupdate.objects.create(
                fieldshide=permissions_fields, status=status_get
            )
            return HttpResponseRedirect("/student_profile_update")

    context = {"student_profile_update": "active", "records": records}
    return render(request, "System_setting/student_profile_update.html", context)


def system_fields_student(request):
    obj = SystemFields.objects.first()
    if request.method == "POST":
        if obj:
            obj.student_fields = request.POST.getlist("system_fields")
            obj.save()
            return redirect("system_fields_student")
        else:
            create = SystemFields(
                student_fields=request.POST.getlist("system_fields"),
            )
            create.save()
            return redirect("system_fields_student")
    context = {"obj": obj.student_fields}
    return render(request, "System_setting/system_fields_student.html", context)


def system_fields_staff(request):
    obj = SystemFields.objects.first()
    if request.method == "POST":
        if obj:
            obj.staff_fields = request.POST.getlist("system_fields")
            obj.save()
            return redirect("system_fields_staff")
        else:
            create = SystemFields()
            create.staff_fields(request.POST.getlist("system_fields"))
            create.save()
            return redirect("system_fields_staff")
    context = {"obj": obj.staff_fields}
    return render(request, "System_setting/system_fields_staff.html", context)


def student_search(request):
    print("search_txt", request.POST)
    search_txt = request.POST.get("search_txt")
    records = StudentAdmission.objects.filter(
        Q(admission_no__icontains=search_txt)
        | Q(roll_number__icontains=search_txt)
        | Q(first_name__icontains=search_txt)
        | Q(last_name__icontains=search_txt)
        | Q(roll_number__icontains=search_txt)
    )
    records = records.filter(session=request.Session)
    context = {"records": records}
    return render(request, "System_setting/student_search.html", context)


def print_header_footer(request):
    image_fees = request.FILES.get("image_fees_receipt")
    note_fees = request.POST.get("note_fees_receipt")
    image_payroll = request.FILES.get("image_payslip")
    note_payroll = request.POST.get("note_payslip")
    fees_receipt = request.POST.get("fees_receipt")
    pay_roll_receipt = request.POST.get("pay_roll_receipt")
    records = PrintHeaderFooter.objects.all().first()
    if request.method == "POST":
        if fees_receipt:
            if records:
                records.image_fees_receipt = image_fees
                records.note_fees_receipt = note_fees
                records.save()
                return HttpResponseRedirect("/print_header_footer")

            else:
                PrintHeaderFooter.objects.create(
                    image_fees_receipt=image_fees,
                    note_fees_receipt=note_fees,
                    image_payslip=image_payroll,
                    note_payslip=note_payroll,
                )
                return HttpResponseRedirect("/print_header_footer")
        if pay_roll_receipt:
            if records:
                records.image_payslip = image_payroll
                records.note_payslip = note_payroll
                records.save()
                return HttpResponseRedirect("/print_header_footer")

            else:
                PrintHeaderFooter.objects.create(
                    image_fees_receipt=image_fees,
                    note_fees_receipt=note_fees,
                    image_payslip=image_payroll,
                    note_payslip=note_payroll,
                )
                return HttpResponseRedirect("/print_header_footer")
    else:
        print()

    context = {"print_header_footer": "avctive", "records": records}
    return render(request, "System_setting/print_header_footer.html", context)


def print_fees(request, pk):
    header_img = PrintHeaderFooter.objects.all().first()
    records = StudentFess.objects.get(id=pk)

    context = {"records": records, "header_img": header_img}
    return render(request, "Fees_Collection/print_fees.html", context)


def print_master_fees(request, pk):
    header_img = PrintHeaderFooter.objects.all().first()
    fees_records = FeesAssign.objects.get(id=pk, session=request.Session)
    master_fees = StudentFess.objects.filter(fess_id=fees_records)

    context = {
        "fees_records": fees_records,
        "master_fees": master_fees,
        "header_img": header_img,
    }
    return render(request, "Fees_Collection/print_master_fees.html", context)
