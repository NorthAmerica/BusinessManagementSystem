from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponse
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from bms.models import *

def index(request):
	return render(request,'bms/client_ui/base.html')