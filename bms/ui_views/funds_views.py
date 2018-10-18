from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from bms.models.choices_for_model import FUND_STATUS_CHOICES
from bms.forms import *
from bms.tool_kit.view_shortcuts import get_agency_obj,get_org_obj,get_org_id,get_agency_id,page_helper,date_joined_sort
from bms.tool_kit.fund_shortcuts import offline_org_balance,offline_agency_balance
from bms.tool_kit.views_decorator import check_fund_rule

@login_required
def funds_list(request):
	if request.user.identity == 'org':
		account_balance = get_org_obj(request).account_balance
	elif request.user.identity == 'agency':
		account_balance =get_agency_obj(request).account_balance
	return render(request, 'bms/funds_config/funds_list.html',locals())

@login_required
def fund_detail_list(request):
	'''资金明细列表'''
	try:
		if request.method == 'POST':
			page = request.POST.get("page")
			rows = request.POST.get("rows")
			fund_list = []
			if request.user.identity =='org':
				fund_list.extend(list(Fund_Detail.objects.filter(org=get_org_obj(request))))
				agency_ids = Agency.objects.filter(organization=get_org_obj(request)).values('id')
				fund_list.extend(list(Fund_Detail.objects.filter(agency__id__in=agency_ids)))
				client_ids = Client.objects.filter(organization=get_org_obj(request)).values('id')
				fund_list.extend(list(Fund_Detail.objects.filter(client__id__in=client_ids)))
			elif request.user.identity=='agency':
				fund_list.extend(list(Fund_Detail.objects.filter(agency=get_agency_obj(request))))
				client_ids = Client.objects.filter(agency=get_agency_obj(request)).values('id')
				fund_list.extend(list(Fund_Detail.objects.filter(client__id__in=client_ids)))
			fund_list.sort(key=date_joined_sort,reverse=True)
			results, total = page_helper(fund_list, rows, page)
			eaList = []
			for fund in results.object_list:
				eaList.append({
					'id': fund.id,
					'serial_number': fund.serial_number,
					'client': fund.client.name if fund.client is not None else '',
					'org': fund.org.name if fund.org is not None else '',
					'agency': fund.agency.name if fund.agency is not None else '',
					'balance_before': fund.balance_before,
					'balance_after': fund.balance_after,
					'balance_change': fund.balance_change,
					'fund_state': fund.get_fund_state_display(),
					'fund_type': fund.get_fund_type_display(),
					'fund_audit': fund.get_fund_audit_display(),
					'date_joined':'' if fund.date_joined is None else fund.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
					'auditor': fund.auditor,
					'audit_time':'' if fund.audit_time is None else fund.audit_time.strftime("%Y-%m-%d %H:%M:%S")
				})

			json_data_list = {
				'total': total,
				'rows': eaList
			}
			return JsonResponse(json_data_list, safe=False)
		else:
			return JsonResponse({}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({}, safe=False)

def get_fund_audit(request):
	'''获取资金审核状态'''
	try:
		if request.method == 'POST':
			return_json = []
			for status in FUND_STATUS_CHOICES:
				return_json.append({
					'id': status[0],
					'text': status[1]
				})
			return JsonResponse(return_json, safe=False)

	except Exception as ex:
		print(ex)
		return_ex = [{
			'id': '0',
			'text': ex.__str__()
		}]
		return JsonResponse(return_ex, safe=False)

@transaction.atomic
def fund_audit(request):
	'''资金状态审核'''
	try:
		if request.method=='POST':
			fund_id = request.POST.get('fund_id',None)
			fund_audit = request.POST.get('fund_audit',None)
			if fund_id is not None and fund_audit is not None:
				find_fund_detail = Fund_Detail.objects.filter(pk=fund_id)
				if find_fund_detail.exists():
					if fund_audit=='agree':
						fund_detail = find_fund_detail.first()
						if fund_detail.org is not None:
							# 不能对机构资金明细进行审核
							return JsonResponse({'success': False, 'msg': '不能对机构资金明细进行审核！'}, safe=False)
						if fund_detail.client is not None:
							Client.objects.filter(pk=fund_detail.client_id).update(account_balance=fund_detail.balance_after)
						if fund_detail.agency is not None:
							if request.user.identity == 'org':
								# 上级才能对资金明细进行审核
								Agency.objects.filter(pk=fund_detail.agency_id).update(account_balance=fund_detail.balance_after)
							else:
								return JsonResponse({'success': False, 'msg': '只有上级才能对资金明细进行审核！'}, safe=False)
					find_fund_detail.update(fund_audit=fund_audit)
					return JsonResponse({'success': True, 'msg': '更新成功！'}, safe=False)
		return JsonResponse({'success': False, 'msg': '参数有误！'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)

@transaction.atomic
@check_fund_rule('in')
def offline_balance_change(request):
	'''线下资金出入金'''
	global false_msg
	try:
		if request.method=='POST':
			balance_change = request.POST.get('balance_change', None)
			type = request.POST.get('type', None)

			if balance_change is not None and type is not None:

				if request.user.identity == 'org':
					is_ok,false_msg = offline_org_balance(get_org_id(request),type,balance_change,request.user.username)
					if is_ok:
						return JsonResponse({'success': True, 'msg': '出入金申请已提交'}, safe=False)

				elif request.user.identity == 'agency':
					is_ok,false_msg = offline_agency_balance(get_agency_id(request),type,balance_change,request.user.username)
					if is_ok:
						return JsonResponse({'success': True, 'msg': '出入金申请已提交'}, safe=False)

		return JsonResponse({'success': False, 'msg': false_msg}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)