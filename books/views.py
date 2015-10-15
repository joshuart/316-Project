from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from books.models import Seller, Book
from django.forms.models import ModelForm, inlineformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def index(request):
	# return HttpResponse("Welcome to Duke's Book Exchange")
	return render_to_response('books/base.html',
		{}, 
		context_instance=RequestContext(request))


def list(request):
	return HttpResponse("Welcome to the list page")
	# return render_to_response('books/list.html',
	# 	{}, 
	# 	context_instance=RequestContext(request))

def all_books(request):
	return HttpResponse("Welcome to the all-books page")
	# return render_to_response('books/all-books.html',
	# 	{'books' : Book.objects.all().order)by('course_dept', 'course_num', 'professor', 'title')}, 
	# 	context_instance = RequestContext(request)) 
