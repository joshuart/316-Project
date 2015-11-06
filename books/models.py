from django.conf import settings
from django.db import models

class Book(models.Model):
	isbn = models.CharField(max_length = 13, primary_key = True)
	title = models.CharField(max_length = 200)
	edition = models.PositiveSmallIntegerField(default = 1)
	author_first_name = models.CharField(max_length = 200, null = True)
	author_last_name = models.CharField(max_length = 200)


class Bid(models.Model):
	bid_time = models.DateTimeField('bid time')
	bid_price = models.DecimalField(max_digits = 5, decimal_places = 2)
	bidder_email = models.EmailField(settings.AUTH_USER_MODEL)
	seller_email = models.EmailField(settings.AUTH_USER_MODEL)
	book_ISBN = models.ForeignKey('Book')
	listing_start_time = models.DateTimeField('date posted') #references



class Listing(models.Model):
	"""Book relation contains the relavant information about the books for sale"""
	POOR = "poor"
	FAIR = "fair"
	GOOD = "good"
	EXCELLENT = "excellent"
	NEW = "new"
	CONDITION_CHOICES = (
		(POOR, "Poor"),
		(FAIR, "Fair"),
		(GOOD, "Good"),
		(EXCELLENT, "Excellent"),
		(NEW, "New"), 
		)


	start_time = models.DateTimeField('date posted')
	seller_email = models.ForeignKey(settings.AUTH_USER_MODEL) #references
	course_dept = models.CharField(max_length = 8)
	course_num = models.IntegerField(default = 0)
	# course_num_letter = models.CharField(max_length = 1)
	professor = models.CharField(max_length = 200)
	title = models.CharField(max_length = 200)
	author_first_name = models.CharField(max_length = 200, null = True)
	author_last_name = models.CharField(max_length= 200)
	edition = models.IntegerField(default = 1)
	condition = models.CharField(max_length = 9, choices = CONDITION_CHOICES, default = GOOD)
	price = models.IntegerField(default = 0.99)
	book_ISBN = models.ForeignKey('Book')
	is_auction = models.IntegerField()
	is_buy_it_now = models.IntegerField(default = 0)
	description = models.TextField(max_length = 500)
	buy_it_now_price = models.IntegerField(default = 0)
	start_price = models.IntegerField(default = buy_it_now_price)
	current_bid = models.DecimalField(max_digits = 5, decimal_places = 2) #references

	class Meta:
		db_table = u'listing'

	def __unicode__():
		return self.seller_email, self.title, self.price
	


# References used:
# http://stackoverflow.com/questions/18992847/best-way-to-reference-the-user-model-in-django-1-5
		
		