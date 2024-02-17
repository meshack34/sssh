import time
from django.http import HttpResponse
from .models import *


class MiddlewareExecutionStart(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        general_setting=GeneralSetting.objects.all().last()
        if general_setting:
            request.Session = general_setting.session
        else:
            request.Session = None
        if request.user.is_authenticated and not request.user.is_superuser:
            if request.user.user_type=='Student':
                request.student=StudentAdmission.objects.filter(user_student=request.user,session=request.Session).last()
            elif request.user.user_type=='Parent':
                request.parent=StudentAdmission.objects.filter(user_parent=request.user,session=request.Session).last()
            else:
                access=AddStaff.objects.filter(user=request.user).last()
                request.permissions=access.roles.permissions
                if not access.roles.permissions:
                    request.permissions=[]


        else:
            request.permissions=[]

        records=Modules.objects.all().first()
        if records and records.system:
            request.system_modules=records.system
        else:
            request.system_modules=[]

        if records and records.student:
            request.student_modules=records.student
        else:
            request.student_modules=[]
        if records and records.parent:
            request.parent_modules=records.parent
        else:
            request.parent_modules=[]

        response = self.get_response(request)
        return response



    # def process_exception(self,request,exception):
    #     return HttpResponse('<h3>Currently We Are Facing Technical Isses</h3>')