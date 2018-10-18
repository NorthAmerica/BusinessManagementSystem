from decimal import Decimal

from django.core.cache import cache
#获取redis缓存的装饰器
from django.http import HttpResponseRedirect, JsonResponse
from bms.models import *
from bms.tool_kit.view_shortcuts import get_org_id,get_agency_obj,check_in_rule
import time



def redis_cache(key, timeout):
	def __redis_cache(func):
		def warpper(*args, **kw):
			#判断缓存是否存在
			print('check key: %s' % key)
			if cache.has_key(key):
				print('get cache')
				data = cache.get(key)
			else:
				#若不存在则执行获取数据的方法
				#注意返回数据的类型(字符串，数字，字典，列表均可)
				print('get data')
				data = func(*args, **kw)
				print('set cache')
				cache.set(key, data, timeout)
			return data
		return warpper
	return __redis_cache


#自定义登录验证装饰器(客户端使用)
def Check_Login(login_page):
	def __Check_Login(func):
		def warpper(request,*args,**kwargs):
			is_login = request.session.get('is_login', False)
			if is_login:
				return func(request,*args,**kwargs)
			else:
				return HttpResponseRedirect(login_page)
		return warpper
	return __Check_Login


# 出入金规则验证装饰器
def check_fund_rule(in_or_out=None):
	def __check_fund_rule(func):
		def warpper(request,*args,**kwargs):
			global find_org_rule
			if (in_or_out is not None and in_or_out=='in') or \
					(request.POST.get('type', None) is not None and request.POST.get('type', None)=='in'):
				# 入金
				balance_change = Decimal(request.POST.get('balance_change', None)) \
					if request.POST.get('balance_change',None) is not None else 0
				if request.user.identity == 'org':
					find_org_rule = Fund_In_Rule.objects.filter(org__id=get_org_id(request))
				elif request.user.identity == 'agency':
					find_org_rule = Fund_In_Rule.objects.filter(org__id=get_agency_obj(request).organization_id)

				if find_org_rule.exists():
					# 如果有机构规则，就按机构规则检查
					org_rule = find_org_rule.first()
					result,msg = check_in_rule(org_rule,balance_change)
					if result:
						return func(request, *args, **kwargs)
					else:
						return JsonResponse({'success': False, 'msg': msg}, safe=False)
				else:
					# 没有机构规则就查询全局规则检查
					find_in_rule = Fund_In_Rule.objects.filter(org=None)
					if find_in_rule.exists():
						# 如果有全局规则，就按全局规则
						in_rule = find_in_rule.first()
						result, msg = check_in_rule(in_rule, balance_change)
						if result:
							return func(request, *args, **kwargs)
						else:
							return JsonResponse({'success': False, 'msg': msg}, safe=False)
					else:
						# 如果什么规则都没有，直接执行方法
						return func(request,*args,**kwargs)
			elif (in_or_out is not None and in_or_out=='out') or \
					(request.POST.get('type', None) is not None and request.POST.get('type', None)=='out'):
				# 出金
				pass
		return warpper
	return __check_fund_rule