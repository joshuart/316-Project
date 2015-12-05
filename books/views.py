from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from books.models import Book, Listing
from books.forms import UserCreateForm
from django.forms.models import ModelForm, inlineformset_factory, modelformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import views
from django.contrib import auth
from django import forms
from django.utils.translation import ugettext_lazy as _
import time
from django.conf import settings

from django.core.mail import send_mail




def index(request):
	# return HttpResponse("Welcome to Duke's Book Exchange")
	return render_to_response('books/index.html',
		{}, 
		context_instance=RequestContext(request))


def register(request):
	if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if form.is_valid():
			form.save()
			form_email = form.cleaned_data['email']
			form_username = form.cleaned_data['username']
			#form_full_name = form.cleaned_data.get("full_name")
			subject = 'Your message is received.'
			from_email = settings.EMAIL_HOST_USER
			to_email = [form_email]
			contact_message = """Hi %s: 
Thank you for registering at dukebooktrading. Thank you.

				Duke Book Trading Team""" %(form_username)
			send_mail(subject, contact_message,from_email, to_email,fail_silently = False)





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
		error_messages = {
			'buy_it_now_price': {
				'min_value': _("Sorry, but the price must be between $0-$999.99!")
			},
			'edition': {
				'min_value': _("An edition less than 1 doesn't make sense!")
			},
			'start_bid': {
				"min_value": _("Sorry, but the price must be between $0-$999.99!")
			},
		}




@login_required(login_url = reverse_lazy('books.views.login'))
def list(request):
	return render_to_response('books/list.html',
        { 'ListBookForm' : ListBookForm(),},
        context_instance=RequestContext(request))




def list_submit(request):
	args = {}
	if request.method == "POST":
		listForm = ListBookForm(request.POST)
		if listForm.is_valid():
			listing = listForm.save(commit = False)
			listing.seller_email = request.user.email
			listing.start_time = int(time.time())
			listing.active = True
			listing.save()

			form_email = request.user.email
			form_username = request.user.username
			subject = 'Your listing has been posted.'
			from_email = settings.EMAIL_HOST_USER
			form_title = listForm.cleaned_data['title']
			to_email = [form_email]
			contact_message = """Hi %s: 
Thank you for listing at dukebooktrading. Your listing of %s has been posted. Thank you.

				Duke Book Trading Team""" %(form_username, form_title)
			send_mail(subject, contact_message,from_email, to_email,fail_silently = False)


			return HttpResponseRedirect(reverse('books.views.all_books'))
	else:
		listForm = ListBookForm()
	args['ListBookForm'] = listForm
	return render(request, 'books/list.html', args)



def navigation(request):
	return render_to_response('books/navigation.html',
		{},
		context_instance=RequestContext(request))


def get_isbn_listings(request, match_isbn):
	listings = Listing.objects.filter(book_id=match_isbn[0])


	return render_to_response('books/listings-for-book.html',
		{'all_listings':listings,},
		context_instance=RequestContext(request))

def get_listings_for_book(request, match_isbn):

	listings = Listing.objects.filter(book_id=match_isbn, start_time__lte= int(time.time())) #, active = True)
	return render_to_response('books/listings-for-book.html',
		{'all_listings':listings,},
		context_instance=RequestContext(request))


def all_books(request):
	all_listings = Book.objects.all()
	return render_to_response('books/all-books.html',
		{ 'book_list':all_listings, },
		context_instance=RequestContext(request))


@login_required(login_url = reverse_lazy('books.views.login'))
def edit_list(request):
	return HttpResponse("Welcome to the edit-listings page")

def buy_book(request, listing_id):
	listing = Listing.objects.filter(id = listing_id)
	listing.active = False
	return HttpResponse("Okay, we'll let the seller know. Expect to hear back from them soon!")


