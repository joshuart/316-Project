from django.db import models

class Seller(models.Model):
	"""Seller relation stores the relavant information about the seller's name and contact information"""
	# first_name = models.CharField(max_length = 200)
	# last_name = models.CharField(max_length = 200)
	email = models.EmailField(max_length = 200)

	def __unicode__():
		return self.email

class Book(models.Model):
	"""Book relation contains the relavant information about the books for sale"""
	post_date = models.DateTimeField('date posted')
	seller_email = models.ForeignKey(Seller)
	course_dept = models.CharField(max_length = 8)
	course_num = models.IntegerField(default = 0)
	# course_num_letter = models.CharField(max_length = 1)
	professor = models.CharField(max_length = 200)
	title = models.CharField(max_length = 200)
	author_first_name = models.CharField(max_length = 200)
	author_last_name = models.CharField(max_length= 200)
	edition = models.IntegerField(default = 1)
	condition = models.CharField(max_length = 20)
	price = models.IntegerField(default = 0.99)
	isbn = models.IntegerField(default = 0)

	def __unicode__():
		return self.title, self.price
	

		
		