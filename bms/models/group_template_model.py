from django.db import models
from django.utils import timezone
from .choices_for_model import TEMPLATE_TYPE_CHOICES
from django.contrib.auth.models import Group

class Group_Template(Group):
	'''组模板'''

	temp_name = models.CharField(blank=False, max_length=100, help_text='这个名称将作为正式名称的后缀,例如：定义为客服部 正式名称为广州金艮-客服部', verbose_name='模板名称')
	type = models.CharField(choices=TEMPLATE_TYPE_CHOICES,max_length=50,blank=False,verbose_name='模板类型')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='注册时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')

	def __str__(self):
		return self.temp_name

	class Meta:
		verbose_name = '组模板'
		verbose_name_plural = '组模板'