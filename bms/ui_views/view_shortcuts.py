from ..models.user_model import  Org_User,Agency_User

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

def get_org_name(request):
	'''从登陆用户获取所属机构名称'''
	if  request.user is not None and request.user.identity == 'org':
		return request.user.org_user.organization.name
	else:
		return '广州金艮投资有限公司'

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