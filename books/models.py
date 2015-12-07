from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Book(models.Model):
	isbn = models.CharField(max_length = 13, primary_key = True)
	title = models.CharField(max_length = 200)
	edition = models.PositiveSmallIntegerField(default = 1, validators = [MinValueValidator(1)])
	first_author_name = models.CharField(max_length = 200)
	second_author_name = models.CharField(max_length = 200, blank = True, default = "")
	third_author_name = models.CharField(max_length = 200, blank = True, default = "")	
	fourth_author_name = models.CharField(max_length = 200, blank = True, default = "")	
	fifth_author_name = models.CharField(max_length = 200, blank = True, default = "")



class Listing(models.Model):
	"""Listing relation contains the relavant information about the books for sale"""


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
	
	book = models.ForeignKey(Book) 	
	start_time = models.IntegerField()
	seller_email = models.EmailField(max_length = 200)
	# course_dept = models.CharField(max_length = 8)
	# course_num = models.PositiveSmallIntegerField(default = 101)
	# professor = models.CharField(max_length = 200)
	condition = models.CharField(max_length = 9, choices = CONDITION_CHOICES, default = GOOD)
	is_auction = models.BooleanField(default = False)
	is_buy_it_now = models.BooleanField(default = True) #need to constrain that is_auction or is_buy_it_now can't be both
	description = models.TextField(max_length = 500, blank = True , default = "")
	buy_it_now_price = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
	start_bid = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
	active = models.BooleanField(default = True)
	#current_bid = models.IntegerField(default = 0) #references

	class Meta:
		db_table = u'listing'
		unique_together = (("start_time","seller_email"),)



class Bid(models.Model):
	bid_time = models.IntegerField('bid time')
	bid_price = models.DecimalField(max_digits = 5, decimal_places = 2, validators = [MinValueValidator(0)])
	bidder_email = models.EmailField(settings.AUTH_USER_MODEL) #check bidder is not seller
	listing = models.ForeignKey(Listing)
	


########## Questions ##############
# 1. How to add constraints and triggers to django
# 2. celery cron jobs
# 3. how to handle boolean data

# TODO:
# 1. celery.py
# 2. create constraints
# 3. create listings page
# 4. create modify listings page
# 5. Check for duplicates



# References used:
# http://stackoverflow.com/questions/18992847/best-way-to-reference-the-user-model-in-django-1-5
		
		