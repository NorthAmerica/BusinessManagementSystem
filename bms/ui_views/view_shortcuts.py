from ..models.user_model import  Org_User,Agency_User
from ..models.agency_model import Agency

def get_org_user_list(request):
	'''从登陆用户获取所属机构管理员列表'''
	if request.user is not None and request.user.identity == 'org':
		all_org_user = []
		org_id = get_org_id(request)
		list_org_user = list(Org_User.objects.filter(organization_id=org_id))
		return [org_user.user for org_user in list_org_user]
		# for org_user in list_org_user:
		# 	all_org_user.append(org_user.user)
		# return all_org_user
	else:
		return None

def get_agency_user_list(request):
	'''从登陆用户获取所属代理管理员列表'''
	if request.user is not None and request.user.identity == 'agency':
		all_agency_user = []
		agency_id = get_agency_id(request)
		list_agency_user = list(Agency_User.objects.filter(agency_id=agency_id))
		return [agency_user.user for agency_user in list_agency_user]
		# for agency_user in list_agency_user:
		# 	all_agency_user.append(agency_user.user)
		# return all_agency_user
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


def get_all_son_agency(first):
	'''递归获得所有子归属'''
	try:
		child = []
		for ag in first:
			child_agency = Agency.objects.filter(f_agency=ag)
			if len(child_agency)>0:
				child.append(
					{'id': ag.id,
					 'text': ag.name,
					 'iconCls':'icon-man',
					 'state': 'open',
					 'children':get_all_son_agency(child_agency)
					 })
			else:
				child.append(
					{'id': ag.id,
					 'text': ag.name,
					 'iconCls': 'icon-man',
					 'state': 'open'
					 })
		return child
	except Exception as ex:
		print(ex)