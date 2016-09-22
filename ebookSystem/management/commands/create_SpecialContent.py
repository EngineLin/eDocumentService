# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

from ebookSystem.models import EBook
import datetime

class Command(BaseCommand):
	help = 'create SpecialContent'
#	def add_arguments(self, parser):
#		parser.add_argument('reviewpart', nargs='*')

	def handle(self, *args, **options):
		for part in EBook.objects.all():
			if part.status == EBook.STATUS['finish']:
				part.create_SpecialContent()
				part.status = part.STATUS['sc_active']
				part.save()