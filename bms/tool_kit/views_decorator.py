from django.core.cache import cache

#获取redis缓存的装饰器
from django.http import HttpResponseRedirect


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



def Check_Login(login_page):
	def __Check_Login(func):  #自定义登录验证装饰器
		def warpper(request,*args,**kwargs):
			is_login = request.session.get('is_login', False)
			if is_login:
				return func(request,*args,**kwargs)
			else:
				return HttpResponseRedirect(login_page)
		return warpper
	return __Check_Login