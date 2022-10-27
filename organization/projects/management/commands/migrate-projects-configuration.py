# -*- coding: utf-8 -*-

import logging
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.projects.models import Project


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
        print(dry_run)

        for project in Project.objects.all():
            if not project.version:
                project.version = project.configuration['version']
            if not project.custom_link_url:
                project.custom_link_url = project.configuration['download_behavior']['strategies']['custom_links']['links']
            if not project.git_tag:
                project.git_tag = project.configuration['download_behavior']['strategies']['repo_release']['git_tag']
            if not project.include_sources:
                project.include_sources = project.configuration['download_behavior']['strategies']['repo_release']['include_sources']
            if not project.include_binaries:
                project.include_binaries = project.configuration['download_behavior']['strategies']['repo_release']['include_binaries']
            if not project.git_ref_archive:
                project.git_ref_archive = project.configuration['download_behavior']['strategies']['git_ref_archive']['git_ref']
            if not project.project_release_ref:
                project.project_release_ref = project.configuration['download_behavior']['strategies']['project_release']['ref']
            if not project.active_strategy:
                project.active_strategy = project.configuration['download_behavior']['active_strategy']
            if 'global_asset_meta' in project.configuration:
                if not project.is_protected:
                    project.is_protected = project.configuration['global_asset_meta']['protected']
                if not project.protection_endpoint:
                    project.protection_endpoint = project.configuration['global_asset_meta']['protection_endpoint']
                if not project.protection_unlock_url:
                    project.protection_unlock_url = project.configuration['global_asset_meta']['protection_unlock_url']

            if not dry_run:
                project.save()
                logger.logger.info(
                    'Project %s configuration migrated' \
                    % str(project.id))


