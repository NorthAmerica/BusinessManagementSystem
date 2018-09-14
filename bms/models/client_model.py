from django.db import models
from django.utils import timezone

class Client(models.Model):
	"""客户"""
	WEB_APP_CHOICES = (
		('web', '网页申请'),
		('app', '手机申请'),
		('back','后台录入')
	)
	STATUS_CHOICES=(
		('1','已开户待提审'),
		('2','已提审待审核'),
		('3','已审核待入金'),
		('4','已入金待交易'),
		('5','已交易')
	)
	name = models.CharField(max_length=100, verbose_name='用户名')
	mobile_phone = models.CharField(max_length=100, verbose_name='手机号码')
	mailbox = models.EmailField(verbose_name='邮箱地址')
	password = models.CharField(max_length=128, verbose_name='密码')
	identity_card = models.CharField(blank=True, null=True,max_length=128,verbose_name='身份证')
	bank_card = models.CharField(blank=True, null=True,max_length=128,verbose_name='银行卡号')
	bank_name = models.CharField(blank=True,null=True,max_length=128,verbose_name='开户银行')
	open_province = models.CharField(blank=True,null=True,max_length=128,verbose_name='开户省份')
	open_city = models.CharField(blank=True,null=True,max_length=128,verbose_name='开户市')
	bank_branch = models.CharField(blank=True,null=True,max_length=128,verbose_name='开户支行')
	organization = models.ForeignKey('Organization',blank=True, null=True,on_delete=models.SET_NULL, verbose_name='所属机构')
	agency = models.ForeignKey('Agency',blank=True, null=True,on_delete=models.SET_NULL, verbose_name='所属代理')
	status = models.CharField(choices=STATUS_CHOICES,max_length=10,default='1',verbose_name='状态')
	is_freeze = models.BooleanField(default=False,verbose_name='能否冻结')
	web_app = models.CharField(choices=WEB_APP_CHOICES,max_length=32,default='back',verbose_name='申请端口')
	last_login_time = models.DateTimeField(blank=True, null=True,verbose_name='最后登陆时间')
	date_joined = models.DateTimeField( default=timezone.now,verbose_name='注册时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '客户'
		verbose_name_plural = '客户'