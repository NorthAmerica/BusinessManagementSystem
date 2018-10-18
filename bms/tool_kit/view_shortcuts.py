from guardian.shortcuts import assign_perm
from django.contrib.auth.hashers import make_password
from multiselectfield.db.fields import MSFList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bms.models import *
import time


def get_org_user_list(request):
	'''从登陆用户获取所属机构管理员列表'''
	if request.user is not None and request.user.identity == 'org':

		org_id = get_org_id(request)
		list_org_user = list(Org_User.objects.filter(organization_id=org_id))
		return [org_user.user for org_user in list_org_user]

	else:
		return None


def get_agency_user_list(request):
	'''从登陆用户获取所属代理管理员列表'''
	if request.user is not None and request.user.identity == 'agency':

		agency_id = get_agency_id(request)
		list_agency_user = list(Agency_User.objects.filter(agency_id=agency_id))
		return [agency_user.user for agency_user in list_agency_user]

	else:
		return None


def get_org_id(request):
	'''从登陆用户获取所属机构ID'''
	if request.user is not None and request.user.identity == 'org':
		return request.user.org_user.organization_id
	else:
		return None


def get_org_obj(request):
	'''从登陆用户获取所属机构ID'''
	if request.user is not None and request.user.identity == 'org':
		return request.user.org_user.organization
	else:
		return None


def get_org_name(request):
	'''从登陆用户获取所属机构名称'''
	if request.user is not None and request.user.identity == 'org':
		return request.user.org_user.organization.name
	else:
		return '广州金艮投资有限公司'

def get_agency_obj(request):
	if request.user is not None and request.user.identity == 'agency':
		return request.user.agency_user.agency
	else:
		return None

def get_agency_id(request):
	if request.user is not None and request.user.identity == 'agency':
		return request.user.agency_user.agency.id
	else:
		return None

def get_agency_name(request):
	'''从登陆用户获取所属机构名称'''
	if request.user is not None and request.user.identity == 'agency':
		return request.user.agency_user.agency.name
	else:
		return '广州金艮投资有限公司'


def get_org_agency_set(request):
	if request.user is not None and request.user.identity == 'org':
		return request.user.org_user.organization.agency_set
	else:
		return None


def get_all_son_agency(first, show_self=False):
	'''递归获得所有子归属'''
	try:
		child = []
		for ag in first:
			child_agency = Agency.objects.filter(f_agency=ag)
			if len(child_agency) > 0:
				child.append(
					{'id': ag.id,
					 'text': ag.name,
					 'iconCls': 'icon-man' if ag.is_freeze is False else 'icon-lock',
					 'state': 'open',
					 'children': get_all_son_agency(child_agency)
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


def auto_add_permissions(obj, request, org_agency):
	'''
	自动复制组模板
	自动分配权限
	自动创建管理员
	'''
	# 新增管理员
	try:
		if org_agency == 'org':
			all_temp = Group_Template.objects.filter(type='org')
			new_user = User.objects.create(username=obj.name + '总管理员', identity='org',
			                               password=make_password('686868'))
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

		elif org_agency == 'agency':
			all_temp = Group_Template.objects.filter(type='agency')
			new_user = User.objects.create(username=obj.name + '总管理员', identity='agency',
			                               password=make_password('686868'))
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
	except Exception as ex:
		print(ex)


def get_choices_text(CHOICES, value):
	'''根据value获取选项的文本内容
	单选！！！
	'''
	if isinstance(CHOICES, tuple):
		for c in CHOICES:
			if c[0] == value:
				return c[1]


def get_multi_text(obj):
	'''返回多选框的文本内容'''
	if isinstance(obj, MSFList):
		# for test in obj:
		# 	test
		return ','.join([obj.choices[text] for text in obj])


def send_msg_all_client(sender, title, msg):
	'''给所有客户发送消息'''
	try:
		msg_dict = {
			'title': title,
			'msg': msg,
			'for_all_client': True,
			'operator': sender
		}
		send = Message.objects.create(**msg_dict)
		if send is not None:
			return True
		else:
			return False
	except Exception as ex:
		print(ex)
		return False


def send_msg_all_org(sender, title, msg):
	'''给所有机构发送消息'''
	try:
		msg_dict = {
			'title': title,
			'msg': msg,
			'for_all_org': True,
			'operator': sender
		}
		send = Message.objects.create(**msg_dict)
		if send is not None:
			return True
		else:
			return False
	except Exception as ex:
		print(ex)
		return False


def send_msg_all_agency(sender, title, msg):
	'''给所有归属发送消息'''
	try:
		msg_dict = {
			'title': title,
			'msg': msg,
			'for_all_agency': True,
			'operator': sender
		}
		send = Message.objects.create(**msg_dict)
		if send is not None:
			return True
		else:
			return False
	except Exception as ex:
		print(ex)
		return False


def send_msg_to_client(sender, title, msg, clients_id):
	'''给一些客户发送消息'''
	try:
		msg_dict = {
			'title': title,
			'msg': msg,
			'msg_type': 'private',
			'operator': sender
		}
		Message.objects.create(**msg_dict).client.add(*Client.objects.filter(id__in=str(clients_id).split(',')))
	# Message.save()
	except Exception as ex:
		print(ex)


def send_msg_to_org(sender, title, msg, orgs_id):
	'''给一部分机构发送消息'''
	try:
		msg_dict = {
			'title': title,
			'msg': msg,
			'msg_type': 'private',
			'operator': sender
		}
		Message.objects.create(**msg_dict).org.add(*Organization.objects.filter(id__in=str(orgs_id).split(',')))
	except Exception as ex:
		print(ex)


def send_msg_to_agency(sender, title, msg, agencys_id):
	'''给一部分归属发送消息'''
	try:
		msg_dict = {
			'title': title,
			'msg': msg,
			'msg_type': 'private',
			'operator': sender
		}
		Message.objects.create(**msg_dict).agency.add(*Agency.objects.filter(id__in=str(agencys_id).split(',')))
	except Exception as ex:
		print(ex)


def get_msg_num(request):
	'''得到消息中心的消息数量'''
	try:
		all_msg_num = 0
		if request.user.identity == 'org':
			org_id = get_org_id(request)
			all_org_msg = Message.objects.filter(for_all_org=True).exclude(
				org_have_read__contains=str(org_id))
			all_msg_num += all_org_msg.count()

			all_msg_num += Message.objects.filter(org__id=org_id).exclude(
				org_have_read__contains=str(org_id)).count()
		elif request.user.identity == 'agency':
			agency_id = get_agency_id(request)
			all_agency_msg = Message.objects.filter(for_all_agency=True).exclude(
				agency_have_read__contains=str(agency_id))
			all_msg_num += all_agency_msg.count()

			all_msg_num += Message.objects.filter(agency__id=agency_id).exclude(
				agency_have_read__contains=str(agency_id)).count()
		return all_msg_num
	except Exception as ex:
		print(ex)
		return 0

def date_joined_sort(elem):
	'''按日期排序'''
	return elem.date_joined

def page_helper(list, rows, page):
	'''分页器'''
	paginator = Paginator(list, rows)
	total = paginator.count
	try:
		results = paginator.page(page)
		return results, total
	except PageNotAnInteger:
		results = paginator.page(1)
		return results, total
	except EmptyPage:
		results = paginator.page(paginator.num_pages)
		return results, total


def msg_have_read(request, msg_id):
	'''设置消息已读'''
	find_msg = Message.objects.filter(pk=msg_id)
	if find_msg.exists():
		msg_obj = find_msg.first()
		if request.user.identity == 'org':
			if msg_obj.org_have_read.split(',').count(
					str(get_org_id(request))) == 0:
				msg_obj.org_have_read += (',' + str(get_org_id(request)))
				update_dict = {
					'org_have_read': msg_obj.org_have_read
				}
				find_msg.update(**update_dict)
		elif request.user.identity == 'agency':
			if msg_obj.agency_have_read.split(',').count(
					str(get_agency_id(request))) == 0:
				msg_obj.ageny_have_read += (',' + str(get_agency_id(request)))
				update_dict = {
					'ageny_have_read': msg_obj.ageny_have_read
				}
				find_msg.update(**update_dict)

def get_week_day():
	'''获得当前日期的星期几'''
	a = time.localtime()
	return time.strftime("%A", a)

def get_local_time():
	'''获取当前时间（小时：分钟：秒）'''
	return time.strftime('%H:%M:%S', time.localtime(time.time()))


def check_in_rule(db_rule,balance_change):
	# 检查是否符合入金规则
	if [day for day in db_rule.week].count(get_week_day()) > 0:
		t1 = int(db_rule.begin_time.strftime("%H%M%S"))
		t2 = int(time.strftime('%H%M%S', time.localtime(time.time())))
		t3 = int(db_rule.end_time.strftime("%H%M%S"))
		if t1 < t2 < t3:
			if db_rule.min_gateway > balance_change or db_rule.min_shortcut > balance_change:
				return False, '抱歉，入金金额必须大于最小金额限制。'
			else:
				return True,''
		else:
			return False, '抱歉，现在时间不能进行入金操作。'
	else:
		return False, '抱歉，今天不能进行入金操作。'