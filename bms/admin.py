from decimal import Decimal

from django.contrib import admin,messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from bms.models import *
from guardian.admin import GuardedModelAdmin
from django.contrib.auth.hashers import make_password
from bms.tool_kit.admin_shortcuts import import_options_rate
from bms.tool_kit.view_shortcuts import auto_add_permissions,get_multi_text
from bms.tool_kit.fund_shortcuts import change_client_account_balance,change_org_account_balance,change_agency_account_balance,unfrozen_client_balance,frozen_client_balance

admin.site.site_header = '广州金艮-云平台管理后台'
admin.site.site_title = '管理后台'

@admin.register(User)
class User_Admin(GuardedModelAdmin):
	# add_form = UserCreationForm
	date_hierarchy = 'date_joined'
	list_display = (
	'username', 'get_full_name', 'mobile_phone', 'email', 'is_staff', 'is_active', 'identity', 'position',
	'date_joined')
	fieldsets = (
		("基本信息", {'fields': ['username', 'first_name', 'last_name', 'password', 'mobile_phone', 'email', 'position']}),
		("权限控制", {'fields': ['identity', 'user_permissions', 'groups', 'is_staff', 'is_active']})
	) # 分组排列
	filter_horizontal = ('user_permissions', 'groups') #生成多选框

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		str1 = str(form.data['password'])[:13]
		if str(form.data['password'])[:13]!='pbkdf2_sha256':
			obj.password = make_password(form.data['password'])
		obj.save()

	readonly_fields = ('operator','date_joined')


@admin.register(Org_User)
class Org_User_Admin(GuardedModelAdmin):
	'''机构用户'''
	list_display = ('user', 'organization', 'operator')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	readonly_fields = ('operator',)

	# 过滤出所有是机构管理员的用户
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'user':
			kwargs['queryset'] = User.objects.filter(identity='org')
		return super(Org_User_Admin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Agency_User)
class Agency_User_Admin(GuardedModelAdmin):
	'''代理用户'''
	list_display = ('user', 'agency')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


	readonly_fields = ('operator',)

	# 过滤出所有是代理管理员的用户
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'user':
			kwargs['queryset'] = User.objects.filter(identity='agency')
		return super(Agency_User_Admin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Organization)
class Organization_Admin(admin.ModelAdmin):
	'''机构'''
	date_hierarchy = 'date_joined'
	list_display = ('name', 'logo', 'cachet', 'account','account_balance','get_allow_business', 'is_freeze', 'date_joined')
	readonly_fields = ('operator','date_joined')

	def get_allow_business(self, obj):
		if  obj.allow_business:
			return get_multi_text(obj.allow_business)
			# return ",".join([obj.allow_business.choices.__getitem__(l) for l in obj.allow_business])
		else:
			return '无'

	get_allow_business.short_description = '允许的业务类型'
	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()
		# 复制组模板
		auto_add_permissions(obj,request,'org')


@admin.register(Org_Rule)
class Org_Rule_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('org', 'contract', 'op_type', 'rebate_x', 'rebate_y', 'operator', 'date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	readonly_fields = ('operator','date_joined')


@admin.register(Agency)
class Agency_Admin(admin.ModelAdmin):
	'''代理'''
	date_hierarchy = 'date_joined'
	list_display = (
	'name', 'get_org_name', 'grade','is_freeze','account_balance','get_allow_business', 'rebate_x', 'rebate_y', 'rebate_z', 'get_f_name', 'invite_num', 'date_joined')
	readonly_fields = ('invite_num', 'operator','date_joined')

	def get_allow_business(self, obj):
		if  obj.allow_business:
			# return obj.allow_business.choices.values()
			return get_multi_text(obj.allow_business)
			# return ",".join([obj.allow_business.choices.__getitem__(l) for l in obj.allow_business])
		else:
			return '无'

	get_allow_business.short_description = '允许的业务类型'

	def get_org_name(self, obj):
		return obj.organization.name

	get_org_name.short_description = '机构名称'

	def get_f_name(self, obj):
		if (obj.f_agency):
			return obj.f_agency.name
		else:
			return '无'

	get_f_name.short_description = '父级归属'

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		if obj.f_agency is None:
			obj.grade = 1
		else:
			obj.grade = obj.f_agency.grade+1
		obj.save()
		# 复制组模板
		auto_add_permissions(obj, request, 'agency')




@admin.register(Group_Template)
class Group_Template_Admin(admin.ModelAdmin):
	'''组模板'''
	date_hierarchy = 'date_joined'
	list_display = ('name','type', 'operator', 'date_joined',)
	filter_horizontal = ('permissions',) #生成多选框
	readonly_fields = ('operator','date_joined')
	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Special_Group)
class Special_Group_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('name', 'operator', 'date_joined',)
	filter_horizontal = ('permissions',)  # 生成多选框
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Menu)
class Menu_Admin(GuardedModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('menu_name', 'menu_url', 'order_num', 'f_menu', 'date_joined','operator')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	readonly_fields = ('operator','date_joined')


admin.site.register(Change_Info)

# ------------------资金状态判断--状态模式-----------------------------------------

class fund_state(object):
	def __init__(self):
		pass

class fund_state_work(object):
	def __init__(self):
		self.obj = None
		self.curr = in_out_state()

	def set_state(self, s):
		self.curr = s

	def change(self):
		return self.curr.change(self)
	def add(self):
		return self.curr.add(self)

class in_out_state(fund_state):
	def change(self, w):
		if w.obj is not None:
			if w.obj.fund_state == 'out' or w.obj.fund_state == 'in':
				return Fund_Detail_Admin.agree_change_account_balance(self,w.obj)
			else:
				w.set_state(freeze_state())
				w.write_program()
		else:
			return False, 'obj对象为空'
	def add(self, w):
		if w.obj is not None:
			if w.obj.org is not None:
				result,msg = Fund_Detail_Admin.change_fund_detail(w.obj.fund_state, w.obj, w.obj.org)
				if not result:
					return result,msg
			elif obj.agency is not None:
				result, msg = Fund_Detail_Admin.change_fund_detail(w.obj.fund_state, w.obj, w.obj.agency)
				if not result:
					return result,msg
			elif obj.client is not None:
				result, msg = Fund_Detail_Admin.change_fund_detail(w.obj.fund_state, w.obj, w.obj.client)
				if not result:
					return result,msg
			return Fund_Detail_Admin.agree_change_account_balance(obj)
		else:
			return False,'obj对象为空'

class freeze_state(fund_state):
	def change(self, w):
		if w.obj is not None:
			if w.obj.fund_state == 'freeze':
				if w.obj.client is not None:
					Fund_Detail_Admin.agree_client_frozen_balance(w.obj)
					return True,''
				else:
					return False,'只能客户进行冻结解冻资金'
			else:
				w.set_state(unfreeze_state())
				w.write_program()
		else:
			return False,'obj对象为空'
	def add(self, w):
		if w.obj is not None:
			if w.obj.client is not None:
				if Fund_Detail_Admin.over_limit(w.obj.client.account_balance, w.obj.balance_change):
					# messages.error(request, '冻结金额不能大于账户余额！')
					return False,'冻结金额不能大于账户余额！'
				w.obj.balance_before = w.obj.client.account_balance
				w.obj.balance_after = w.obj.client.account_balance - w.obj.balance_change
				result = Fund_Detail_Admin.agree_client_frozen_balance(w.obj)
				if result:
					return True,''
				else:
					return False, '冻结客户资金失败！'
			else:
				# messages.error(request, '只能对客户资金进行冻结！')
				return False,'只能对客户资金进行冻结！'
		else:
			return False,'obj对象为空'

class unfreeze_state(fund_state):
	def change(self, w):
		if w.obj is not None:
			if w.obj.fund_state == 'unfreeze':
				Fund_Detail_Admin.agree_client_unfrozen_balance(w.obj)
				return True,''
		else:
			return False, 'obj对象为空'

	def add(self, w):
		if w.obj is not None:
			if w.obj.client is not None:
				if Fund_Detail_Admin.over_limit(w.obj.client.frozen_balance, w.obj.balance_change):
					# messages.error(request, '解冻金额不能大于冻结余额！')
					return False,'解冻金额不能大于冻结余额！'
				w.obj.balance_before = w.obj.client.account_balance
				w.obj.balance_after = w.obj.client.account_balance + w.obj.balance_change
				result = Fund_Detail_Admin.agree_client_unfrozen_balance(w.obj)
				if result:
					return True,''
				else:
					return False,'解冻客户资金失败！'
			else:
				# messages.error(request, '只能对客户资金进行解冻！')
				return False, '只能对客户资金进行解冻！'
		else:
			return False, 'obj对象为空'

# ------------------资金状态判断--状态模式-----------------------------------------

@admin.register(Fund_Detail)
class Fund_Detail_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'serial_number', 'org','agency','client','fund_type', 'fund_state', 'balance_before', 'balance_after',
		'balance_change', 'fund_audit', 'date_joined')
	fieldsets = (
		("资金申请对象(三个中只能选择其中一种)", {'fields': ['org', 'agency', 'client']}),
		("资金情况", {'fields': ['fund_type', 'fund_state', 'balance_before', 'balance_after', 'balance_change']}),
		("审核状态", {'fields': ['fund_audit']}),
		("其他信息", {'fields': ['serial_number','audit_time','auditor','operator','date_joined']})
	)
	readonly_fields = ('balance_before', 'balance_after','audit_time','auditor','serial_number', 'operator','date_joined')

	def response_add(self, request, obj, post_url_continue=None):
		"""
		@des:这里可以自定义 创建对象后的 出错信息-----修改对象用response_change, 删除对象用resonse_delete
		"""
		# 如果有出错消息
		if messages.get_messages(request):
			return HttpResponseRedirect(".")
		# end--如果没有出错消息
		return super(Fund_Detail_Admin, self).response_add(request, obj, post_url_continue)

	def response_change(self, request, obj):
		"""
		@des:这里可以自定义 创建对象后的 出错信息-----修改对象用response_change, 删除对象用resonse_delete
		"""
		# 如果有出错消息
		if messages.get_messages(request):
			return HttpResponseRedirect(".")
		# end--如果没有出错消息
		return super(Fund_Detail_Admin, self).response_change(request, obj)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		# messages.error(request, u'角色不存在')
		# return
		if form.changed_data.count('fund_state') > 0 and (obj.fund_state == 'profit' or obj.fund_state == 'loss'):
			messages.error(request, '资金类型不能选择盈利或亏损')
			return

		if change:
			# 如果是修改状态
			if form.changed_data.count('fund_audit')>0 and form.initial['fund_audit']=='agree':
				# 已经审核通过的不能再次修改状态
				messages.error(request, '不能再次修改已经审核通过的资金状态！')
				return
			if form.changed_data.count('fund_state')>0 or form.changed_data.count('fund_type')>0:
				# 不能修改资金渠道及资金类型
				messages.error(request, '资金渠道及资金类型不能进行修改！')
				return
			if form.changed_data.count('fund_audit')>0 and obj.fund_audit=='agree':

				work = fund_state_work()
				work.obj = obj
				result,msg = work.change()
				if not result:
					messages.error(request, msg)
					return
				# if obj.fund_state == 'out' or obj.fund_state == 'in':
				# 	result,msg = self.agree_change_account_balance(obj)
				# 	if not result:
				# 		messages.error(request, msg)
				# 		return
				# elif obj.fund_state == 'freeze':
				# 	if obj.client is not None:
				# 		self.agree_client_frozen_balance(obj)
				# 	else:
				# 		messages.error(request, '只能客户进行冻结解冻资金！')
				# 		return
				# elif obj.fund_state == 'unfreeze':
				# 	self.agree_client_unfrozen_balance(obj)
		else:
			# 如果是新增
			work = fund_state_work()
			work.obj = obj
			result, msg = work.add()
			if not result:
				messages.error(request, msg)
				return
			# if obj.fund_state == 'out' or obj.fund_state == 'in':
			# 	# 出金操作
			#
			# 	if obj.org is not None:
			# 		self.change_fund_detail(obj.fund_state,request,obj,obj.org)
			# 	elif obj.agency is not None:
			# 		self.change_fund_detail(obj.fund_state,request, obj, obj.agency)
			# 	elif obj.client is not None:
			# 		self.change_fund_detail(obj.fund_state,request, obj, obj.client)
			# 	result, msg = self.agree_change_account_balance(obj)
			# 	if not result:
			# 		messages.error(request, msg)
			# 		return
			#
			# elif obj.fund_state == 'freeze':
			# 	# 冻结资金
			# 	if obj.client is not None:
			# 		if self.over_limit(obj.client.account_balance, obj.balance_change):
			# 			messages.error(request, '冻结金额不能大于账户余额！')
			# 			return
			# 		obj.balance_before = obj.client.account_balance
			# 		obj.balance_after = obj.client.account_balance - obj.balance_change
			# 		self.agree_client_frozen_balance(obj)
			# 	else:
			# 		messages.error(request, '只能对客户资金进行冻结！')
			# 		return
			# elif obj.fund_state == 'unfreeze':
			# 	# 解冻资金
			# 	if obj.client is not None:
			# 		if self.over_limit(obj.client.frozen_balance, obj.balance_change):
			# 			messages.error(request, '解冻金额不能大于冻结余额！')
			# 			return
			# 		obj.balance_before = obj.client.account_balance
			# 		obj.balance_after = obj.client.account_balance + obj.balance_change
			# 		self.agree_client_unfrozen_balance(obj)
			# 	else:
			# 		messages.error(request, '只能对客户资金进行解冻！')
			# 		return

		obj.save()

	def change_fund_detail(self,in_or_out,obj,who):
		# 变更资金明细
		if in_or_out=='out':
			if self.over_limit(who.account_balance, obj.balance_change):
				# messages.error(request, '出金金额不能大于账户余额！')
				return False,'出金金额不能大于账户余额！'
			obj.balance_before = who.account_balance
			obj.balance_after = who.account_balance - obj.balance_change
			return True,''
		elif in_or_out=='in':
			obj.balance_before = who.account_balance
			obj.balance_after = who.account_balance + obj.balance_change
			return True,''

	def over_limit(self,min,max):
		# 是否超过现有账户金额
		if Decimal(min) < Decimal(max):
			return True
		else:
			return False

	def agree_client_frozen_balance(self,obj):
		if obj.fund_audit == 'agree':
			return frozen_client_balance(obj.client_id,obj.balance_change)
	def agree_client_unfrozen_balance(self,obj):
		if obj.fund_audit == 'agree':
			return unfrozen_client_balance(obj.client_id,obj.balance_change)

	def agree_change_account_balance(self,obj):
		# 审核通过资金变更申请
		if obj.fund_audit == 'agree':
			if obj.org is not None:
				return change_org_account_balance(obj.org_id, obj.balance_change,obj.fund_state)
			elif obj.agency is not None:
				return change_agency_account_balance(obj.agency_id, obj.balance_change,obj.fund_state)
			elif obj.client is not None:
				return change_client_account_balance(obj.client_id, obj.balance_change,obj.fund_state)


@admin.register(Fund_In_Rule)
class Fund_In_Rule_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'org', 'begin_time', 'end_time', 'week', 'min_gateway', 'min_shortcut',
		'operator', 'date_joined')
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Fund_Out_Rule)
class Fund_Out_Rule_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'week', 'org', 'begin_time', 'end_time', 'max_count_each_day', 'max_money_each_day', 'max_money_each_time',
		'operator', 'date_joined')
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Exchange_Rule)
class Exchange_Rule_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'week','org', 'begin_time', 'end_time', 'option_type', 'type', 'operator',
		'date_joined')
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

@admin.register(Notional_Principal)
class Notional_Principal_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'number', 'org', 'option_type', 'operator', 'date_joined')
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

@admin.register(Client)
class Client_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'mobile_phone', 'identity_card', 'organization','agency','status','is_freeze','account_balance','get_allow_business','date_joined')
	readonly_fields = ('operator','date_joined')
	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	def get_allow_business(self, obj):
		if  obj.allow_business:
			return get_multi_text(obj.allow_business)
			# return ",".join([obj.allow_business.choices.__getitem__(l) for l in obj.allow_business])
		else:
			return '无'

	get_allow_business.short_description = '允许的业务类型'


@admin.register(Order_Detail)
class Order_Detail_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'serial_number', 'client', 'org', 'agency', 'option_type',
		'call_put', 'option_pattern','option_code','option_rate',
		'order_number','order_price','exercise_day','notional_principal'
		,'date_joined')
	readonly_fields = ('serial_number','operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

@admin.register(Message)
class Message_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'title','colored_msg_type','for_all_client',
		'for_all_org','for_all_agency',
		'date_joined','operator'
	)
	fieldsets = (
		("消息内容", {'fields': ['title','msg', 'msg_type']}),
		("发送个别人员", {'fields': ['client', 'org', 'agency']}),
		("发送全体人员", {'fields': ['for_all_client', 'for_all_org', 'for_all_agency']})
	)  # 分组排列

	filter_horizontal = ('client','org','agency')  # 生成多选框
	readonly_fields = ('client_have_read','org_have_read','agency_have_read','operator','date_joined')

	def colored_msg_type(self,obj):
		if  obj.msg_type=='public':
			return format_html('<span style="color:green">{}</span>',obj.get_msg_type_display())
		elif obj.msg_type=='private':
			return format_html('<span style="color:red">{}</span>',obj.get_msg_type_display())
	colored_msg_type.short_description = '消息类型'

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Options_File)
class Options_File_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_filter = ('op_type', 'effective_date')
	search_fields = ['file', ]
	list_display = ('date_joined','file','op_type','effective_date','operator')

	def response_add(self, request, obj, post_url_continue=None):
		"""
		@des:这里可以自定义 创建对象后的 出错信息-----修改对象用response_change, 删除对象用resonse_delete
		"""
		# 如果有出错消息
		if messages.get_messages(request):
			return HttpResponseRedirect(".")
		# end--如果没有出错消息
		return super(Options_File_Admin, self).response_add(request, obj, post_url_continue)

	def response_change(self, request, obj):
		"""
		@des:这里可以自定义 创建对象后的 出错信息-----修改对象用response_change, 删除对象用resonse_delete
		"""
		# 如果有出错消息
		if messages.get_messages(request):
			return HttpResponseRedirect(".")
		# end--如果没有出错消息
		return super(Options_File_Admin, self).response_change(request, obj)

	def save_model(self, request, obj, form, change):
		find_options_file = Options_File.objects.filter(effective_date=obj.effective_date).filter(op_type=obj.op_type)
		if find_options_file.exists():
			messages.error(request, '已经上传过今天的%s'%obj.get_op_type_display()+'数据，如需更新请把今天的数据先删除！')
			return
		else:
			obj.operator = request.user.username
			obj.save()
			result,msg = import_options_rate(self, request, obj, change)
			if not result:
				messages.error(request, msg)
				return



@admin.register(Option_Rate)
class Option_Rate_Admin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('code','name','colored_op_type','colored_call_put','notional_principal','effective_date','date_joined','operator')
	list_filter = ('op_type', 'call_put', 'effective_date')
	search_fields = ['code', 'name',]
	readonly_fields = ('operator','date_joined','options_file')

	def colored_op_type(self,obj):
		if  obj.op_type=='commodity':
			return format_html('<span style="color:green">{}</span>',obj.get_op_type_display())
		elif obj.op_type=='stock':
			return format_html('<span style="color:red">{}</span>',obj.get_op_type_display())
	colored_op_type.short_description = '期权类型'

	def colored_call_put(self,obj):
		if  obj.call_put=='call':
			return format_html('<span style="color:green">{}</span>',obj.get_call_put_display())
		elif obj.call_put=='put':
			return format_html('<span style="color:red">{}</span>',obj.get_call_put_display())
	colored_call_put.short_description = '期权方向'