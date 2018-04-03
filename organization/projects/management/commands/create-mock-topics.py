# -*- coding: utf-8 -*-

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.projects.models import *
from faker import Faker
import random

class Command(BaseCommand):
    help = """Creates mock project topic"""

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            dest='amount',
            help='Amount of topics to generate',
        )

    def handle(self, *args, **options):

        if options['amount']:
            amount = int(options['amount'])
        else:
            amount = 1

        failed = 0

        print("Generating {} topic(s)".format(amount))

        for i in range(amount):

            fake = Faker()

            topic = ProjectTopic()
            topic.key = fake.word()
            topic.name = topic.key.capitalize()
            # To prevent
            try:
                topic.save()
            except e:
                failed += 1

            print("> {}".format(topic.name))

        print("Done.")
        
        if failed:
            print("{} insertions silently failed".format(failed))
