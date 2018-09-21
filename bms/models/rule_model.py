from django.db import models
from django.utils import timezone
from .org_model import Organization,OPTION_TYPE
from multiselectfield import MultiSelectField
import time

DAYS_CHOICE = (
		('Monday', '星期一'),
		('Tuesday', '星期二'),
		('Wednesday', '星期三'),
		('Thursday', '星期四'),
		('Friday', '星期五'),
		('Saturday', '星期六'),
		('Sunday', '星期日'),
	)
class Fund_In_Rule(models.Model):
	'''入金规则'''
	org = models.ForeignKey(Organization,blank=True,null=True,on_delete=models.SET_NULL,verbose_name='所属机构')
	begin_time = models.TimeField(default='00:00:00',verbose_name='开始时间')
	end_time = models.TimeField(default='23:59:59',verbose_name='结束时间')
	week = MultiSelectField(choices=DAYS_CHOICE, verbose_name='星期')
	min_gateway = models.DecimalField(null=True,max_digits=12,decimal_places=2, verbose_name='网关单笔最小入金金额')
	min_shortcut = models.DecimalField(null=True,max_digits=12,decimal_places=2, verbose_name='快捷单笔最小入金金额')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	class Meta:
		verbose_name = '入金限制表'
		verbose_name_plural = '入金限制表'

class Fund_Out_Rule(models.Model):
	'''出金规则'''
	org = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.SET_NULL,verbose_name='所属机构')
	begin_time = models.TimeField(default='00:00:00',verbose_name='开始时间')
	end_time = models.TimeField(default='23:59:59',verbose_name='结束时间')
	week = MultiSelectField(choices=DAYS_CHOICE, verbose_name='星期')
	max_count_each_day = models.IntegerField(verbose_name='单日最大出金次数')
	max_money_each_day = models.DecimalField(null=True,max_digits=12,decimal_places=2, verbose_name='单日最大出金金额')
	max_money_each_time = models.DecimalField(null=True,max_digits=12,decimal_places=2, verbose_name='单笔最大出金金额')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	class Meta:
		verbose_name = '出金限制表'
		verbose_name_plural = '出金限制表'


EXCHANGE_TYPE=(
	('enquiry','询价时间设置'),
	('order','下单时间设置'),
	('close','平仓时间设置')
)

class Exchange_Rule(models.Model):
	'''交易询价时间设置'''
	org = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='所属机构')
	begin_time = models.TimeField(default='00:00:00',verbose_name='开始时间')
	end_time = models.TimeField(default='23:59:59',verbose_name='结束时间')
	week = MultiSelectField(choices=DAYS_CHOICE,verbose_name='星期')
	option_type = models.CharField(choices=OPTION_TYPE,max_length=32,verbose_name='期权类型')
	type = models.CharField(choices=EXCHANGE_TYPE,max_length=32,verbose_name='所属类型')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')

	class Meta:
		verbose_name = '交易询价时间设置'
		verbose_name_plural = '交易询价时间设置'


class Notional_Principal(models.Model):
	'''名义本金设置'''
	org = models.ForeignKey(Organization,blank=True,null=True,on_delete=models.SET_NULL,verbose_name='所属机构')
	option_type = models.CharField(choices=OPTION_TYPE, max_length=32, verbose_name='期权类型')
	number = models.DecimalField(null=True,max_digits=12,decimal_places=2, verbose_name='名义本金数额')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	class Meta:
		verbose_name = '名义本金设置'
		verbose_name_plural = '名义本金设置'
# class Order_Rule(models.Model):
# 	'''下单时间设置'''
# 	org = models.ForeignKey(Organization, blank=True, null=True, verbose_name='所属机构')
# 	begin_time = models.TimeField(verbose_name='开始时间')
# 	end_time = models.TimeField(verbose_name='结束时间')
# 	type = models.CharField(choices=OPTION_TYPE, max_length=32, verbose_name='期权类型')
# 	week = MultiSelectField(choices=WEEK_CHOICE, verbose_name='星期')
# 	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
# 	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
#
# 	class Meta:
# 		verbose_name = '询价时间设置'
# 		verbose_name_plural = '询价时间设置'
#
# class Close_Rule(models.Model):
# 	'''平仓时间设置'''
# 	org = models.ForeignKey(Organization, blank=True, null=True, verbose_name='所属机构')
# 	begin_time = models.TimeField(verbose_name='开始时间')
# 	end_time = models.TimeField(verbose_name='结束时间')
# 	type = models.CharField(choices=OPTION_TYPE, max_length=32, verbose_name='期权类型')
# 	week = MultiSelectField(choices=WEEK_CHOICE, verbose_name='星期')
# 	date_joined = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
# 	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
#
# 	class Meta:
# 		verbose_name = '询价时间设置'
# 		verbose_name_plural = '询价时间设置'