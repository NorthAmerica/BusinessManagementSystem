from decimal import Decimal

from django.contrib import admin,messages
from django.http import HttpResponseRedirect

from bms.models import *
from guardian.admin import GuardedModelAdmin
from django.contrib.auth.hashers import make_password
from bms.tool_kit.view_shortcuts import auto_add_permissions,get_multi_text
from bms.tool_kit.fund_shortcuts import change_client_account_balance,change_org_account_balance,change_agency_account_balance,unfrozen_client_balance,frozen_client_balance

admin.site.site_header = '广州金艮-云平台管理后台'
admin.site.site_title = '管理后台'

@admin.register(User)
class UserAdmin(GuardedModelAdmin):
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
class Org_UserAdmin(GuardedModelAdmin):
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
		return super(Org_UserAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Agency_User)
class Agency_UserAdmin(GuardedModelAdmin):
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
		return super(Agency_UserAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
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
class Org_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('org', 'contract', 'op_type', 'rebate_x', 'rebate_y', 'operator', 'date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	readonly_fields = ('operator','date_joined')


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
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
class Group_TemplateAdmin(admin.ModelAdmin):
	'''组模板'''
	date_hierarchy = 'date_joined'
	list_display = ('name','type', 'operator', 'date_joined',)
	filter_horizontal = ('permissions',) #生成多选框
	readonly_fields = ('operator','date_joined')
	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Special_Group)
class Special_GroupAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('name', 'operator', 'date_joined',)
	filter_horizontal = ('permissions',)  # 生成多选框
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Menu)
class MenuAdmin(GuardedModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('menu_name', 'menu_url', 'order_num', 'f_menu', 'date_joined','operator')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	readonly_fields = ('operator','date_joined')


admin.site.register(Change_Info)


@admin.register(Fund_Detail)
class Fund_DetailAdmin(admin.ModelAdmin):
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
		return super(Fund_DetailAdmin, self).response_add(request, obj, post_url_continue)

	def response_change(self, request, obj):
		"""
		@des:这里可以自定义 创建对象后的 出错信息-----修改对象用response_change, 删除对象用resonse_delete
		"""
		# 如果有出错消息
		if messages.get_messages(request):
			return HttpResponseRedirect(".")
		# end--如果没有出错消息
		return super(Fund_DetailAdmin, self).response_change(request, obj)

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
				if obj.fund_state == 'out' or obj.fund_state == 'in':
					self.agree_change_account_balance(obj)
				elif obj.fund_state == 'freeze':
					if obj.client is not None:
						self.agree_client_frozen_balance(obj)
					else:
						messages.error(request, '只能客户进行冻结解冻资金！')
						return
				elif obj.fund_state == 'unfreeze':
					self.agree_client_unfrozen_balance(obj)

		else:
			# 如果是新增
			# if obj.fund_state == 'in':
			# 	# 入金操作
			# 	if obj.org is not None:
			# 		obj.balance_before = obj.org.account_balance
			# 		obj.balance_after = obj.org.account_balance + obj.balance_change
			# 	elif obj.agency is not None:
			# 		obj.balance_before = obj.agency.account_balance
			# 		obj.balance_after = obj.agency.account_balance + obj.balance_change
			# 	elif obj.client is not None:
			# 		obj.balance_before = obj.client.account_balance
			# 		obj.balance_after = obj.client.account_balance + obj.balance_change
			# 	self.agree_change_account_balance(obj)
			if obj.fund_state == 'out' or obj.fund_state == 'in':
				# 出金操作
				if obj.org is not None:
					self.change_fund_detail(obj.fund_state,request,obj,obj.org)
				elif obj.agency is not None:
					self.change_fund_detail(obj.fund_state,request, obj, obj.agency)
				elif obj.client is not None:
					self.change_fund_detail(obj.fund_state,request, obj, obj.client)
				self.agree_change_account_balance(obj)
			elif obj.fund_state == 'freeze':
				# 冻结资金
				if obj.client is not None:
					if self.over_limit(obj.client.account_balance, obj.balance_change):
						messages.error(request, '冻结金额不能大于账户余额！')
						return
					obj.balance_before = obj.client.account_balance
					obj.balance_after = obj.client.account_balance - obj.balance_change
					self.agree_client_frozen_balance(obj)
				else:
					messages.error(request, '只能对客户资金进行冻结！')
					return
			elif obj.fund_state == 'unfreeze':
				# 解冻资金
				if obj.client is not None:
					if self.over_limit(obj.client.frozen_balance, obj.balance_change):
						messages.error(request, '解冻金额不能大于冻结余额！')
						return
					obj.balance_before = obj.client.account_balance
					obj.balance_after = obj.client.account_balance + obj.balance_change
					self.agree_client_unfrozen_balance(obj)
				else:
					messages.error(request, '只能对客户资金进行解冻！')
					return
			else:
				messages.error(request, '资金类型不能修改为盈利或亏损！')
				return
		obj.save()

	def change_fund_detail(self,in_or_out,request,obj,who):
		if in_or_out=='out':
			if self.over_limit(who.account_balance, obj.balance_change):
				messages.error(request, '出金金额不能大于账户余额！')
				return
			obj.balance_before = who.account_balance
			obj.balance_after = who.account_balance - obj.balance_change
		elif in_or_out=='in':
			obj.balance_before = who.account_balance
			obj.balance_after = who.account_balance + obj.balance_change

	def over_limit(self,min,max):
		# 是否超过现有账户金额
		if Decimal(min) < Decimal(max):
			return True
		else:
			return False

	def agree_client_frozen_balance(self,obj):
		if obj.fund_audit == 'agree':
			frozen_client_balance(obj.client_id,obj.balance_change)
	def agree_client_unfrozen_balance(self,obj):
		if obj.fund_audit == 'agree':
			unfrozen_client_balance(obj.client_id,obj.balance_change)

	def agree_change_account_balance(self,obj):
		# 审核通过资金变更申请
		if obj.fund_audit == 'agree':
			if obj.org is not None:
				change_org_account_balance(obj.org_id, obj.balance_after)
			elif obj.agency is not None:
				change_agency_account_balance(obj.agency_id, obj.balance_after)
			elif obj.client is not None:
				change_client_account_balance(obj.client_id, obj.balance_after)


@admin.register(Fund_In_Rule)
class Fund_In_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'org', 'begin_time', 'end_time', 'week', 'min_gateway', 'min_shortcut',
		'operator', 'date_joined')
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Fund_Out_Rule)
class Fund_Out_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'week', 'org', 'begin_time', 'end_time', 'max_count_each_day', 'max_money_each_day', 'max_money_each_time',
		'operator', 'date_joined')
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Exchange_Rule)
class Exchange_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'week','org', 'begin_time', 'end_time', 'option_type', 'type', 'operator',
		'date_joined')
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

@admin.register(Notional_Principal)
class Notional_PrincipalAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'number', 'org', 'option_type', 'operator', 'date_joined')
	readonly_fields = ('operator','date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
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
class Order_DetailAdmin(admin.ModelAdmin):
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
class MessageAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'title','msg_type','for_all_client',
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
	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()