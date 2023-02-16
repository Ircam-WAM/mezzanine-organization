# -*- coding: utf-8 -*-

import logging
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.projects.models import Project, ProjectLink
from organization.core.models import LinkType


class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = """Migrates projects' properties from
            the configuration JSONField to ModelFields"""

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--dry-run',
            dest='dry-run',
            action='store_true',
            help='do not save new fields',
        )
        parser.add_argument(
            '--log-file',
            type=str,
            dest='log-file',
            required=True,
            help='log file path')

    def handle(self, *args, **kwargs):
        dry_run = kwargs['dry-run']
        log_file = kwargs['log-file']
        logger = Logger(log_file)

        if dry_run:
            print("!!! DRY-RUN !!!")

        for project in Project.objects.all():
            if not project.version:
                project.version = project.configuration['version']

            if project.external_url == "None":
                project.external_url = ""

            links = project.configuration['download_behavior']['strategies']['custom_links']['links']
            project_links = project.links.all()
            for link in links:
                url = link['url']
                if not project_links.filter(url=url):
                    link_type = LinkType.objects.get(name="Link")
                    pl = ProjectLink(project=project, url=url, link_type=link_type)
                    pl.save()

            project.custom_link_url = ""
            project.git_tag = project.configuration['download_behavior']['strategies']['repo_release']['git_tag']
            project.include_sources = project.configuration['download_behavior']['strategies']['repo_release']['include_sources']
            project.include_binaries = project.configuration['download_behavior']['strategies']['repo_release']['include_binaries']
            project.git_ref_archive = project.configuration['download_behavior']['strategies']['git_ref_archive']['git_ref']
            project.project_release_ref = project.configuration['download_behavior']['strategies']['project_release']['ref']
            project.active_strategy = project.configuration['download_behavior']['active_strategy']

            if 'global_asset_meta' in project.configuration:
                project.is_protected = project.configuration['global_asset_meta']['protected']
                project.protection_endpoint = project.configuration['global_asset_meta']['protection_endpoint']
                project.protection_unlock_url = project.configuration['global_asset_meta']['protection_unlock_url']

            i = 0
            for release in project.projectrelease_set.all().order_by('-updated'):
                # print(str(i), release.updated)
                release.release_order = i
                if not release.date_published:
                    release.date_published = release.updated
                # print(str(i), release.date_published)
                if not dry_run:
                    release.save()
                i += 1

            if not dry_run:
                project.save()
                message = 'Project %s configuration migrated' \
                    % str(project.id)
            else:
                message = 'Project %s configuration NOT migrated (dry-run)' \
                    % str(project.id)

            logger.logger.info(message)



