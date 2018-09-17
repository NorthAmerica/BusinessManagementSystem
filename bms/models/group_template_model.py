from django.db import models
from django.utils import timezone

class Group_Template(models.Model):
	'''组模板'''
	TYPE_CHOICE=(
		('org', '机构模板'),
		('agency', '代理模板'),
	)
	name = models.CharField(blank=False, max_length=100, help_text='这个名称将作为正式名称的后缀', verbose_name='模板名称')
	type = models.CharField(choices=TYPE_CHOICE,max_length=50,blank=False,verbose_name='模板类型')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='注册时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '组模板'
		verbose_name_plural = '组模板'