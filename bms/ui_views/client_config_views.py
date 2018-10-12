from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bms.models import *
from django.contrib.auth.hashers import make_password
from bms.tool_kit.view_shortcuts import get_org_obj, send_msg_to_client,get_multi_text,page_helper

def client_list(request):
	return render(request, 'bms/client_config/client_list.html')

def get_client_list(request):
	'''客户列表'''
	try:
		if  request.method == 'POST':
			page = request.POST.get("page")
			rows = request.POST.get("rows")
			client_list = []
			if request.POST.get('agency_id') is not None and request.POST.get('agency_id')!='0'and request.POST.get('agency_id')!=0:
				#如果按归属查询归属下客户
				client_list.extend(list(Client.objects.filter(agency=Agency.objects.get(pk=request.POST.get('agency_id',None)))))
			else:
				#默认查询机构下所有客户
				client_list.extend(list(Client.objects.filter(organization=get_org_obj(request))))
			results, total = page_helper(client_list,rows,page)
			eaList = []
			for client in results.object_list:
				eaList.append({
					'id': client.id,
					'name': client.name,
					'mobile_phone': client.mobile_phone,
					'mailbox': client.mailbox,
					'organization': client.organization.name,
					'agency': client.agency.name,
					'status': client.get_status_display(),
					'is_freeze': '是' if client.is_freeze else '否',
					'allow_business_id': client.allow_business,
					'allow_business': get_multi_text(client.allow_business),
					'identity_card':client.identity_card,
					'bank_image':client.bank_image.name,
					'bank_card':client.bank_card,
					'bank_name':client.bank_name,
					'open_city':client.open_city,
					'bank_branch':client.bank_branch
				})
			json_data_list = {
				'total': total,
				'rows': eaList
			}
			return JsonResponse(json_data_list, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse([], safe=False)

def freeze_client(request):
	'''冻结和解冻'''
	try:
		is_freeze = request.POST.get("is_freeze")
		client_id = request.POST.get("client_id")
		if is_freeze is not None and client_id is not None:
			find_client = Client.objects.filter(pk=client_id)
			if find_client.exists():
				update_data = {
					'is_freeze': is_freeze == str(True)
				}
				rows = find_client.update(**update_data)
				if rows!=0:
					return JsonResponse({'success': True, 'msg': '更新完成。'}, safe=False)
		return JsonResponse({'success': False, 'msg': '更新数量为0。'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)

def change_client_pwd(request):
	'''修改客户密码'''
	try:
		if request.method == 'POST':
			client_id = request.POST.get('client_id')
			password = request.POST.get('password')
			dic = {
				"password": make_password(password),
			}
			count = Client.objects.filter(pk=client_id).update(**dic)
			if count != 0:
				return JsonResponse({'success': True, 'msg': '密码更新成功！'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex})

def check_client(request):
	'''审核实名认证'''
	try:
		if request.method == 'POST':
			client_id = request.POST.get('client_id')
			check = request.POST.get('check')
			find_clinet = Client.objects.filter(pk=client_id)
			if find_clinet.exists():
				if check=='true':
					dic = {
						"status": STATUS_CHOICES[2][0],
						"status_before": find_clinet.first().status,
						"verifier":request.user.username
					}
					msg='恭喜您，您的实名认证已通过！'
				else:
					dic = {
						"status": STATUS_CHOICES[0][0],
						"status_before":find_clinet.first().status,
						"verifier":request.user.username
					}
					msg='非常遗憾的通知您，您的实名认证未能通过，请重新提交真实的认证信息。'
				count = find_clinet.update(**dic)
				if count != 0:
					send_msg_to_client(request.user.username,'审批实名认证通知',msg,client_id)
					return JsonResponse({'success': True, 'msg': '审核完成！'}, safe=False)
		return JsonResponse({'success': False, 'msg': '未查询到相关数据！'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex})

def allow_business(request):
	'''允许的业务'''
	try:
		if request.method == 'POST':
			client_id = request.POST.get('client_id')
			allow_business = request.POST.get('allow_business')
			find_clinet = Client.objects.filter(pk=client_id)
			if find_clinet.exists():
				dic = {
					"allow_business": allow_business
				}
				count = find_clinet.update(**dic)
				if count != 0:
					return JsonResponse({'success': True, 'msg': '更新完成！'}, safe=False)
		return JsonResponse({'success': False, 'msg': '未查询到相关数据！'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex})