from django.conf import settings
from django.db import models


class Book(models.Model):
	"""Book relation contains the relavant information about the books for sale"""
	post_date = models.DateTimeField('date posted')
	seller_email = models.ForeignKey(settings.AUTH_USER_MODEL)
	course_dept = models.CharField(max_length = 8)
	course_num = models.IntegerField(default = 0)
	# course_num_letter = models.CharField(max_length = 1)
	professor = models.CharField(max_length = 200)
	title = models.CharField(max_length = 200)
	author_first_name = models.CharField(max_length = 200, null = True)
	author_last_name = models.CharField(max_length= 200)
	edition = models.IntegerField(default = 1)
	condition = models.CharField(max_length = 20)
	price = models.IntegerField(default = 0.99)
	isbn = models.IntegerField(default = 0)

	class Meta:
		db_table = u'book'

	def __unicode__():
		return self.seller_email, self.title, self.price
	


# References used:
# http://stackoverflow.com/questions/18992847/best-way-to-reference-the-user-model-in-django-1-5
		
		