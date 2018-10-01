from guardian.shortcuts import assign_perm
from django.contrib.auth.hashers import make_password
from multiselectfield.db.fields import MSFList
from bms.models import *

def get_org_user_list(request):
	'''从登陆用户获取所属机构管理员列表'''
	if request.user is not None and request.user.identity == 'org':
		all_org_user = []
		org_id = get_org_id(request)
		list_org_user = list(Org_User.objects.filter(organization_id=org_id))
		return [org_user.user for org_user in list_org_user]

	else:
		return None

def get_agency_user_list(request):
	'''从登陆用户获取所属代理管理员列表'''
	if request.user is not None and request.user.identity == 'agency':
		all_agency_user = []
		agency_id = get_agency_id(request)
		list_agency_user = list(Agency_User.objects.filter(agency_id=agency_id))
		return [agency_user.user for agency_user in list_agency_user]

	else:
		return None

def get_agency_id(request):
	'''从登陆用户获取所属代理ID'''
	if  request.user is not None and request.user.identity =='agency':
		return request.user.agency_user.agency_id
	else:
		return None

def get_org_id(request):
	'''从登陆用户获取所属机构ID'''
	if  request.user is not None and request.user.identity == 'org':
		return request.user.org_user.organization_id
	else:
		raise PermissionError()

def get_org_obj(request):
	'''从登陆用户获取所属机构ID'''
	if  request.user is not None and request.user.identity == 'org':
		return request.user.org_user.organization
	else:
		raise PermissionError()

def get_org_name(request):
	'''从登陆用户获取所属机构名称'''
	if  request.user is not None and request.user.identity == 'org':
		return request.user.org_user.organization.name
	else:
		return '广州金艮投资有限公司'

def get_ageny_id(request):
	if  request.user is not None and request.user.identity == 'agency':
		return request.user.agency_user.agency.id
	else:
		raise PermissionError()

def get_ageny_obj(request):
	if  request.user is not None and request.user.identity == 'agency':
		return request.user.agency_user.agency
	else:
		raise PermissionError()

def get_agency_name(request):
	'''从登陆用户获取所属机构名称'''
	if  request.user is not None and request.user.identity == 'agency':
		return request.user.agency_user.agency.name
	else:
		return '广州金艮投资有限公司'

def get_org_agency_set(request):
	if  request.user is not None and request.user.identity =='org':
		return request.user.org_user.organization.agency_set
	else:
		return None


def get_all_son_agency(first,show_self=False):
	'''递归获得所有子归属'''
	try:
		child = []
		for ag in first:
			child_agency = Agency.objects.filter(f_agency=ag)
			if len(child_agency)>0:
				child.append(
					{'id': ag.id,
					 'text': ag.name,
					 'iconCls': 'icon-man' if ag.is_freeze is False else 'icon-lock',
					 'state': 'open',
					 'children':get_all_son_agency(child_agency)
					 })

			else:
				child.append(
					{'id': ag.id,
					 'text': ag.name,
					 'iconCls': 'icon-man' if ag.is_freeze is False else 'icon-lock',
					 'state': 'open'
					 })

		return child
	except Exception as ex:
		print(ex)


def auto_add_permissions(obj,request,org_agency):
	'''
	自动复制组模板
	自动分配权限
	自动创建管理员
	'''
	# 新增管理员
	if org_agency=='org':
		all_temp = Group_Template.objects.filter(type='org')
		new_user = User.objects.create(username=obj.name + '总管理员', identity='org', password=make_password('686868'))
		Org_User.objects.create(user=new_user, organization=obj, operator=request.user.username)
		for temp in all_temp:
			all_perm = [perm for perm in temp.permissions.all()]
			all_object_perm = list(temp.groupobjectpermission_set.all())

			s_group = Special_Group.objects.create(name=obj.name + temp.temp_name, org=obj,
			                                       operator=request.user.username)
			for perm in all_perm:
				s_group.permissions.add(perm)
			for object_perm in all_object_perm:
				codename = object_perm.permission.codename
				content_object = object_perm.content_object
				assign_perm(codename, s_group, content_object)
			new_user.groups.add(s_group)

	elif org_agency=='agency':
		all_temp = Group_Template.objects.filter(type='agency')
		new_user = User.objects.create(username=obj.name + '总管理员', identity='agency', password=make_password('686868'))
		Agency_User.objects.create(user=new_user, agency=obj, operator=request.user.username)
		for temp in all_temp:
			all_perm = [perm for perm in temp.permissions.all()]
			all_object_perm = list(temp.groupobjectpermission_set.all())

			s_group = Special_Group.objects.create(name=obj.name + temp.temp_name, agency=obj,
			                                       operator=request.user.username)
			for perm in all_perm:
				s_group.permissions.add(perm)
			for object_perm in all_object_perm:
				codename = object_perm.permission.codename
				content_object = object_perm.content_object
				assign_perm(codename, s_group, content_object)
			new_user.groups.add(s_group)


def get_choices_text(CHOICES,value):
	'''根据value获取选项的文本内容
	单选！！！
	'''
	if isinstance(CHOICES,tuple):
		for c in CHOICES:
			if c[0]==value:
				return c[1]

def get_multi_text(obj):
	'''返回多选框的文本内容'''
	if isinstance(obj,MSFList):
		return ','.join([text for text in obj.choices.values()])