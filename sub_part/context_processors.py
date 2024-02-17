from django.contrib.auth.models import User
from .models import *

def users_and_projects(request):
    general_setting=GeneralSetting.objects.all().last()
    if not general_setting:
        general_setting=[]

    return {'general_setting': general_setting}