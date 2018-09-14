from django.contrib import admin, auth
from bms.models import *
from django.forms import ModelForm
from guardian.admin import GuardedModelAdmin
from django.contrib.auth.hashers import make_password
from guardian.shortcuts import assign_perm
from multiselectfield import MultiSelectField

admin.site.site_header = '广州金艮业务系统管理后台'
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
	)
	filter_horizontal = ('user_permissions', 'groups')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.password = make_password(form.data['password'])
		obj.save()

	readonly_fields = ('operator',)


@admin.register(Org_User)
class Org_UserAdmin(GuardedModelAdmin):
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
	date_hierarchy = 'date_joined'
	list_display = ('name', 'logo', 'cachet', 'account', 'is_freeze', 'date_joined')

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	readonly_fields = ('operator',)


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
	date_hierarchy = 'date_joined'
	list_display = (
	'name', 'get_org_name', 'is_freeze', 'rebate_x', 'rebate_y', 'rebate_z', 'get_f_name', 'invite_num', 'date_joined')
	readonly_fields = ('invite_num', 'operator',)

	def get_org_name(self, obj):
		return obj.organization.name

	get_org_name.short_description = '机构名称'

	def get_f_name(self, obj):
		if (obj.f_agency):
			return obj.f_agency.name
		else:
			return '无'

	get_f_name.short_description = '父级代理'

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Special_Group)
class Special_GroupAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = ('name', 'operator', 'date_joined',)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()

	readonly_fields = ('operator',)


admin.site.register(Client)


@admin.register(Menu)
class MenuAdmin(GuardedModelAdmin):
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
		'org', 'begin_time', 'end_time', 'week', 'max_count_each_day', 'max_money_each_day', 'max_money_each_time',
		'operator', 'date_joined')
	readonly_fields = ('operator',)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()


@admin.register(Exchange_Rule)
class Exchange_RuleAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_display = (
		'org', 'begin_time', 'end_time', 'week', 'option_type', 'type', 'operator',
		'date_joined')
	readonly_fields = ('operator',)

	def save_model(self, request, obj, form, change):
		obj.operator = request.user.username
		obj.save()
