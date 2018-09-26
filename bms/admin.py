from django.contrib import admin, auth
from bms.models import *
from django.forms import ModelForm
from guardian.admin import GuardedModelAdmin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm
from multiselectfield import MultiSelectField
from bms.ui_views.view_shortcuts import auto_add_permissions,get_multi_text

admin.site.site_header = '广州金艮-云平台管理后台'
admin.site.site_title = '管理后台'


# Register your models here.




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

	readonly_fields = ('operator',)


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
	list_display = ('name', 'logo', 'cachet', 'account','get_allow_business', 'is_freeze', 'date_joined')
	readonly_fields = ('operator',)

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
		# # 新增管理员
		# new_user = User.objects.create(username=obj.name + '总管理员',identity='org',password=make_password('686868'))
		# Org_User.objects.create(user=new_user, organization=obj, operator=request.user.username)
		# for temp in all_temp:
		# 	all_perm = [perm for perm in temp.permissions.all()]
		# 	all_object_perm = list(temp.groupobjectpermission_set.all())
		#
		# 	s_group = Special_Group.objects.create(name=obj.name+temp.temp_name,org=obj,operator=request.user.username)
		# 	for perm in all_perm:
		# 		s_group.permissions.add(perm)
		# 	for object_perm in all_object_perm:
		# 		codename = object_perm.permission.codename
		# 		content_object = object_perm.content_object
		# 		assign_perm(codename,s_group,content_object)
		# 	new_user.groups.add(s_group)

@admin.register(Org_Rule)
class Org_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('org', 'contract', 'op_type', 'rebate_x', 'rebate_y', 'operator', 'date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	readonly_fields = ('operator',)


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
	'''代理'''
	date_hierarchy = 'date_joined'
	list_display = (
	'name', 'get_org_name', 'grade','is_freeze','get_allow_business', 'rebate_x', 'rebate_y', 'rebate_z', 'get_f_name', 'invite_num', 'date_joined')
	readonly_fields = ('invite_num', 'operator',)

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
		# new_user = User.objects.create(username=obj.name + '总管理员', identity='agency',password=make_password('686868'))
		# Agency_User.objects.create(user=new_user, agency=obj, operator=request.user.username)
		# for temp in all_temp:
		# 	all_perm = [perm for perm in temp.permissions.all()]
		# 	all_object_perm = list(temp.groupobjectpermission_set.all())
		#
		# 	s_group = Special_Group.objects.create(name=obj.name + temp.temp_name, agency=obj,
		# 	                                       operator=request.user.username)
		# 	for perm in all_perm:
		# 		s_group.permissions.add(perm)
		# 	for object_perm in all_object_perm:
		# 		codename = object_perm.permission.codename
		# 		content_object = object_perm.content_object
		# 		assign_perm(codename,s_group,content_object)
		# 	new_user.groups.add(s_group)



@admin.register(Group_Template)
class Group_TemplateAdmin(admin.ModelAdmin):
	'''组模板'''
	date_hierarchy = 'date_joined'
	list_display = ('name','type', 'operator', 'date_joined',)
	filter_horizontal = ('permissions',) #生成多选框
	readonly_fields = ('operator',)
	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Special_Group)
class Special_GroupAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('name', 'operator', 'date_joined',)
	filter_horizontal = ('permissions',)  # 生成多选框
	readonly_fields = ('operator',)

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

	readonly_fields = ('operator',)


admin.site.register(Change_Info)


@admin.register(Fund_Detail)
class Fund_DetailAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'order_number', 'client', 'change_type', 'balance_before', 'balance_after',
		'balance_change', 'frozen_balance', 'date_joined')
	readonly_fields = ('order_number', 'operator',)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Fund_In_Rule)
class Fund_In_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'org', 'begin_time', 'end_time', 'week', 'min_gateway', 'min_shortcut',
		'operator', 'date_joined')
	readonly_fields = ('operator',)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Fund_Out_Rule)
class Fund_Out_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'week', 'org', 'begin_time', 'end_time', 'max_count_each_day', 'max_money_each_day', 'max_money_each_time',
		'operator', 'date_joined')
	readonly_fields = ('operator',)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Exchange_Rule)
class Exchange_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'week','org', 'begin_time', 'end_time', 'option_type', 'type', 'operator',
		'date_joined')
	readonly_fields = ('operator',)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

@admin.register(Notional_Principal)
class Notional_PrincipalAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'number', 'org', 'option_type', 'operator', 'date_joined')
	readonly_fields = ('operator',)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'mobile_phone', 'identity_card', 'organization','agency','status','is_freeze','get_allow_business','date_joined')
	readonly_fields = ('operator',)
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