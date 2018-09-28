from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from BusinessManagementSystem import settings
from bms.models import *
import os


def my_account(request):
	return render(request,'bms/client_ui/account/my_account.html')

def authentication(request):
	return render(request,'bms/client_ui/account/authentication.html')

def update_authentication_info(request):
	try:
		if request.method=='POST':
			bank_card = request.FILES.get('bank_card')
			db_url = "bank/{id}/{file}".format(id=request.session.get('mobile_phone'), file=bank_card._name)
			save_url = "bank/{id}/".format(id=request.session.get('mobile_phone'))
			url = os.path.join(settings.MEDIA_ROOT, save_url)
			if not os.path.exists(url):
				os.makedirs(url)
			dest = os.path.join(settings.MEDIA_ROOT,save_url,bank_card._name)
			if os.path.exists(dest):
				os.remove(dest)
			with open(dest, "wb+") as destination:
				for chunk in bank_card.chunks():
					destination.write(chunk)

			card_no = request.POST.get('card_no')
			id_no = request.POST.get('id_no')
			bank_name = request.POST.get('bank_name')
			bank_city = request.POST.get('bank_city')
			branch_name = request.POST.get('branch_name')

			dic = {
				'identity_card':id_no,
				'bank_image':db_url,
				'bank_card':card_no,
				'bank_name':bank_name,
				'open_city':bank_city,
				'bank_branch':branch_name,
				'status':2
			}
			update_count = Client.objects.filter(pk=request.session.get('client_id')).update(**dic)
			if update_count!=0:
				request.session['status']='2'
				return JsonResponse({'success': True, 'msg': '认证信息上传成功！'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)

def checking(request):
	return render(request,'bms/client_ui/account/checking.html')
