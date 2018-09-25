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

CHANGE_TYPE_CHOICES = (
		('in_online', '网银入金'),
		('in_offline', '线下入金'),
		('out_online', '网银出金'),
		('out_offline', '线下出金'),
		('order', '下单'),
		('close', '结算'),
	)

TYPE_CHOICE=(
		('org', '机构模板'),
		('agency', '代理模板'),
	)


BUSINESS_TYPE = (
		('options','期权交易'),
		('margin','融资融券'),
)

OPTION_TYPE = (
		('commodity','商品期权'),
		('stock','个股期权'),
	)

EVENT_TYPE_CHOICES = (
		('DEBUG','调试'),
		('INFO','信息'),
		('WARNING', '警告'),
		('ERROR', '错误'),
	)

EXCHANGE_TYPE=(
	('enquiry','询价时间设置'),
	('order','下单时间设置'),
	('close','平仓时间设置')
)

DAYS_CHOICE = (
		('Monday', '星期一'),
		('Tuesday', '星期二'),
		('Wednesday', '星期三'),
		('Thursday', '星期四'),
		('Friday', '星期五'),
		('Saturday', '星期六'),
		('Sunday', '星期日'),
	)

IDENTITY_CHOICE=(
		('org','机构管理员'),
		('agency','代理管理员'),
		('admin','后台管理员'),
	)