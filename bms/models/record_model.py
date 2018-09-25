from django.db import models
from django.utils import timezone
from .choices_for_model import EVENT_TYPE_CHOICES

class Change_Info(models.Model):
	'''变更记录'''

	initiator = models.CharField(max_length=100, verbose_name='发起者')
	receiver = models.CharField(max_length=100, verbose_name='接受者')
	event_type = models.CharField(choices=EVENT_TYPE_CHOICES,max_length=32,default='back',verbose_name='变更类型')
	event = models.TextField(verbose_name='具体事件内容')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
	class Meta:
		verbose_name = '日志记录'
		verbose_name_plural = '日志记录'