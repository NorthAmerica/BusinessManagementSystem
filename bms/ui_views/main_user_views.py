from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from bms.models import *
from bms.forms import *
from bms.ui_views.view_shortcuts import get_org_user_list,get_org_id

@login_required
def main_user_list(request):
	if  request.method == 'POST':
		try:
			page = request.POST.get("page")
			rows = request.POST.get("rows")
			user_all= []
			if request.user.is_superuser:
				user_all =list(User.objects.all())#.values_list('username','mobile_phone','position')
			elif request.user.identity =='org':
				user_all = get_org_user_list(request)
			paginator = Paginator(user_all, rows)

			try:
				books = paginator.page(page)
			except PageNotAnInteger:
				books = paginator.page(1)
			except EmptyPage:
				books = paginator.page(paginator.num_pages)
			eaList=[]
			for user in books.object_list:
				eaList.append({
					'id':user.id,
					"username":user.username,
					"mobile_phone":user.mobile_phone,
					'last_name':user.last_name,
					'email':user.email,
					"position":user.position,
					"is_active" :user.is_active
				})

			json_data_list = {
				'total':paginator.count,
				'rows':eaList
			}
			return JsonResponse(json_data_list)
		except Exception as ex:
			print(ex)
	else:
		return render(request, 'bms/user_config/user_config.html')

@login_required
@transaction.atomic
def add_main_user(request):
	'''新增用户'''
	if  request.method == 'POST':
		try:
			username = request.POST.get('username')
			password = request.POST.get('password')
			last_name = request.POST.get('last_name')
			email = request.POST.get('email')
			position = request.POST.get('position')
			mobile_phone = request.POST.get('mobile_phone')
			is_active = request.POST.get('is_active')
			org_id = get_org_id(request)
			dic = {
				"username": username,
				"password": make_password(password),
				"last_name": last_name,
				"email": email,
				"position": position,
				"mobile_phone": mobile_phone,
				"is_active": is_active,
				"identity": 'org'
			}

			obj = User.objects.create(**dic)
			if  obj is not None:
				org_user = {
					"user":obj,
					"organization":request.user.org_user.organization,
					"operator":request.user.username
				}
				create_user = Org_User.objects.create(**org_user)
				if  create_user is not None:
					return JsonResponse({'success':'true','msg':'新用户添加成功！'})
				else:
					return JsonResponse({'success': 'false', 'msg': '新用户没有添加成功，请您重新检查'})
			else:
				return JsonResponse({'success':'false','msg':'新用户没有添加成功，请您重新检查'})
		except Exception as ex:
			print(ex)
			return  JsonResponse({'success':'false','msg':ex})

@login_required
def update_main_user(request):
	'''更新用户'''
	if  request.method == 'POST':
		try:

			id = request.POST.get('id')
			username = request.POST.get('username')
			last_name = request.POST.get('last_name')
			email = request.POST.get('email')
			position = request.POST.get('position')
			mobile_phone = request.POST.get('mobile_phone')
			is_active = request.POST.get('is_active')

			dic = {
				"username": username,
				"last_name": last_name,
				"email": email,
				"position": position,
				"mobile_phone": mobile_phone,
				"is_active": is_active,

			}
			if id is not None:
				obj = User.objects.filter(id=id).update(**dic)
				if  obj is not None:
					return JsonResponse({'success':'true','msg':'用户更新成功！'})
			else:
				return JsonResponse({'success':'false','msg':'用户没有更新成功，请您重新检查'})
		except Exception as ex:
			print(ex)
			return  JsonResponse({'success':'false','msg':ex})

@login_required
def change_pwd_main_user(request):
	'''更新密码'''
	if  request.method == 'POST':
		try:

			id = request.POST.get('id')
			password = request.POST.get('password')
			dic = {
				"password": make_password(password),
			}
			if id is not None:
				obj = User.objects.filter(id=id).update(**dic)
				if  obj is not None:
					return JsonResponse({'success':'true','msg':'密码更新成功！'})
			else:
				return JsonResponse({'success':'false','msg':'密码没有更新成功，请您重新检查'})
		except Exception as ex:
			print(ex)
			return  JsonResponse({'success':'false','msg':ex})