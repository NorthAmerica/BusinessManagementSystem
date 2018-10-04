from django.db import models
from django.utils import timezone
from .choices_for_model import MSG_TYPE_CHOICE


class Message(models.Model):
	'''系统消息'''
	title = models.CharField(max_length=100, verbose_name='标题')
	msg = models.TextField(verbose_name='消息文本')
	msg_type = models.CharField(choices=MSG_TYPE_CHOICE,max_length=32, null=True,default='public',verbose_name='消息类型')
	client = models.ManyToManyField('Client', blank=True, verbose_name='特定客户')
	org = models.ManyToManyField('Organization', blank=True, verbose_name='特定机构')
	agency = models.ManyToManyField('Agency', blank=True,verbose_name='特定归属')

	for_all_client = models.BooleanField(default=False,verbose_name='是否发送至所有客户')
	for_all_org = models.BooleanField(default=False,verbose_name='是否发送至所有机构')
	for_all_agency = models.BooleanField(default=False,verbose_name='是否发送至所有归属')

	client_have_read = models.TextField(blank=True,verbose_name='客户已读列表')
	org_have_read = models.TextField(blank=True,verbose_name='机构已读列表')
	agency_have_read = models.TextField(blank=True,verbose_name='归属已读列表')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = '系统消息'
		verbose_name_plural = '系统消息'