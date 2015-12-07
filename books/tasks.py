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

from books.models import Listing, Bid, Book
import time
import calendar

#@periodic_task for listings with buy_it_now function only
@periodic_task(run_every=crontab(minute=0, hour=0))  #Execute daily at midnight.
def send_email_BIN():
	from_email = settings.EMAIL_HOST_USER
	#replace the follow pseudo code with real code:
	#select listings in buy_it_now style only with start_time earlier than three days ago but later than four days ago as dying_listings
	dying_listings = Listing.objects.filter(start_time__lte = calendar.timegm(time.gmtime()) - 86400000*3).filter(start_time__gt = calendar.timegm(time.gmtime())- 86400000*4).filter(is_buy_it_now = True).filter(is_auction = False)
	#just for testing: select listings with start_time ealier than 10 seconds ago but later than 20 seconds ago as dying_listings
	#dying_listings = Listing.objects.filter(start_time__lte = calendar.timegm(time.gmtime()) - 10000).filter(start_time__gt = calendar.timegm(time.gmtime())- 20000).filter(is_auction = True)


	for listing in dying_listings:
		task_seller_email = listing.seller_email
		task_seller_first = User.objects.get(email = task_seller_email).first_name
		task_seller_last = User.objects.get(email = task_seller_email).last_name
		task_listing_title = Book.objects.get(isbn = listing.book_id).title   #listing.title

		subject = "Your listing didn't sell"
		to_email = task_seller_email
		contact_message = """Hi %s %s: 
Your listing of [%s] didn't sell. Welcome to relist your listing at DukeBookTrading.

				Best Wishes,
				Duke Book Trading Team""" %(task_seller_first, task_seller_last,task_listing_title)
		send_mail(subject, contact_message,from_email, [to_email],fail_silently = False)


#periodic_task for listings with bid function (can also be buy_it_now)
@periodic_task(run_every=crontab(minute=0, hour=0))  #Execute daily at midnight.
#@periodic_task(run_every=timedelta(seconds=8))  #Execute every 8 seconds.
def send_email_bid():
	from_email = settings.EMAIL_HOST_USER
	#replace the follow pseudo code with real code:
	#select listings with start_time earlier than three days ago but later than four days ago as dying_listings
	dying_listings = Listing.objects.filter(start_time__lte = calendar.timegm(time.gmtime()) - 86400000*3).filter(start_time__gt = calendar.timegm(time.gmtime())- 86400000*4).filter(is_auction = True)
	#just for testing: select listings with start_time ealier than 10 seconds ago but later than 20 seconds ago as dying_listings
	#dying_listings = Listing.objects.filter(start_time__lte = calendar.timegm(time.gmtime()) - 10000).filter(start_time__gt = calendar.timegm(time.gmtime())- 20000).filter(is_auction = True)
	#just_bids = Bid.objects.filter(bid_time_lte = calendar.timegm(time.gmtime()) - 10000).filter(bid_time_gt = calendar.timegm(time.gmtime())- 20000)
	for listing in dying_listings:

		task_listing_title = Book.objects.get(isbn = listing.book_id).title    #listing.title
		task_seller_email = listing.seller_email
		task_seller_first = User.objects.get(email = task_seller_email).first_name
		task_seller_last = User.objects.get(email = task_seller_email).last_name

		task_bids = Bid.objects.filter(listing_id = listing.id)
		if len(task_bids) <= 0:  #didn't sell
			subject = "Your listing didn't sell"
			to_email = task_seller_email
			contact_message = """Hi %s %s: 
Your listing of [%s] didn't sell. Welcome to relist your listing at DukeBookTrading.

					Best Wishes,
					Duke Book Trading Team""" %(task_seller_first, task_seller_last,task_listing_title)
			send_mail(subject, contact_message,from_email, to_email,fail_silently = False)

		elif len(task_bids) >= 1: #sold
			task_bid = Bid.objects.get(listing_id = listing.id)
			task_buyer_email = task_bid.bidder_email
			task_buyer_first = User.objects.get(email = task_buyer_email).first_name
			task_buyer_last = User.objects.get(email = task_buyer_email).last_name
			task_bid_price = task_bid.bid_price

			#email seller:
			subject1 = "Your listing sold"
			to_email1 = task_seller_email
			contact_message1 = """Hi %s %s: 
Your listing of [%s] just sold for %s. The buyer is %s %s. 
Please contact the buyer at %s for book delivery.

					Best Wishes,
					Duke Book Trading Team""" %(task_seller_first, task_seller_last,task_listing_title,task_bid_price, task_buyer_first,task_buyer_last,task_buyer_email)
			send_mail(subject1, contact_message1,from_email, [to_email1],fail_silently = False)



			#email buyer:
			subject2 = "Thank you for your purchase at DukeBookTrading"
			to_email2 = task_buyer_email
			contact_message2 = """Hi %s %s: 
Thank you for your purchase of [%s]. The seller is %s %s.
Please contact the seller at %s for book delivery.

					Best Wishes,
					Duke Book Trading Team""" %(task_buyer_first, task_buyer_last,task_listing_title, task_seller_first, task_seller_last, task_seller_email)
			send_mail(subject2, contact_message2,from_email, [to_email2],fail_silently = False)



    # subject, from_email, to = 'Your listing is ending soon!', settings.EMAIL_HOST_USER, 'xiaoxian.wu@duke.edu'
    # #print("fffff")
    # contact_message = "XXXXX"

    # #html_content = render_to_string('email_signup.html', {'user': user.full_name})
    # #text_content = strip_tags(html_content)
    # msg = EmailMultiAlternatives(subject, contact_message, from_email, [to])
    # #msg.attach_alternative(html_content, "text/html")
    # msg.send()






@periodic_task(run_every=timedelta(seconds=5))  #Execute every 5 seconds.
def send_email_demo_only():
	from_email = settings.EMAIL_HOST_USER
	#replace the follow pseudo code with real code:
	#select listings with start_time earlier than three days ago but later than four days ago as dying_listings
	#dying_listings = Listing.objects.filter(start_time__lte = calendar.timegm(time.gmtime()) - 86400000*3).filter(start_time__gt = calendar.timegm(time.gmtime())- 86400000*4).filter(is_auction = True)
	#just for testing: select listings with start_time ealier than 10 seconds ago but later than 20 seconds ago as dying_listings
	#dying_listings = Listing.objects.filter(start_time__lte = calendar.timegm(time.gmtime()) - 10000).filter(start_time__gt = calendar.timegm(time.gmtime())- 20000).filter(is_auction = True)
	#send_mail("Great!", "Yes!",from_email, ["tw159@duke.edu"],fail_silently = False)
	
	#just_bids = Bid.objects.filter(bid_time__lte = calendar.timegm(time.gmtime()) - 10000).filter(bid_time__gt = calendar.timegm(time.gmtime())- 20000)
	just_bids = Bid.objects.filter(bidder_email = "tw159@duke.edu").filter(bid_time__gt = calendar.timegm(time.gmtime()) - 5000)
	for bid in just_bids:
		email = bid.bidder_email
		bid_listing_id = bid.listing_id
		task_listing = Listing.objects.get(id = bid_listing_id)
		book = Book.objects.get(isbn = task_listing.book_id)
		title = book.title
		price = bid.bid_price

		subject2 = "Thank you for your bidding"
		to_email2 = email
		contact_message2 = """Hi: 
Thank you for your bidding on %s for the price of %s.

					Best Wishes,
					Duke Book Trading Team"""%(title,price)
		send_mail(subject2, contact_message2,from_email, [to_email2],fail_silently = False)
	





