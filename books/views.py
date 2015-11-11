from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from books.models import Book, Listing
from books.forms import UserCreateForm
from django.forms.models import ModelForm, inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import views
from django.contrib import auth
# import pytz
import datetime




def index(request):
	# return HttpResponse("Welcome to Duke's Book Exchange")
	return render_to_response('books/index.html',
		{}, 
		context_instance=RequestContext(request))


def register(request):
	# return HttpResponse("Please finish the registration page")
	if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('books.views.login'))
	else:
		form = UserCreateForm()
	return render_to_response('books/register.html',
		{ 'form':form, }, 
		context_instance = RequestContext(request))


def logout(request):
	auth_logout(request)
	return HttpResponseRedirect(reverse('books.views.index'))

def login(request):
	return render_to_response('books/login.html',
		{},
		context_instance = RequestContext(request))


class ListBookForm(ModelForm):
	class Meta:
		model = Listing
		# fields ='__all__'
		exclude = ['start_time', 'seller_email', 'active',]



@login_required(login_url = reverse_lazy('books.views.login'))
def list(request):

    return render_to_response('books/list.html',
        { 'ListBookForm' : ListBookForm(),},
        context_instance=RequestContext(request))




def list_submit(request):
	listForm = ListBookForm(request.POST)
	listing = listForm.save(commit = False)
	listing.seller_email = request.user.email
	listing.start_time = datetime.datetime.now()
	listing.active = True
	listing.save()
	return HttpResponseRedirect(reverse('books.views.all_books'))


def navigation(request):
	return render_to_response('books/navigation.html',
		{},
		context_instance=RequestContext(request))



def all_books(request):
	return HttpResponse("Welcome to the all-books page")
	# return render_to_response('books/all-books.html',
	# 	{'books' : Book.objects.all().order)by('course_dept', 'course_num', 'professor', 'title')}, 
	# 	context_instance = RequestContext(request)) 
