from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

class Special_Group(Group):
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	org  = models.ForeignKey('Organization',blank=True, null=True, on_delete=models.SET_NULL,verbose_name='所属机构')
	agency = models.ForeignKey('Agency',blank=True, null=True, on_delete=models.SET_NULL,verbose_name='所属代理')
	class Meta:
		verbose_name = '特别组'
		verbose_name_plural = '特别组'