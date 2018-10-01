from django.db import models
from django.utils import timezone
import time
from multiselectfield import MultiSelectField
from .choices_for_model import BUSINESS_TYPE
from django.contrib.auth.models import AbstractUser

def invite_num_key():
	'''邀请码产生器'''
	return 'A'+str(int(time.time()*1000))+str(int(time.clock()*1000000))


class Agency(models.Model):
	"""归属"""
	name = models.CharField(max_length=100, verbose_name='名称')
	organization = models.ForeignKey('Organization', null=True, on_delete=models.SET_NULL,
	                                 verbose_name='所属机构')
	rebate_x = models.DecimalField(blank=True, null=True,default=0,max_digits=12,decimal_places=2, verbose_name='返佣参数X')
	rebate_y = models.DecimalField(blank=True, null=True,default=0,max_digits=12,decimal_places=2, verbose_name='返佣参数Y')
	rebate_z = models.DecimalField(blank=True, null=True,default=0,max_digits=12,decimal_places=2, verbose_name='返佣参数Z')
	f_agency = models.ForeignKey('Agency', blank=True, null=True, on_delete=models.SET_NULL,
	                                 verbose_name='上级归属')
	allow_business = MultiSelectField(choices=BUSINESS_TYPE,blank=True, null=True, verbose_name='允许的业务类型')
	account_balance = models.DecimalField(blank=True, null=True,default=0,max_digits=12,decimal_places=2, verbose_name='账户余额')
	grade = models.IntegerField(blank=True, null=True,verbose_name='归属等级')
	invite_num = models.CharField(max_length=100,default=invite_num_key,verbose_name='邀请码',help_text='作为邀请客户开户ID')
	is_freeze = models.BooleanField(default=False, verbose_name='能否冻结',help_text='冻结情况下，归属不能出金或新开客户')
	date_joined = models.DateTimeField(default=timezone.now,verbose_name='添加时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '归属'
		verbose_name_plural = '归属'