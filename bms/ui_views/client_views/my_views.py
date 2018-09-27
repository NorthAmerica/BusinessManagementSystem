
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from bms.models import *


def my_account(request):
	return render(request,'bms/client_ui/account/my_account.html')

def authentication(request):
	return render(request,'bms/client_ui/account/authentication.html')

def update_authentication_info(request):
	try:
		if request.method=='POST':
			myfile = request.FILES.get('bank_card', None)
			return JsonResponse({'success': True, 'msg': '认证信息上传成功！'}, safe=False)
	except Exception as ex:

		pass