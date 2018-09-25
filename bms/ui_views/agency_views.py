from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponse
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from bms.models import *
from bms.ui_views.view_shortcuts import auto_add_permissions
from bms.ui_views.view_shortcuts import get_org_obj,get_all_son_agency,get_ageny_id
import logging


def agency_config(request):
	return render(request, 'bms/agency_config/agency_config.html')

def agency_user_config(request):
	return render(request, 'bms/agency_config/agency_user_config.html')


def get_agency_tree(request):
	'''归属树'''
	try:
		if  request.method == 'POST':
			if request.user.identity =='org': #如果是机构管理员

				first = Agency.objects.filter(f_agency=None).filter(organization=get_org_obj(request))

				return_json=[{
					'id': '0',
					'text': '所有归属',
					'state': 'open',
					'children':get_all_son_agency(first)
				}]
				return JsonResponse(return_json,safe=False)
			elif request.user.identity == 'agency': #如果是归属管理员

				first1 = Agency.objects.filter(f_agency=get_ageny_id(request))#

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
					'invite_url':request.get_host()+'/register?code='+agency.invite_num,
					'invite_num': agency.invite_num,
					'is_freeze':agency.is_freeze
				})
				return JsonResponse(agency_json, safe=False)
			else:
				return JsonResponse([], safe=False)
				# return Http404('用户身份有误，请重新登陆')
	except Exception as ex:
		print(ex)
		return JsonResponse([], safe=False)


@transaction.atomic
def add_agency(request):
	'''新增归属'''
	try:
		if request.method == 'POST':
			name = request.POST.get('name')
			rebate_x = request.POST.get('rebate_x') if request.POST.get('rebate_x') is not None and request.POST.get('rebate_x')!='' else 0
			rebate_y = request.POST.get('rebate_y') if request.POST.get('rebate_y') is not None and request.POST.get('rebate_y')!='' else 0
			rebate_z = request.POST.get('rebate_z') if request.POST.get('rebate_z') is not None and request.POST.get('rebate_z')!='' else 0
			is_freeze = request.POST.get('is_freeze')
			f_agency_id = request.POST.get('f_agency') if request.POST.get('f_agency') is not None and request.POST.get('f_agency')!='' else 0
			invite_num = invite_num_key()
			dic = {}
			if request.user.identity =='org':
				#如果是机构管理员新增归属
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
			elif request.user.identity=='agency':
				# 如果是归属管理员新增归属
				dic = {
					"name": name,
					"rebate_x": rebate_x,
					"rebate_y": rebate_y,
					"rebate_z": rebate_z,
					"is_freeze": False,
					"invite_num": invite_num,
					'organization':request.user.agency_user.agency.organization,
					'f_agency':request.user.agency_user.agency if request.POST.get('f_agency')=='null' else Agency.objects.get(pk=request.POST.get('f_agency')),
					'grade': request.user.agency_user.agency.grade+1
				}
			create_a = Agency.objects.create(**dic)
			auto_add_permissions(create_a, request, 'agency')
			if create_a is not None:
				return JsonResponse({'success': True, 'msg': '新归属添加成功！'}, safe=False)
			else:
				return JsonResponse({'success': False, 'msg': '新归属没有添加成功，请您重新检查'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)

def update_agency(request):
	'''更新归属'''
	try:
		if request.method == 'POST':
			id = request.POST.get('id')
			name = request.POST.get('name')
			rebate_x = request.POST.get('rebate_x') if request.POST.get('rebate_x') is not None and request.POST.get(
				'rebate_x') != '' else 0
			rebate_y = request.POST.get('rebate_y') if request.POST.get('rebate_y') is not None and request.POST.get(
				'rebate_y') != '' else 0
			rebate_z = request.POST.get('rebate_z') if request.POST.get('rebate_z') is not None and request.POST.get(
				'rebate_z') != '' else 0
			is_freeze = request.POST.get('is_freeze')
			f_agency_id = request.POST.get('f_agency')

			dic = {}
			if f_agency_id != 0 and f_agency_id != '0':
				select_f_agency = Agency.objects.get(pk=f_agency_id)
				update_agency = Agency.objects.get(pk=id)

				if select_f_agency.grade!=update_agency.f_agency.grade:
					return JsonResponse({'success': False, 'msg': '上级归属必须同等级转换'}, safe=False)
				if select_f_agency.organization_id!=update_agency.f_agency.organization_id:
					return JsonResponse({'success': False, 'msg': '上级归属不能跨机构转换'}, safe=False)

				dic = {
					"name": name,
					"rebate_x": rebate_x,
					"rebate_y": rebate_y,
					"rebate_z": rebate_z,
					"is_freeze": is_freeze,
					'f_agency': select_f_agency,
					'grade': select_f_agency.grade + 1
				}
			else:
				dic = {
					"name": name,
					"rebate_x": rebate_x,
					"rebate_y": rebate_y,
					"rebate_z": rebate_z,
					"is_freeze": is_freeze
				}
			create_a = Agency.objects.filter(pk=id).update(**dic)
			if create_a is not None:
				return JsonResponse({'success': True, 'msg': '归属更新成功！'}, safe=False)
			else:
				return JsonResponse({'success': False, 'msg': '归属没有更新成功，请您重新检查'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)


def agency_group_config(request):
	return render(request,'bms/agency_config/agency_group_config.html')

def get_agency_group(request):
	try:
		if request.method == 'POST':
			all_group = []
			if request.POST.get('agency_id') is not None:
				all_group = Special_Group.objects.filter(agency=Agency.objects.get(pk=request.POST.get('agency_id')))
			child = []
			if  all_group is None or len(all_group)==0:
				item = [{
					'id': '0',
					'text': '没有任何组',
					'state': 'open',
					'children': child}]
				return JsonResponse(item, safe=False)
			else:
				for group in all_group:
					child.append(
						{'id': group.id,
						 'text': group.name,
						 'state': 'open'
						 })
				item = [{
					'id': '0',
					'text': '所有组',
					'state': 'open',
					'children': child}]
				return JsonResponse(item, safe=False)

	except Exception as ex:
		print(ex)
		return JsonResponse({'id': '0', 'text': '取角色异常'}, safe=False)