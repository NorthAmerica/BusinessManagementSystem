from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
from bms.models import *
from bms.ui_views.view_shortcuts import get_org_obj,get_all_son_agency,get_ageny_id,auto_add_permissions,get_choices_text,get_multi_text

def client_list(request):
	return render(request, 'bms/client_config/client_list.html')

def get_client_list(request):
	try:
		if  request.method == 'POST':
			page = request.POST.get("page")
			rows = request.POST.get("rows")
			json_data_list={}
			if request.POST.get('agency_id') is not None and request.POST.get('agency_id')!='0'and request.POST.get('agency_id')!=0: #如果按归属查询归属下客户
				client_by_agency = list(Client.objects.filter(agency=Agency.objects.get(pk=request.POST.get('agency_id'))))
				paginator = Paginator(client_by_agency, rows)
				try:
					clients = paginator.page(page)
				except PageNotAnInteger:
					clients = paginator.page(1)
				except EmptyPage:
					clients = paginator.page(paginator.num_pages)
				eaList = []
				for client in clients.object_list:
					eaList.append({
						'id': client.id,
						'name':client.name,
						'mobile_phone':client.mobile_phone,
						'mailbox':client.mailbox,
						'organization':client.organization.name,
						'agency':client.agency.name,
						'status':get_choices_text(STATUS_CHOICES,client.status),
						'is_freeze':'是' if client.is_freeze else '否',
						'allow_business_id': client.allow_business,
						'allow_business': get_multi_text(client.allow_business)
					})
				json_data_list = {
					'total': paginator.count,
					'rows': eaList
				}
			else:   #默认查询机构下所有客户
				client_by_org =list(Client.objects.filter(organization=get_org_obj(request)))
				paginator = Paginator(client_by_org, rows)
				try:
					clients = paginator.page(page)
				except PageNotAnInteger:
					clients = paginator.page(1)
				except EmptyPage:
					clients = paginator.page(paginator.num_pages)
				eaList = []
				for client in clients.object_list:
					eaList.append({
						'id': client.id,
						'name': client.name,
						'mobile_phone': client.mobile_phone,
						'mailbox': client.mailbox,
						'organization': client.organization.name,
						'agency': client.agency.name,
						'status': get_choices_text(STATUS_CHOICES,client.status),
						'is_freeze': '是' if client.is_freeze else '否',
						'allow_business_id': client.allow_business,
						'allow_business': get_multi_text(client.allow_business)
					})
				json_data_list = {
					'total': paginator.count,
					'rows': eaList
				}

			return JsonResponse(json_data_list, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse([], safe=False)