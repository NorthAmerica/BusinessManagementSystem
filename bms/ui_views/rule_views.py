from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from bms.models import *
from bms.forms import *
from django.contrib.auth.models import Group
from bms.ui_views.view_shortcuts import get_org_obj

def fund_in_config(request):

	return render(request,'bms/rule_config/fund_in_config.html')

def fund_out_config(request):
	return render(request, 'bms/rule_config/fund_out_config.html')

def exchange_config(request):
	return render(request, 'bms/rule_config/exchange_config.html')

def get_org_tree(request):
	try:
		if request.method == 'POST':
			org_all = []
			if request.user.is_superuser:  # 超级管理员
				org_all = Organization.objects.all()
			elif request.user.identity == 'org':  # 机构管理员
				org_all = [get_org_obj(request)]

			Org_List = []
			for org in org_all:
				Org_List.append({
					'id': org.id,
					"text": org.name,
					'state': 'open',
				})
			return JsonResponse(Org_List, safe=False)

	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')

def get_global_fund_in(request):
	try:
		if request.method == 'POST':
			if request.POST.get('org_id')==0 or request.POST.get('org_id')=='0':
				global_fund_in = Fund_In_Rule.objects.filter(org=None).first()
				if  global_fund_in is not None:
					json_ret = {
						'org':'',
						'success':True,
						'begin_time':global_fund_in.begin_time,
						'end_time':global_fund_in.end_time,
						'week':[day for day in global_fund_in.week],
						'min_gateway':global_fund_in.min_gateway,
						'min_shortcut':global_fund_in.min_shortcut
					}
					return JsonResponse(json_ret, safe=False)
				else:
					return JsonResponse({'success':'false', 'msg': '没有满足条件的全局入金配置'})
			else:
				Org = Organization.objects.get(pk=request.POST.get('org_id'))
				global_fund_in = Fund_In_Rule.objects.filter(org=Org).first()
				if global_fund_in is not None:
					json_ret = {
						'org':Org.name,
						'success': True,
						'begin_time': global_fund_in.begin_time,
						'end_time': global_fund_in.end_time,
						'week': [day for day in global_fund_in.week],
						'min_gateway': global_fund_in.min_gateway,
						'min_shortcut': global_fund_in.min_shortcut
					}
					return JsonResponse(json_ret, safe=False)
				else:
					return JsonResponse({'success': 'false', 'msg': '该机构没有满足条件的入金配置'})
	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')

def add_fund_in(request):
	try:
		if request.method == 'POST':
			if request.user.is_superuser or request.user.identity == 'org':
				org = request.POST.get('org')
				begin_time = request.POST.get('begin_time')
				end_time = request.POST.get('end_time')
				week = request.POST.get('week')
				min_gateway = request.POST.get('min_gateway')
				min_shortcut = request.POST.get('min_shortcut')
				dic = {
					"org": Organization.objects.get(pk=org),
					"begin_time": begin_time,
					"end_time": end_time,
					"week": week,
					"min_gateway": min_gateway,
					'min_shortcut': min_shortcut,
					'operator':request.user.username
				}
				if Organization.objects.get(pk=org).fund_in_rule_set.all().count()==0:
					c_obj = Fund_In_Rule.objects.create(**dic)
					if c_obj is not None:
						return JsonResponse({'success': 'true', 'msg': '入金规则添加成功！'})
				else:
					row = Organization.objects.get(pk=org).fund_in_rule_set.all().update(**dic)
					if row != 0:
						return JsonResponse({'success': 'true', 'msg': '入金规则修改成功！'})
	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')


def get_global_fund_out(request):
	try:
		if request.method == 'POST':
			if request.POST.get('org_id')==0 or request.POST.get('org_id')=='0':
				global_fund_out = Fund_Out_Rule.objects.filter(org=None).first()
				if  global_fund_out is not None:
					json_ret = {
						'org':'',
						'success':True,
						'begin_time':global_fund_out.begin_time,
						'end_time':global_fund_out.end_time,
						'week':[day for day in global_fund_out.week],
						'max_count_each_day':global_fund_out.max_count_each_day,
						'max_money_each_day':global_fund_out.max_money_each_day,
						'max_money_each_time':global_fund_out.max_money_each_time
					}
					return JsonResponse(json_ret, safe=False)
				else:
					return JsonResponse({'success':'false', 'msg': '没有满足条件的全局出金配置'})
			else:
				Org = Organization.objects.get(pk=request.POST.get('org_id'))
				global_fund_out = Fund_Out_Rule.objects.filter(org=Org).first()
				if global_fund_out is not None:
					json_ret = {
						'org':Org.name,
						'success': True,
						'begin_time': global_fund_out.begin_time,
						'end_time': global_fund_out.end_time,
						'week': [day for day in global_fund_out.week],
						'max_count_each_day':global_fund_out.max_count_each_day,
						'max_money_each_day':global_fund_out.max_money_each_day,
						'max_money_each_time':global_fund_out.max_money_each_time
					}
					return JsonResponse(json_ret, safe=False)
				else:
					return JsonResponse({'success': 'false', 'msg': '该机构没有满足条件的出金配置'})
	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')

def add_fund_out(request):
	try:
		if request.method == 'POST':
			if request.user.is_superuser or request.user.identity == 'org':
				org = request.POST.get('org')
				begin_time = request.POST.get('begin_time')
				end_time = request.POST.get('end_time')
				week = request.POST.get('week')
				max_count_each_day = request.POST.get('max_count_each_day')
				max_money_each_day = request.POST.get('max_money_each_day')
				max_money_each_time = request.POST.get('max_money_each_time')
				dic = {
					"org": Organization.objects.get(pk=org),
					"begin_time": begin_time,
					"end_time": end_time,
					"week": week,
					"max_count_each_day": max_count_each_day,
					'max_money_each_day': max_money_each_day,
					'max_money_each_time': max_money_each_time,
					'operator':request.user.username
				}
				if Organization.objects.get(pk=org).fund_out_rule_set.all().count()==0:
					c_obj = Fund_Out_Rule.objects.create(**dic)
					if c_obj is not None:
						return JsonResponse({'success': 'true', 'msg': '出金规则添加成功！'})
				else:
					row = Organization.objects.get(pk=org).fund_out_rule_set.all().update(**dic)
					if row != 0:
						return JsonResponse({'success': 'true', 'msg': '出金规则修改成功！'})
	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')