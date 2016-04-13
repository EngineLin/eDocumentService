﻿# coding: utf-8
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpRequest,HttpResponse
from django.test import Client, RequestFactory, TestCase, TransactionTestCase
from account.models import Editor
from ebookSystem.models import *
from genericUser.models import User
from guest.models import Guest
from guest.views import *
from mysite import settings
import os
import shutil

class create_documentTestCase(TransactionTestCase):
	@classmethod
	def setUpClass(cls):
		super(create_documentTestCase, cls).setUpClass()
		cls.client = Client()
		cls.factory = RequestFactory()

	def test_create_document_normal(self):
		user = User(username='test-guest', is_active=True, phone='1234567890', birthday='2016-01-01')
		user.set_password('test-guest')
		user.save()
		guest = Guest(user=user)
		guest.save()
		c = self.client.login(username='test-guest', password='test-guest')
		self.assertTrue(c)
		with open('temp/uploadTestFile.zip') as fileObject:
			request = self.factory.post(reverse('guest:create_document'), {'bookname':u'遠山的回音test','author':u'Khaled Hosseini','translator':u'李靜宜','house':u'木馬文化','ISBN':u'9789865829810','date':u'2014-01-22', 'fileObject': fileObject})
		request.user = user
		response = create_document(request)
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(Book.objects.all()),1)
		self.assertEqual(len(EBook.objects.all()),4)
		book =Book.objects.first()
		self.assertTrue(os.path.exists(book.path))
		shutil.rmtree(book.path)

	def test_create_document_repeat(self):
		user = User(username='test-guest', is_active=True, phone='1234567890', birthday='2016-01-01')
		user.set_password('test-guest')
		user.save()
		guest = Guest(user=user)
		guest.save()
		c = self.client.login(username='test-guest', password='test-guest')
		self.assertTrue(c)
		with open('temp/uploadTestFile.zip') as fileObject:
			response = self.client.post(reverse('guest:create_document'), {'bookname':u'遠山的回音test','author':u'Khaled Hosseini','translator':u'李靜宜','house':u'木馬文化','ISBN':u'9789865829810','date':u'2014-01-22', 'fileObject': fileObject})
		self.assertEqual(response.context['status'],'success')
		self.assertEqual(response.context['message'],u'成功建立並上傳文件')
		with open('temp/uploadTestFile.zip') as fileObject:
			response = self.client.post(reverse('guest:create_document'), {'bookname':u'遠山的回音test','author':u'Khaled Hosseini','translator':u'李靜宜','house':u'木馬文化','ISBN':u'9789865829810','date':u'2014-01-22', 'fileObject': fileObject})
		self.assertEqual(response.context['status'],'error')
		print response.context['message']
#		self.assertEqual(response.context['message'],u'文件已存在')
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(Book.objects.all()),1)
		self.assertEqual(len(EBook.objects.all()),4)
		book =Book.objects.first()
		self.assertTrue(os.path.exists(book.path))
		shutil.rmtree(book.path)

	@classmethod
	def tearDownClass(cls):
		super(create_documentTestCase, cls).tearDownClass()

class cacheTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		super(cacheTestCase, cls).setUpClass()

	def test_cache(self):
		from django.core.cache import cache
		data = {'key1':'value1'}
		cache.set('1', data)
		response = cache.get('1')
		self.assertEqual(response, data)
		print 'cache test'

	@classmethod
	def tearDownClass(cls):
		super(cacheTestCase, cls).tearDownClass()

class profileTestCase(TransactionTestCase):
	@classmethod
	def setUpClass(cls):
		super(profileTestCase, cls).setUpClass()
		cls.client = Client()
		cls.factory = RequestFactory()

	def test_profile_normal(self):
		user = User(username='test-guest', is_active=True, phone='1234567890', birthday='2016-01-01')
		user.set_password('test-guest')
		user.save()
		guest = Guest.objects.create(user=user)
		Book.objects.create(bookname=u'藍色駭客', author=u'傑佛瑞．迪佛', translator=u'宋瑛堂', house=u'皇冠', ISBN=u'9573321564', date=u'2013-07-11', guest=guest)
		c = self.client.login(username='test-guest', password='test-guest')
		self.assertTrue(c)
		response = self.client.get(reverse('guest:profile'))
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(Book.objects.all()),1)
		self.assertEqual(len(EBook.objects.all()),10)
		response = self.client.post(reverse('guest:profile'), {'emailBook':u'9573321564'})
		self.assertEqual(response.context['status'], 'success')
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(mail.outbox), 1)

	@classmethod
	def tearDownClass(cls):
		super(profileTestCase, cls).tearDownClass()