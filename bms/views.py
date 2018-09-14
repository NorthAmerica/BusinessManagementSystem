from django.shortcuts import render
from bms.models import menu_model
from django.contrib.auth.decorators import login_required
from bms.forms import *
from django.middleware import csrf
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from .ui_views.view_shortcuts import get_org_name


# Create your views here.

def get_or_create_csrf_token(request):
	token = request.META.get('CSRF_COOKIE', None)
	if token is None:
		token = csrf._get_new_csrf_string()
		request.META['CSRF_COOKIE'] = token
	request.META['CSRF_COOKIE_USED'] = True
	return token


def login_page(request):
	return render(request, 'bms/login.html', locals())


def login_check(request):
	ret_msg = {}
	if request.method == 'POST':
		try:
			userName = request.POST.get('username')
			userPassword = request.POST.get('password')
			user = authenticate(username=userName, password=userPassword)
			if user is not None:
				if user.is_active:
					login(request, user)
					ret_msg = {'success': 'true', 'msg': '登陆成功'}
				else:
					ret_msg = {'success': 'false', 'msg': '该用户未激活！'}
			else:
				ret_msg = {'success': 'false', 'msg': '用户名或密码错误'}
		# return render(request, 'bms/login.html', context={})

		except Exception as ex:
			print(ex)
			return JsonResponse({'success': 'false', 'msg': ex})

	return JsonResponse(ret_msg)

@login_required
def index(request):
	ls_menu = []
	main_menu = Menu.objects.exclude(f_menu__isnull=False).order_by('order_num')
	for menu in main_menu:

		p_menu = menu_model.MenuModel()
		p_menu.setName(menu.menu_name)
		p_menu.setUrl(menu.menu_url)
		child_menu = menu.get_child()
		for child in child_menu:
			c_menu = menu_model.MenuModel()
			c_menu.setName(child.menu_name)
			c_menu.setUrl(child.menu_url)
			# if  request.user.has_perm('view_menu',child):
			p_menu.child.append(c_menu)
		# if  request.user.has_perm('view_menu',menu):
		ls_menu.append(p_menu)

	org_name = get_org_name(request)

	return render(request, 'bms/index.html', locals())


def Logout_page(request):
	# 注销用户，这个方法就会把我们的session跟cookie清理掉
	logout(request)
	return render(request, 'bms/login.html')