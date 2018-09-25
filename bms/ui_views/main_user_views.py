from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from bms.models import *
from bms.forms import *
from django.contrib.auth.models import Group
from bms.ui_views.view_shortcuts import get_org_user_list,get_org_id

@login_required
def main_user_list(request):
	if  request.method == 'POST':
		try:
			page = request.POST.get("page")
			rows = request.POST.get("rows")
			user_all= []
			if request.user.is_superuser: #超级管理员
				user_all =list(User.objects.all())#.values_list('username','mobile_phone','position')
			elif request.user.identity =='org': #机构管理员
				#获取页面选择的组下的用户
				if request.POST.get('group_id') is not None:
					group = Group.objects.get(pk=request.POST.get('group_id'))
					user_all = list(group.user_set.all())
				elif request.POST.get('agency_id') is not None:
					agency = Agency.objects.get(pk=request.POST.get('agency_id'))
					user_all =[agency_user_set.user for agency_user_set in agency.agency_user_set.all()]
				else:
					#获取当前用户同机构下的用户
					user_all = get_org_user_list(request)
			elif request.user.identity=='agency': #归属管理员
				if request.POST.get('group_id') is not None:
					group = Group.objects.get(pk=request.POST.get('group_id'))
					user_all = list(group.user_set.all())
				if request.POST.get('agency_id') is not None:
					agency = Agency.objects.get(pk=request.POST.get('agency_id'))
					user_all =[agency_user_set.user for agency_user_set in agency.agency_user_set.all()]
			#分页判断
			if page is not None and rows is not None:
				#有分页
				paginator = Paginator(user_all, rows)

				try:
					users = paginator.page(page)
				except PageNotAnInteger:
					users = paginator.page(1)
				except EmptyPage:
					users = paginator.page(paginator.num_pages)
				eaList=[]
				for user in users.object_list:
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
			else:
				#无分页
				User_List = []
				for user in user_all:
					User_List.append({
						'id': user.id,
						"username": user.username,
						"mobile_phone": user.mobile_phone,
						'last_name': user.last_name,
						'email': user.email,
						"position": user.position,
						"is_active": user.is_active
					})
				return JsonResponse(User_List,safe=False)
		except Exception as ex:
			print(ex)
			#Change_Info.objects.create(initiator=request.user.username,receiver='',event_type='ERROR',)
	else:
		return render(request, 'bms/user_config/org_user_config.html')

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
			# org_id = get_org_id(request)

			if request.POST.get('agency_id') is not None:
				#新增代理管理员
				dic = {
					"username": username,
					"password": make_password(password),
					"last_name": last_name,
					"email": email,
					"position": position,
					"mobile_phone": mobile_phone,
					"is_active": is_active,
					"identity": 'agency'
				}

				obj = User.objects.create(**dic)
				if obj is not None:
					#如果是选择的新增代理用户
					ag_user = {
						"user": obj,
						"agency": Agency.objects.get(pk=request.POST.get('agency_id')),
						"operator": request.user.username
					}
					create_user = Agency_User.objects.create(**ag_user)
					if create_user is not None:
						#Change_Info.objects.create(initiator=request.user.username, receiver=create_user.user.username, event_type='ERROR', )
						return JsonResponse({'success': 'true', 'msg': '新用户添加成功！'})
					else:
						return JsonResponse({'success': 'false', 'msg': '新用户没有添加成功，请您重新检查'})
				else:
					return JsonResponse({'success':'false','msg':'新用户没有添加成功，请您重新检查'})
			else:
				# 新增机构管理员
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
				if obj is not None:
					#如果是新增机构用户
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