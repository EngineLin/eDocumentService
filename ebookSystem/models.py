﻿# coding: utf-8
from mysite import settings
from django.db import models
from django.db.models.signals import *
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import AbstractUser
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

class Editor(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	service_hours = models.IntegerField(default=0)
	professional_field = models.CharField(max_length=30, blank=True, null=True)
	is_book = models.BooleanField(default=False)

#	class Meta:
#		db_table = 'editor'

	def __unicode__(self):
		return self.user.username

class Guest(models.Model):
	user = models.OneToOneField(User, primary_key=True)

#	class Meta:
#		db_table = 'guest'

	def __unicode__(self):
		return self.user.username

class Book(models.Model):
	bookname = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	translator = models.CharField(max_length=50, blank=True, null=True)
	house = models.CharField(max_length=30)
	date = models.DateField()
	ISBN = models.CharField(max_length=20)
	path = models.CharField(max_length=255, blank=True, null=True)
	page_count = models.IntegerField(blank=True, null=True)
	part_count = models.IntegerField(blank=True, null=True)
	page_per_part = models.IntegerField(default=50)
	get_count = models.IntegerField(default=0)
	upload_date = models.DateField(default = timezone.now())
	remark = models.CharField(max_length=255, blank=True, null=True)
	def __unicode__(self):
		return self.bookname

class EBook(models.Model):
	book = models.ForeignKey(Book)
	part = models.IntegerField()
	begin_page = models.IntegerField()
	end_page = models.IntegerField()
	edited_page = models.IntegerField(default=0)
	editor = models.ForeignKey(Editor,blank=True, null=True, on_delete=models.SET_NULL)
	guest = models.ForeignKey(Guest,blank=True, null=True, on_delete=models.SET_NULL)
	is_finish = models.BooleanField(default=False)
	is_edited = models.BooleanField(default=False)
	edit_date = models.DateTimeField(blank=True, null=True)
	finish_date = models.DateField(blank=True, null=True)
	deadline = models.DateField(blank=True, null=True)
	get_date = models.DateTimeField(blank=True, null=True)
	service_hours = models.IntegerField(default=0)
	remark = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		unique_together = ('book', 'part',)

	def __unicode__(self):
		return self.book.bookname+u'-part'+str(self.part)

def pre_save_Book(**kwargs):
	book = kwargs.get('instance')
	if book.page_count == None or book.part_count == None:
		book.path = settings.PREFIX_PATH + u'static/ebookSystem/document/{0}'.format(book.bookname)
		book.page_count=0
		try:
			fileList=os.listdir(book.path+u'/source')
			for scanPage in fileList:
				if scanPage.split('.')[-1]=='jpg':
					book.page_count = book.page_count+1
		except:
			print(book.bookname+u'source not found')
		print 'set page_count and part_count'
		book.part_count = book.page_count/book.page_per_part+1

def post_save_Book(**kwargs):
	book = kwargs.get('instance')
	if len(book.ebook_set.all()) == 0:
		createEBookBatch(book)
	else:
		print 'The ebook is already exist'

pre_save.connect(pre_save_Book, Book)
post_save.connect(post_save_Book, Book)

def createEBookBatch(book):
#	if len(book.ebook_set.all()) != 0:
#		print 'The ebook is already exist'
#		return 0
	print u'create ebook batch {0}'.format(book.bookname)
	for i in range(book.part_count):
		begin_page = i*book.page_per_part
		end_page = (i+1)*book.page_per_part-1
		if end_page >= book.page_count:
			end_page = book.page_count-1
		part = EBook(book=book, part=i+1, begin_page=begin_page, end_page=end_page)
		part.save()
	return 1

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