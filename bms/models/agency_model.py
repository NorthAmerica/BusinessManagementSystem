from django.db import models
from django.utils import timezone
import time
from django.contrib.auth.models import AbstractUser

def invite_num_key():
	'''邀请码产生器'''
	return 'A'+str(int(time.time()*1000))+str(int(time.clock()*1000000))


class Agency(models.Model):
	"""代理"""
	name = models.CharField(max_length=100, verbose_name='名称')
	organization = models.ForeignKey('Organization', null=True, on_delete=models.SET_NULL,
	                                 verbose_name='所属机构')
	rebate_x = models.DecimalField(blank=True, null=True,max_digits=12,decimal_places=2, verbose_name='返佣参数X')
	rebate_y = models.DecimalField(blank=True, null=True,max_digits=12,decimal_places=2, verbose_name='返佣参数Y')
	rebate_z = models.DecimalField(blank=True, null=True,max_digits=12,decimal_places=2, verbose_name='返佣参数Z')
	f_agency = models.ForeignKey('Agency', blank=True, null=True, on_delete=models.SET_NULL,
	                                 verbose_name='上级代理')
	invite_num = models.CharField(max_length=100,default=invite_num_key,verbose_name='邀请码')
	is_freeze = models.BooleanField(default=False, verbose_name='能否冻结')
	date_joined = models.DateTimeField(default=timezone.now,verbose_name='添加时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '归属'
		verbose_name_plural = '归属'