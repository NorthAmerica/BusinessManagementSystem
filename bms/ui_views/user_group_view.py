from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json
from bms.models import *
from bms.forms import *
from bms.ui_views.view_shortcuts import get_org_user_list, get_org_id

def user_group(request):
	return render(request, 'bms/user_config/user_group_config.html')

def group_list(request):
	if request.method == 'POST':
		try:
			all_group = Special_Group.objects.all()
			child = []
			for group in all_group:
				child.append(
					{'id': group.id,
					 'text': group.name,
					 'state': 'open'
					 }
				)
			item = [{
				'id': '0',
				'text': '所有组',
				'state': 'open',
				'children':child}]
			return HttpResponse(json.dumps(item))
		except Exception as ex:
			print(ex)
			return JsonResponse(({'id': '0', 'text': '取角色异常'}))


def user_list(request):
	pass
