from __future__ import absolute_import
from celery.decorators import task
from celery.registry import tasks
from celery.task import Task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from django.template.loader import render_to_string
#from django.utils.html import strip_tags

#from django.core.mail import EmailMultiAlternatives
from celery import Celery

from celery.task import PeriodicTask
from datetime import timedelta
from celery.schedules import crontab
from celery.task import periodic_task

from books.models import Listing, Book, Bid
import time
import calendar

#periodic_task for listings with buy_it_now function only
@periodic_task(run_every=crontab(minute=0, hour=0))  #Execute daily at midnight.
def send_email_BIN():
	from_email = settings.EMAIL_HOST_USER
	#replace the follow pseudo code with real code:
	#select listings in buy_it_now style only with start_time earlier than three days ago but later than four days ago as dying_listings
	dying_listings = Listing.objects.filter(start_time__lte = calendar.timegm(time.gmtime()) - 86400000*3).filter(start_time__gt = calendar.timegm(time.gmtime())- 86400000*4).filter(is_buy_it_now = True).filter(is_auction = False)
	
	for listing in dying_listings:
		task_seller_email = listing.seller_email
		task_seller_first = User.objects.get(email = task_seller_email).first_name
		task_seller_last = User.objects.get(email = task_seller_email).last_name
		task_listing_title = Book.objects.get(isbn = listing.book_id).title

		subject = "Your listing didn't sell"
		to_email = task_seller_email
		contact_message = """Hi %s %s: 
Your listing of [%s] didn't sell. Welcome to relist your listing at DukeBookTrading.

				Best Wishes,
				Duke Book Trading Team""" %(task_seller_first, task_seller_last,task_listing_title)
		send_mail(subject, contact_message,from_email, to_email,fail_silently = False)


#periodic_task for listings with bid function (can also be buy_it_now)
@periodic_task(run_every=crontab(minute=0, hour=0))  #Execute daily at midnight.
def send_email_bid():
	from_email = settings.EMAIL_HOST_USER
	#replace the follow pseudo code with real code:
	#select bids whose listing's start_time is earlier than three days ago but later than four days ago as dying_bids
	for bid in dying_bids:
		
		task_buyer_email = bid.bidder_email
		task_buyer_first = User.objects.get(email = task_buyer_email).first_name
		task_buyer_last = User.objects.get(email = task_buyer_email).last_name
		#task_buyer_major = 

		task_listing = Listing.objects.get(id = bid.listing_id)

		task_seller_email = task_listing.seller_email
		task_seller_first = User.objects.get(email = task_seller_email).first_name
		task_seller_last = User.objects.get(email = task_seller_email).last_name
		#task_seller_major = 

		task_listing_title = Book.objects.get(isbn = task_listing.book_id).title
		task_bid_price = bid.bid_price
		task_listing_start_price = task_listing.start_bid

		#didn't sell
		if task_bid_price <= task_listing_start_price:
			subject = "Your listing didn't sell"
			to_email = task_seller_email
			contact_message = """Hi %s %s: 
Your listing of [%s] didn't sell. Welcome to relist your listing at DukeBookTrading.

				Best Wishes,
				Duke Book Trading Team""" %(task_seller_first, task_seller_last,task_listing_title)
			send_mail(subject, contact_message,from_email, to_email,fail_silently = False)

		else:
		#sold
			#email seller:
			subject1 = "Your listing sold"
			to_email1 = task_seller_email
			contact_message1 = """Hi %s %s: 
Your listing of [%s] just sold for %s. The buyer is %s %s. 
Please contact the buyer at %s for book delivery.

				Best Wishes,
				Duke Book Trading Team""" %(task_seller_first, task_seller_last,task_listing_title,task_bid_price, task_buyer_first,task_buyer_last,task_buyer_email)
			send_mail(subject1, contact_message1,from_email, to_email1,fail_silently = False)



			#email buyer:
			subject2 = "Thank you for your purchase at DukeBookTrading"
			to_email2 = task_buyer_email
			contact_message2 = """Hi %s %s: 
Thank you for your purchase of [%s]. The seller is %s %s.
Please contact the seller at %s for book delivery.

				Best Wishes,
				Duke Book Trading Team""" %(task_buyer_first, task_buyer_last,task_listing_title, task_seller_first, task_seller_last, task_seller_email)
			send_mail(subject2, contact_message2,from_email, to_email2,fail_silently = False)

















    # subject, from_email, to = 'Your listing is ending soon!', settings.EMAIL_HOST_USER, 'xiaoxian.wu@duke.edu'
    # #print("fffff")
    # contact_message = "XXXXX"

    # #html_content = render_to_string('email_signup.html', {'user': user.full_name})
    # #text_content = strip_tags(html_content)
    # msg = EmailMultiAlternatives(subject, contact_message, from_email, [to])
    # #msg.attach_alternative(html_content, "text/html")
    # msg.send()

