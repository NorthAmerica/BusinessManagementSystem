from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group,Permission
from .user_model import User
from multiselectfield import MultiSelectField
from .choices_for_model import OPTION_TYPE,BUSINESS_TYPE


def logo_path_handler(instance, filename):
	return "logo/{id}/{file}".format(id=instance.account, file=filename)  # 保存路径和格式


def cachet_path_handler(instance, filename):
	return "cachet/{id}/{file}".format(id=instance.account, file=filename)  # 保存路径和格式


class Organization(models.Model):
	"""机构"""
	name = models.CharField(max_length=100, verbose_name='名称')
	logo = models.ImageField(upload_to=logo_path_handler, verbose_name='logo')
	cachet = models.ImageField(upload_to=cachet_path_handler, verbose_name='公章')
	account = models.CharField(max_length=200, verbose_name='账户')
	allow_business = MultiSelectField(choices=BUSINESS_TYPE, blank=True, null=True,verbose_name='允许的业务类型')
	is_freeze = models.BooleanField(default=False, verbose_name='能否冻结')
	is_open_commodity = models.BooleanField(default=False,verbose_name='是否开启商品费率')
	is_open_stock = models.BooleanField(default=False,verbose_name='是否开启个股费率')
	account_balance = models.DecimalField(blank=True, null=True, default=0, max_digits=12, decimal_places=2,
	                                      verbose_name='账户余额')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '机构'
		verbose_name_plural = '机构'




class Org_Rule(models.Model):
	'''机构费率规则'''
	org = models.ForeignKey('Organization', null=True, on_delete=models.SET_NULL,
	                        verbose_name='所属机构')
	contract = models.CharField(max_length=100,blank=True, null=True,default='all',verbose_name='合约代码')
	op_type = models.CharField(choices=OPTION_TYPE,max_length=32,verbose_name='期权类型')
	rebate_x = models.DecimalField(blank=True, null=True,max_digits=12,decimal_places=2, verbose_name='参数X')
	rebate_y = models.DecimalField(blank=True, null=True,max_digits=12, decimal_places=2, verbose_name='参数Y')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')

	class Meta:
		verbose_name = '机构费率规则'
		verbose_name_plural = '机构费率规则'
