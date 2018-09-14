from django.forms import ModelForm
from bms.models import *

class MainUserForm(ModelForm):

	class Meta:
		model = User
		fields = '__all__'