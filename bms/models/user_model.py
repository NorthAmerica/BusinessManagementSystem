from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from .choices_for_model import IDENTITY_CHOICE

class User(AbstractUser):
	"""后台用户"""

	identity = models.CharField(choices=IDENTITY_CHOICE,max_length=10,default='admin',verbose_name='管理员身份')
	position = models.CharField(blank=True, null=True, max_length=100, verbose_name='职位')
	mobile_phone = models.CharField(blank=True, null=True, max_length=100, verbose_name='手机号码')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')


	def __str__(self):
		return self.username
	class Meta:
		# app_label = '用户组'
		verbose_name = '后台用户'
		verbose_name_plural = '后台用户'

class Org_User(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,verbose_name='后台用户')
	organization = models.ForeignKey('Organization', blank=True, null=True, on_delete=models.SET_NULL,verbose_name='所属机构')
	# org_groups = models.ManyToManyField(
	# 	 'Org_Group',
	# 	verbose_name=('机构组'),
	# 	blank=True,)
	# org_permissions = models.ManyToManyField(
	# 	'Org_Permission',
	# 	verbose_name=('机构权限'),
	# 	blank=True,
	# )
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	# def get_all_org_user(self):
	# 	return list(User.objects.filter(identity='org'))

	class Meta:
		# app_label = '用户组'
		verbose_name = '机构后台用户'
		verbose_name_plural = '机构后台用户'

class Agency_User(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,verbose_name='后台用户')
	agency = models.ForeignKey('Agency', blank=True, null=True, on_delete=models.SET_NULL,verbose_name='所属代理')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	class Meta:
		# app_label = '用户组'
		verbose_name = '归属后台用户'
		verbose_name_plural = '归属后台用户'