from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from .choices_for_model import STATUS_CHOICES,WEB_APP_CHOICES,BUSINESS_TYPE

def bank_path_handler(instance, filename):
	return "bank/{id}/{file}".format(id=instance.mobile_phone, file=filename)  # 保存路径和格式


class Client(models.Model):
	"""客户"""

	name = models.CharField(max_length=100, verbose_name='用户名')
	mobile_phone = models.CharField(max_length=100, verbose_name='手机号码')
	mailbox = models.EmailField(verbose_name='邮箱地址')
	password = models.CharField(max_length=128, verbose_name='密码')
	identity_card = models.CharField(blank=True, null=True,max_length=128,verbose_name='身份证')
	bank_image = models.ImageField(upload_to=bank_path_handler,blank=True, null=True, verbose_name='银行卡照片')
	bank_card = models.CharField(blank=True, null=True,max_length=128,verbose_name='银行卡号')
	bank_name = models.CharField(blank=True,null=True,max_length=128,verbose_name='开户银行')
	open_city = models.CharField(blank=True,null=True,max_length=128,verbose_name='开户市')
	bank_branch = models.CharField(blank=True,null=True,max_length=128,verbose_name='开户支行')
	organization = models.ForeignKey('Organization',blank=True, null=True,on_delete=models.SET_NULL, verbose_name='所属机构')
	agency = models.ForeignKey('Agency',blank=True, null=True,on_delete=models.SET_NULL, verbose_name='所属代理')
	status = models.CharField(choices=STATUS_CHOICES,max_length=10,default='1',verbose_name='状态')
	is_freeze = models.BooleanField(default=False,verbose_name='能否冻结')
	allow_business = MultiSelectField(choices=BUSINESS_TYPE, blank=True, null=True,verbose_name='允许的业务类型')
	web_app = models.CharField(choices=WEB_APP_CHOICES,max_length=32,default='app',verbose_name='申请端口')
	account_balance = models.DecimalField(blank=True, null=True, default=0, max_digits=12, decimal_places=2,
	                                      verbose_name='账户余额')
	last_login_time = models.DateTimeField(blank=True, null=True,verbose_name='最后登陆时间')
	date_joined = models.DateTimeField( default=timezone.now,verbose_name='注册时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '客户'
		verbose_name_plural = '客户'