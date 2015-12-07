from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from books.models import Listing, Book
from books.forms import UserCreateForm
from django.forms.models import ModelForm, inlineformset_factory, modelformset_factory
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.contrib import auth
from django import forms
from django.utils.translation import ugettext_lazy as _
import time
from django.conf import settings

from django.core.mail import send_mail

#from .tasks import send_email_BIN
#from .tasks import send_email_bid


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
		# listForm.fields["Book"].queryset = Book.objects.raw('Select title from Book')
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
	listings = Listing.objects.filter(isbn=match_isbn[0], active = True, start_time__gte= int(time.time()) - 259200)


	return render_to_response('books/listings-for-book.html',
		{'all_listings':listings,},
		context_instance=RequestContext(request))

def get_listings_for_book(request, match_isbn, match_title):


	listings = Listing.objects.filter(isbn=match_isbn, active = True, start_time__gte= int(time.time()) - 259200)
	if Listing.objects.filter(isbn=match_isbn, active = True, start_time__gte= int(time.time()) - 259200).count() == 0:
		return render_to_response('books/no-listings-for-book.html',
			{'the_title':match_title, 'all_listings':listings,},
			context_instance=RequestContext(request))
	return render_to_response('books/listings-for-book.html',
			{'the_title':match_title, 'all_listings':listings,},
			context_instance=RequestContext(request))

def get_bid_info(request, match_listing):
	return

def all_books(request):

	all_listings = Listing.objects.raw('Select distinct title, id from listing')

	return render_to_response('books/all-books.html',
		{ 'book_list':all_listings, },
		context_instance=RequestContext(request))


@login_required(login_url = reverse_lazy('books.views.login'))
def edit_list(request):
	return HttpResponse("Welcome to the edit-listings page")


def buy_book(request, listing_id):



	listing = Listing.objects.get(id = listing_id)
	listing.active = False

	#Send email to the seller:
	form_seller_email = listing.seller_email
	form_seller_first = User.objects.get(email = form_seller_email).first_name
	form_seller_last = User.objects.get(email = form_seller_email).last_name
	#form_seller_major = User.objects.get(email = form_seller_email).major

	form_buyer_email = request.user.email
	form_buyer_first = request.user.first_name
	form_buyer_last = request.user.last_name
	#form_buyer_major = request.user.major

	subject_seller = 'Your listing sold'
	subject_buyer = 'You just bought a book'
	from_email = settings.EMAIL_HOST_USER
	#form_title = listing.title
	form_title = Book.objects.get(isbn = listing.book_id).title
	contact_message_seller = """Hi %s %s: 
Your listing of %s just sold. The buyer is %s %s. You can contact the buyer at %s. Thank you.

				Best Wishes,
				Duke Book Trading Team""" %(form_seller_first, form_seller_last, form_title, form_buyer_first, form_buyer_last, form_buyer_email)
	send_mail(subject_seller, contact_message_seller,from_email, [form_seller_email],fail_silently = False)


	contact_message_buyer = """Hi %s %s: 
Thank you for purchasing %s at dukebooktrading. The seller is %s %s. You can contact the seller at %s. Thank you.

				Best Wishes,
				Duke Book Trading Team""" %(form_buyer_first, form_buyer_last, form_title, form_seller_first, form_seller_last, form_seller_email)
	send_mail(subject_buyer, contact_message_buyer,from_email, [form_buyer_email],fail_silently = False)





	return HttpResponse("Okay, we'll let the seller know. Expect to hear back from them soon!")
'''
def buy_it_now_click(request):
	#when someone clicks the buy_it_now button, an email will be sent to both buyer and seller
'''
