
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from bms.models import *

def login(request):
	# 登陆页面
	request.session.flush()
	return render(request, 'bms/client_ui/login.html')

def login_check(request):
	# 登陆验证
	try:
		if request.method == 'POST':
			user_tel = request.POST.get('user_tel')
			user_pwd = request.POST.get('user_pwd')
			find_client = Client.objects.filter(mobile_phone=user_tel)
			if find_client.exists():
				client = find_client.first()
				if check_password(user_pwd,client.password):
					if client.is_freeze:
						return JsonResponse({'success': False, 'msg': '您的账户已被冻结，暂时不能登陆系统，请与您的经纪人进行联系。'},safe=False)
					else:
						request.session['is_login'] = True
						request.session['client_id'] = client.id
						request.session['client_name'] = client.name
						request.session['mobile_phone'] = client.mobile_phone
						request.session['allow_business'] = client.allow_business
						request.session['status'] = client.status
						request.session['org_id'] = client.organization_id
						request.session['agency_id'] = client.agency_id
						find_client.update(last_login_time=timezone.now())
						return JsonResponse({'success': True, 'msg': ''},safe=False)
			else:
				return JsonResponse({'success': False, 'msg': '用户名或密码不正确'}, safe=False)
	except Exception as e:
		print(e)
		return JsonResponse({'success': False, 'msg': e.__str__()},safe=False)


def register(request):
	# 注册页面
	return render(request, 'bms/client_ui/register.html')

def reg_check(request):
	# 注册验证
	try:
		if request.method == 'POST':
			code = request.POST.get('code')
			user_tel = request.POST.get('user_tel')
			pwd = request.POST.get('user_pwd')
			find_client = Client.objects.filter(mobile_phone=user_tel)
			if find_client.exists():
				return JsonResponse({'success': False, 'msg': '该手机号码已被注册，请使用其他号码注册。'},safe=False)
			agency = Agency.objects.filter(invite_num=code)
			if agency.exists():
				new_c = Client.objects.create(name=user_tel,
				                      mobile_phone=user_tel,
				                      password=make_password(pwd),
				                      agency=agency.first(),
				                      organization=agency.first().organization,
				                      operator=user_tel)
				if new_c is not None:
					return JsonResponse({'success': True, 'msg': '恭喜您！用户注册成功！'},safe=False)
				else:
					return JsonResponse({'success': False, 'msg': '对不起，客户添加失败。'},safe=False)
			else:
				return JsonResponse({'success': False, 'msg': '邀请码有误，请重新填写。'},safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()},safe=False)

def logout(request):
	# 用户注销
	return render(request,'bms/client_ui/login.html')