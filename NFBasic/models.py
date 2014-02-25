from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
	n_detail = models.CharField(max_length=10000)
	n_pubDate = models.CharField(max_length=100)
	n_grade = models.CharField(max_length=10)
	n_sender = models.ForeignKey(User)
	n_date = models.DateTimeField('date')

	def __unicode__(self):
		return self.n_detail


class Announcement(models.Model):
	a_title = models.CharField(max_length=50)
	a_detail = models.CharField(max_length=10000)
	a_pubDate = models.CharField(max_length=30)
	a_grade = models.CharField(max_length=10)
	a_sender = models.ForeignKey(User)
	a_image = models.FileField(upload_to='documents/%Y/%m/%d')

	def __unicode__(self):
		return self.a_title


class DeviceToken(models.Model):
	ios_token = models.CharField(max_length=80)