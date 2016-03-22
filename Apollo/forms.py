from django import forms
from django.contrib.auth.models import User

class RegisterUserForm(forms.Form):
    username = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200,
				label='Password',
				widget = forms.PasswordInput())

    def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError('Username already exists.')
		return username
