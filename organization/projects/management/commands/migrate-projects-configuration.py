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
            type=bool,
            help='do not save new fields',
        )
        parser.add_argument(
            '--logfile',
            type=str,
            required=True,
            help='log file path')

    def handle(self, *args, **kwargs):
        dry_run = kwargs['dry-run']
        log_file = kwargs['log-file']
        logger = Logger(log_file)

        for project in Project.objects.all():
            json_conf = project.configuration

            project.version = json_conf['version']
            project.custom_link_url = json_conf['download_behavior']['strategies']['custom_links']['links']
            project.git_tag = json_conf['download_behavior']['strategies']['repo_release']['git_tag']
            project.include_sources = json_conf['download_behavior']['strategies']['repo_release']['include_sources']
            project.include_binaries = json_conf['download_behavior']['strategies']['repo_release']['include_binaries']
            project.git_ref_archive = json_conf['download_behavior']['strategies']['git_ref_archive']['git_ref']
            project.project_release_ref = json_conf['download_behavior']['strategies']['project_release']['ref']
            project.active_strategy = json_conf['download_behavior']['active_strategy']
            project.is_protected = json_conf['global_asset_meta']['protected']
            project.protection_endpoint = json_conf['global_asset_meta']['protection_endpoint']
            project.protection_unlock_url = json_conf['global_asset_meta']['protection_unlock_url']

            if not dry_run:
                project.save()
                logger.logger.info(
                    'Project %s configuration migrated' \
                    % str(project.id))


