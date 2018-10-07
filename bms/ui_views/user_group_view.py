from django.shortcuts import render
from django.http import JsonResponse
from bms.models import *
from django.contrib.auth.models import Group
from bms.tool_kit.view_shortcuts import get_org_obj,get_agency_obj

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
				all_group = Special_Group.objects.filter(agency=get_agency_obj(request))
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
			return JsonResponse({'id': '0', 'text': '取角色异常'}, safe=False)


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
			return JsonResponse({'success':True,'msg':'用户添加组成功！'}, safe=False)
		except Exception as ex:
			print(ex)
			return  JsonResponse({'success':False,'msg':ex}, safe=False)

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
			return JsonResponse({'success':True,'msg':'用户添加组成功！'}, safe=False)
		except Exception as ex:
			print(ex)
			return  JsonResponse({'success':False,'msg':ex}, safe=False)
