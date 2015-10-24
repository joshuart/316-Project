from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required = True)
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit = True):
		user = super(UserCreateForm, self).save(commit = False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

# I got this code from: http://jessenoller.com/blog/2011/12/19/quick-example-of-extending-usercreationform-in-django
# Ask Prof. Yang if that's okay
