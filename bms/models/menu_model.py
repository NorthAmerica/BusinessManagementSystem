from django.db import models
from django.utils import timezone

class Menu(models.Model):
	"""菜单"""
	menu_name = models.CharField(max_length=100,verbose_name='菜单名')
	menu_url = models.CharField(max_length=500,verbose_name='菜单链接')
	order_num = models.IntegerField(verbose_name='排序')
	f_menu = models.ForeignKey('Menu',blank=True,null=True,on_delete=models.CASCADE, verbose_name='父菜单')
	date_joined = models.DateTimeField(default=timezone.now,verbose_name='操作时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	def __str__(self):
		return self.menu_name

	def get_child(self):
		return Menu.objects.filter(f_menu=self.id).order_by('order_num')

	class Meta:
		permissions = (
			('audit_menu', '测试一下'),
			('org_menu','再增加一个权限'),
		)
		verbose_name = '菜单管理'
		verbose_name_plural = '菜单管理'

class MenuModel:
	def __init__(self):
		self.name = ''
		self.child = []
	def setUrl(self, url):
		self.url = url
	def getUrl(self):
		return self.url
	def setName(self, name):
		self.name = name
	def getName(self):
		return self.name