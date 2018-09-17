from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponse
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from bms.models import *
from bms.forms import *
from django.contrib.auth.models import Group
from bms.ui_views.view_shortcuts import get_org_obj,get_all_son_agency,get_ageny_id


def agency_config(request):
	return render(request, 'bms/agency_config/agency_config.html')

def agency_user_config(request):
	return render(request, 'bms/agency_config/agency_user_config.html')


def get_agency_tree(request):
	'''归属树'''
	try:
		if  request.method == 'POST':
			if request.user.identity =='org':

				first = Agency.objects.filter(f_agency=None).filter(organization=get_org_obj(request))

				return_json=[{
					'id': '0',
					'text': '所有归属',
					'state': 'open',
					'children':get_all_son_agency(first)
				}]
				return JsonResponse(return_json,safe=False)
			elif request.user.identity == 'agency':

				first1 = Agency.objects.filter(pk=get_ageny_id(request))#
				# test = get_all_son_agency(first1)
				return_json1 = [{
					'id': '0',
					'text': '所有归属',
					'state': 'open',
					'children': get_all_son_agency(first1)
				}]
				return JsonResponse(return_json1, safe=False)
			else:
				return_json2 =[{
					'id': '0',
					'text': '所有归属',
					'state': 'open'}]
				return JsonResponse(return_json2,safe=False)

	except Exception as ex:
		print(ex)
		return render(request,'./bms/404.html')

def get_agency_list(request):
	'''归属列表'''
	try:
		if  request.method == 'POST':
			if request.POST.get('agency_id') is not None:
				agency = Agency.objects.get(pk=request.POST.get('agency_id'))
				agency_json = []
				agency_json.append({
					'id': agency.id,
					"name": agency.name,
					"organization": agency.organization.name,
					'rebate_x': agency.rebate_x,
					'rebate_y': agency.rebate_y,
					"rebate_z": agency.rebate_z,
					"f_agency_id": 0 if agency.f_agency is None else agency.f_agency.id,
					"f_agency": '无' if agency.f_agency is None else agency.f_agency.name,
					'invite_num': agency.invite_num,
					'is_freeze':agency.is_freeze
				})
				return JsonResponse(agency_json, safe=False)
			else:
				return JsonResponse([], safe=False)
				# return Http404('用户身份有误，请重新登陆')
	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')

def add_agency(request):
	'''新增归属'''
	try:
		if request.method == 'POST':
			name = request.POST.get('name')
			rebate_x = request.POST.get('rebate_x') if request.POST.get('rebate_x') is not None and request.POST.get('rebate_x')!='' else 0
			rebate_y = request.POST.get('rebate_y') if request.POST.get('rebate_y') is not None and request.POST.get('rebate_y')!='' else 0
			rebate_z = request.POST.get('rebate_z') if request.POST.get('rebate_z') is not None and request.POST.get('rebate_z')!='' else 0
			is_freeze = request.POST.get('is_freeze')
			f_agency_id = request.POST.get('f_agency')
			invite_num = invite_num_key()

			if request.user.identity =='org':
				#如果是机构管理员新增归属
				dic={}
				if f_agency_id != 0 and f_agency_id != '0':
					dic = {
						"name": name,
						"rebate_x": rebate_x,
						"rebate_y": rebate_y,
						"rebate_z": rebate_z,
						"is_freeze": is_freeze,
						"invite_num": invite_num,
						'organization': request.user.org_user.organization,
						'f_agency': Agency.objects.get(pk=f_agency_id),
						'grade': Agency.objects.get(pk=f_agency_id).grade+1
					}
				else:
					dic = {
						"name": name,
						"rebate_x": rebate_x,
						"rebate_y": rebate_y,
						"rebate_z": rebate_z,
						"is_freeze": is_freeze,
						"invite_num": invite_num,
						'organization': request.user.org_user.organization,
						'grade': 1,
					}
				create_a = Agency.objects.create(**dic)
				if create_a is not None:
					return JsonResponse({'success': 'true', 'msg': '新用户添加成功！'})
				else:
					return JsonResponse({'success': 'false', 'msg': '新用户没有添加成功，请您重新检查'})
			elif request.user.identity=='agency':
				# 如果是归属管理员新增归属
				dic = {
					"name": name,
					"rebate_x": rebate_x,
					"rebate_y": rebate_y,
					"rebate_z": rebate_z,
					"is_freeze": True,
					"invite_num": invite_num,
					'organization':request.user.agency_user.agency.organization,
					'f_agency':request.user.agency_user.agency,
					'grade': request.user.agency_user.agency.grade+1
				}
				create_a = Agency.objects.create(**dic)
				if create_a is not None:
					return JsonResponse({'success': 'true', 'msg': '新用户添加成功！'})
				else:
					return JsonResponse({'success': 'false', 'msg': '新用户没有添加成功，请您重新检查'})
	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')

def update_agency(request):
	'''更新归属'''
	try:
		if request.method == 'POST':
			name = request.POST.get('name')
			rebate_x = request.POST.get('rebate_x') if request.POST.get('rebate_x') is not None and request.POST.get(
				'rebate_x') != '' else 0
			rebate_y = request.POST.get('rebate_y') if request.POST.get('rebate_y') is not None and request.POST.get(
				'rebate_y') != '' else 0
			rebate_z = request.POST.get('rebate_z') if request.POST.get('rebate_z') is not None and request.POST.get(
				'rebate_z') != '' else 0
			is_freeze = request.POST.get('is_freeze')
			f_agency_id = request.POST.get('f_agency')
			dic = {
				"name": name,
				"rebate_x": rebate_x,
				"rebate_y": rebate_y,
				"rebate_z": rebate_z,
				"is_freeze": is_freeze,
				'f_agency': Agency.objects.get(pk=f_agency_id),#还没添加同级限制！！！！！！！！！！！！
				'grade': Agency.objects.get(pk=f_agency_id).grade + 1
			}
			create_a = Agency.objects.create(**dic)
			if create_a is not None:
				return JsonResponse({'success': 'true', 'msg': '新用户添加成功！'})
			else:
				return JsonResponse({'success': 'false', 'msg': '新用户没有添加成功，请您重新检查'})
	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')
