# -*- coding: utf-8 -*-

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.projects.models import *
from faker import Faker
import random

class Command(BaseCommand):
    help = """Creates mock collection of projects"""

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            dest='amount',
            help='Amount of collections to generate',
        )

    def handle(self, *args, **options):
        
        available_projects = Project.objects.all()
        max_projects = 20

        if len(available_projects) == 0:
            print("No projects were found. Seed some projects before seeding a collection.")
            return

        if len(available_projects) < max_projects:
            max_projects = len(available_projects)

        # For generating between [2/3 of max_projects, max_projects]
        min_projects = max_projects - int((max_projects / 3))

        if options['amount']:
            amount = int(options['amount'])
        else:
            amount = 1

        print("Generating {} collection(s)".format(amount))

        for i in range(amount):
            
            fake = Faker()
            random.seed()

            collection = ProjectCollection()
            collection.title = fake.sentence(nb_words=2, variable_nb_words=True).strip('.')
            collection.description = fake.sentence(nb_words=10, variable_nb_words=True)
            collection.save()

            print("> {}".format(collection.title))

            projects_amount = random.randint(min_projects, max_projects)
            projects = random.sample(set(available_projects), projects_amount)

            for project in projects:

                rel = DynamicCollectionProject()
                rel.collection = collection
                rel.project = project
                rel.save()
                print(" - {}".format(project.title))

        print("Done.")
