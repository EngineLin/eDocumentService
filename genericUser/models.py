﻿# coding: utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from mysite import settings
import os
import datetime

EDU = (
	(u'高中' , u'高中'),
	(u'學士' , u'學士'),
	(u'碩士' , u'碩士'),
)

ContactUsKIND = (
	(u'校對問題' , u'校對問題'),
	(u'系統問題' , u'系統問題'),
	(u'營運建議' , u'營運建議'),
	(u'加入我們' , u'加入我們'),
	(u'其他' , u'其他'),
)

class User(AbstractUser):
	phone = models.CharField(max_length=30)
	birthday = models.DateField()
	education = models.CharField(max_length=30, choices=EDU)

	def __unicode__(self):
		return self.username

	def is_editor(self):
		try:
			self.editor
			return True
		except:
			return False

	def is_guest(self):
		try:
			self.guest
			return True
		except:
			return False

class ContactUs(models.Model):
	name = models.CharField(max_length=10)
	email = models.EmailField()
	message_datetime = models.DateField(default = timezone.now())
	kind = models.CharField(max_length=10, choices=ContactUsKIND)
	subject = models.CharField(max_length=50)
	content = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.subject

class Reply(models.Model):
	contact_us = models.ForeignKey(ContactUs)
	message_datetime = models.DateField(default = timezone.now())
	content = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.message_datetime