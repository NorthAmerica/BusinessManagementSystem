from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from bms.models import *
from django.contrib.auth.models import Group
from bms.ui_views.view_shortcuts import get_org_obj,get_ageny_obj

def user_group(request):
	return render(request, 'bms/user_config/user_group_config.html')

def group_list(request):
	if request.method == 'POST':
		try:
			all_group=[]
			if request.user.is_superuser:
				all_group = Special_Group.objects.all()
			elif request.user.identity =='org':
				all_group = Special_Group.objects.filter(org=get_org_obj(request))
			elif request.user.identity=='agency':
				all_group = Special_Group.objects.filter(agency=get_ageny_obj(request))
			child = []
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
				'children':child}]
			return JsonResponse(item,safe=False)
			# return HttpResponse(json.dumps(item))
		except Exception as ex:
			print(ex)
			return JsonResponse(({'id': '0', 'text': '取角色异常'}))


def add_user_to_group(request):
	if request.method == 'POST':
		try:

			group_id = request.POST.get('RoleID')
			users_id = request.POST.get('UserIDs')
			if group_id is not None and users_id is not None:
				group = Group.objects.get(pk=group_id)

				users = str(users_id).split(",")
				for user_id in users:
					user = User.objects.get(pk=user_id)
					group.user_set.add(user)
			return JsonResponse({'success':'true','msg':'用户添加组成功！'})
		except Exception as ex:
			print(ex)
			return  JsonResponse({'success':'false','msg':ex})

def remove_user_from_group(request):
	if request.method == 'POST':
		try:
			group_id = request.POST.get('RoleID')
			users_id = request.POST.get('UserIDs')
			if group_id is not None and users_id is not None:
				group = Group.objects.get(pk=group_id)

				users = str(users_id).split(",")
				for user_id in users:
					user = User.objects.get(pk=user_id)
					group.user_set.remove(user)
			return JsonResponse({'success':'true','msg':'用户添加组成功！'})
		except Exception as ex:
			print(ex)
			return  JsonResponse({'success':'false','msg':ex})
