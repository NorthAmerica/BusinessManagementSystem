from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from django.db import transaction
from bms.forms import *
from bms.tool_kit.view_shortcuts import get_org_obj

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
		return HttpResponseNotFound(ex)

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
					return JsonResponse({'success':False, 'msg': '没有满足条件的全局入金配置'}, safe=False)
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
					return JsonResponse({'success': False, 'msg': '该机构没有满足条件的入金配置'}, safe=False)
		else:
			return JsonResponse({'success': False, 'msg': 'POST only'}, safe=False)
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)

def add_fund_in(request):
	try:
		if request.method == 'POST':
			if request.user.is_superuser or request.user.identity == 'org': #前端限制必须选择机构进行修改
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
						return JsonResponse({'success': True, 'msg': '入金规则添加成功！'}, safe=False)
				else:
					row = Organization.objects.get(pk=org).fund_in_rule_set.all().update(**dic)
					if row != 0:
						return JsonResponse({'success': True, 'msg': '入金规则修改成功！'}, safe=False)
		else:
			return JsonResponse({'success': False, 'msg': 'POST only'}, safe=False)
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)


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
					return JsonResponse({'success':False, 'msg': '没有满足条件的全局出金配置'}, safe=False)
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
					return JsonResponse({'success': False, 'msg': '该机构没有满足条件的出金配置'}, safe=False)
		else:
			return JsonResponse({'success': False, 'msg': 'POST only'}, safe=False)
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)

def add_fund_out(request):
	try:
		if request.method == 'POST':
			if request.user.is_superuser or request.user.identity == 'org':#前端限制必须选择机构进行修改
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
						return JsonResponse({'success': True, 'msg': '出金规则添加成功！'}, safe=False)
				else:
					row = Organization.objects.get(pk=org).fund_out_rule_set.all().update(**dic)
					if row != 0:
						return JsonResponse({'success': True, 'msg': '出金规则修改成功！'}, safe=False)
		else:
			return JsonResponse({'success': False, 'msg': 'POST only'}, safe=False)
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)


def get_exchange_rule(request):
	'''获取交易询价时间设置'''
	try:
		if request.method == 'POST':
			if request.POST.get('org_id')==0 or request.POST.get('org_id')=='0':
				exchange_rule = Exchange_Rule.objects.filter(org=None)
				json_ret = {'success': True, 'org': ''}
			else:
				Org = Organization.objects.get(pk=request.POST.get('org_id'))
				exchange_rule = Exchange_Rule.objects.filter(org=Org)
				json_ret = {'success': True, 'org': Org.name}
			for rule in exchange_rule:
				if rule is not None:
					if rule.type == 'enquiry' and rule.option_type == 'stock':
						json_ret['enquiry_stock'] = {
							'begin_time': rule.begin_time,
							'end_time': rule.end_time,
							'week': [day for day in rule.week],
						}
					elif rule.type == 'enquiry' and rule.option_type == 'commodity':
						json_ret['enquiry_commodity'] = {
							'begin_time': rule.begin_time,
							'end_time': rule.end_time,
							'week': [day for day in rule.week],
						}
					elif rule.type == 'order' and rule.option_type == 'stock':
						json_ret['order_stock'] = {
							'begin_time': rule.begin_time,
							'end_time': rule.end_time,
							'week': [day for day in rule.week],
						}
					elif rule.type == 'order' and rule.option_type == 'commodity':
						json_ret['order_commodity'] = {
							'begin_time': rule.begin_time,
							'end_time': rule.end_time,
							'week': [day for day in rule.week],
						}
					elif rule.type == 'close' and rule.option_type == 'stock':
						json_ret['close_stock'] = {
							'begin_time': rule.begin_time,
							'end_time': rule.end_time,
							'week': [day for day in rule.week],
						}
					elif rule.type == 'close' and rule.option_type == 'commodity':
						json_ret['close_commodity'] = {
							'begin_time': rule.begin_time,
							'end_time': rule.end_time,
							'week': [day for day in rule.week],
						}
			return JsonResponse(json_ret, safe=False)
				# else:
				# 	return JsonResponse({'success': False, 'msg': '没有满足条件的全局出金配置'})
				# else:
				# 	return JsonResponse({'success': 'false', 'msg': '该机构没有满足条件的出金配置'})
		else:
			return JsonResponse({'success': False, 'msg': 'POST only'}, safe=False)
	except Exception as ex:
		print(ex)
		return render(request, './bms/404.html')

@transaction.atomic
def add_exchange_rule(request):
	'''新增交易询价时间设置'''
	try:
		if request.method == 'POST':
			if request.user.is_superuser or request.user.identity == 'org':
				org_id = request.POST.get('org')
				org_obj = Organization.objects.get(pk=org_id)

				rule_list = ['enquiry_stock','enquiry_commodity','order_stock',
				             'order_commodity','close_stock','close_commodity']

				for rule_name in rule_list:
					begin_time = '%s[begin_time]'%rule_name
					end_time = '%s[end_time]'%rule_name
					week='%s[week]'%rule_name
					option_type = rule_name.split('_')[1]
					type = rule_name.split('_')[0]
					insert_dict = {
						"org": org_obj,
						"begin_time": request.POST.get(begin_time),
						"end_time": request.POST.get(end_time),
						"week": request.POST.get(week),
						'option_type': option_type,
						'type': type,
						'operator': request.user.username
					}
					if org_obj.exchange_rule_set.filter(option_type=option_type).filter(
							type=type).count() == 0:
						Exchange_Rule.objects.create(**insert_dict)
					else:
						org_obj.exchange_rule_set.filter(option_type=option_type).filter(
							type=type).all().update(**insert_dict)

				return JsonResponse({'success': True, 'msg': '交易询价时间设置添加成功！'}, safe=False)
		else:
			return JsonResponse({'success': False, 'msg': 'POST only'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)

def notional_principal_config(request):

	return render(request,'./bms/rule_config/notional_principal_config.html')

def get_notional_principal(request):
	'''获取名义本金设置'''
	try:
		if request.method == 'POST':
			# all = Notional_Principal.objects.all()
			eaList = []
			for np in Notional_Principal.objects.all():
				eaList.append({
					'id': np.id,
					'number': np.number
				})
			return JsonResponse(eaList, safe=False)
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)

