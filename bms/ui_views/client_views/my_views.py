
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from bms.models import *


def my_account(request):
	return render(request,'bms/client_ui/my_account.html')