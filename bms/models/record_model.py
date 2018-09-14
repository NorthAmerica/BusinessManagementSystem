from django.db import models
from django.utils import timezone

class Change_Info(models.Model):
	'''变更记录'''
	EVENT_TYPE_CHOICES = (
		('add','增加'),
		('update','修改'),
		('del', '删除'),
		('select', '查询'),
	)
	initiator = models.CharField(max_length=100, verbose_name='发起者')
	receiver = models.CharField(max_length=100, verbose_name='接受者')
	event_type = models.CharField(choices=EVENT_TYPE_CHOICES,max_length=32,default='back',verbose_name='变更类型')
	event = models.CharField(max_length=500,verbose_name='事件')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
	class Meta:
		verbose_name = '变更记录'
		verbose_name_plural = '变更记录'