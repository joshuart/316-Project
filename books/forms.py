from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re

class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required = True)
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")


	def clean_email(self):
		data = self.cleaned_data['email']
		valid = re.search("(@)?(\w+)(.duke.edu)", data)
		if "@duke.edu" not in data and valid == None: 
			raise forms.ValidationError("Must be a Duke email address")
		return data

	def save(self, commit = True):
		user = super(UserCreateForm, self).save(commit = False)
		user.email = self.clean_email()
		if commit:
			user.save()
		return user

# I got this code from: http://jessenoller.com/blog/2011/12/19/quick-example-of-extending-usercreationform-in-django
#  and here: http://stackoverflow.com/questions/13240032/restrict-user-to-use-a-specific-domain-to-sign-up-django