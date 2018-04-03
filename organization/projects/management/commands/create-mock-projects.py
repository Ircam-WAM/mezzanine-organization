# -*- coding: utf-8 -*-

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.projects.models import *
from organization.core.models import LinkType
from faker import Faker
import random

class Command(BaseCommand):
    help = """Creates mock projects"""

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            dest='amount',
            help='Amount of projects to generate',
        )

    def handle(self, *args, **options):
        
        available_topics = ProjectTopic.objects.all()
        min_topics = 1
        max_topics = 6

        if len(available_topics) == 0:
            print("WARNING: No project topics were found. The generated projects won't have topics.")

        if len(available_topics) < max_topics:
            max_topics = len(available_topics)

        if options['amount']:
            amount = int(options['amount'])
        else:
            amount = 1

        print("Generating {} project(s)".format(amount))

        for i in range(amount):
            
            fake = Faker()

            project = Project()
            project.title = fake.sentence(nb_words=2, variable_nb_words=True).strip('.')
            project.description = fake.sentence(nb_words=10, variable_nb_words=True)

            project.save()

            topics = random.sample(set(available_topics), k=random.randint(1, len(available_topics)))
            project.topics = topics
            
            project.save()

            # 101 = Repository, 102 = Discussion (see app.link_types fixture)
            # TODO: generate real Github/Gitlab URLs for APIs to work /!\

            link_repo = ProjectLink(
                link_type=LinkType.objects.get(pk=101),
                url=fake.url(),
                project=project
            )
            link_repo.save()
            
            discussion_repo = ProjectLink(
                link_type=LinkType.objects.get(pk=101),
                url=fake.url(),
                project=project
            )
            discussion_repo.save()
            print("> {}".format(project.title))

        print("Done.")
