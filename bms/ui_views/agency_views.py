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
				test = get_all_son_agency(first1)
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

