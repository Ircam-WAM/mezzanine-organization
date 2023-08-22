# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import copy
import datetime
import logging
import os

import pydash as dsh
from django.utils.safestring import mark_safe
from django.core.files.images import get_image_dimensions
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import settings as m_settings
from mezzanine.core.models import Displayable, Orderable, RichText, Slugged, Ownable
from mezzanine.core.models import (CONTENT_STATUS_DRAFT,
                                    CONTENT_STATUS_PUBLISHED,
                                    CONTENT_STATUS_CHOICES)
from mezzanine_agenda.models import *
from organization.core.fields import JSONField
from organization.core.models import *
from organization.core.models import TitledSlugged, Period,\
    Named, Titled, Description, Block, Link, Image, UserImage, File,\
    SubTitled, NamedOnly, RelatedTitle, URL, DynamicContent, Address, LinkType, \
    OwnableOrNot
from organization.pages.models import Page
from organization.network.models import Person, Organization
from organization.magazine.models import Article
from organization.media.models import PlaylistRelated
from mezzanine_agenda.models import Event
from mezzanine.core.models import Slugged, RichText, Displayable, Orderable, MetaData,\
    TimeStamped, RichTextField, TeamOwnable
from mezzanine.conf import settings as m_settings

from django.conf import settings

logger = logging.getLogger("app")

PROJECT_TYPE_CHOICES = [
    ("internal", _("internal")),
    ("external", _("external")),
    ('tutorial', _('tutorial')),
    ("project", _("project")),
]

PROJECT_ACTIVE_STRATEGY = [
    ("git_ref_archive", _("git_ref_archive")),
    ("repo_release", _("repo_release")),
    ("custom_links", _("custom_links")),
    ("project_release", _("project_release")),
]

REPOSITORY_ACCESS_CHOICES = [
    ("public", _("public")),
    ("shared", _("shared")),
    ("private", _("private")),
]

REPOSITORY_VENDORS = [
    ("gitlab", _("Gitlab")),
    ("github", _("Github")),
]

DIMENSION_CHOICES = (
    ("startup", _("Start-up / Micro")),
    ("sme", _("SME")),
    ("large", _("Large")),
)

PROJECT_TYPE_CHOICES = [
    ('internal', ('Internal project')),
    ('external', ('National or European project')),
    ('industrial', ('Industrial project')),
]

PROJECT_STATUS_CHOICES = (
    (0, ('rejected')),
    (1, ('pending')),
    (2, ('in process')),
    (3, ('accepted')),
)

PROJECT_TOPIC_STATUS_CHOICES = (
    (0, ('rejected')),
    (1, ('pending')),
    (2, ('accepted')),
    (3, ('to be merged')),
)

FUNDING_CHOICES = (
    ("public", _("EU / National Program")),
    ("private", _("Privately Funded")),
)


class GuestContentMixin(models.Model):

    """Adds the submission fields and logic needed to handle guest content"""

    submitted = models.BooleanField(default=False)
    submitted_on = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # NOTE: permissions are assigned/removed in ircamforum.signals
        # Sets or clean the submitted date depending on the submitted status
        if self.submitted and not self.submitted_on:
            self.submitted_on = now()
        if not self.submitted:
            self.submitted_on = None
        if not self.pk:  # Draft if new object
            self.status = CONTENT_STATUS_DRAFT
        super().save(*args, **kwargs)


class Project(Displayable,
    Period,
    RichText,
    OwnableOrNot,
    GuestContentMixin):
    """(Project description)"""

    type = models.CharField(
        _("type"), max_length=128, choices=PROJECT_TYPE_CHOICES, default="project"
    )
    external_id = models.CharField(
        _("external ID"), blank=True, null=True, max_length=128
    )
    program = models.ForeignKey(
        "ProjectProgram",
        verbose_name=_("project program"),
        related_name="projects",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    program_type = models.ForeignKey(
        "ProjectProgramType",
        verbose_name=_("project program type"),
        related_name="projects",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    call = models.ForeignKey(
        "ProjectCall",
        verbose_name=_("project call"),
        related_name="projects",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    lead_team = models.ForeignKey(
        "organization_network.Team",
        verbose_name=_("lead team"),
        related_name="leader_projects",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    lead_organization = models.ForeignKey(
        "organization_network.Organization",
        verbose_name=_("lead organization"),
        related_name="leader_projects",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    teams = models.ManyToManyField(
        "organization_network.Team",
        verbose_name=_("teams"),
        related_name="partner_projects",
        blank=True,
    )
    organizations = models.ManyToManyField(
        "organization_network.Organization",
        verbose_name=_("organizations"),
        blank=True
    )
    website = models.URLField(
        _("website"),
        max_length=512,
        blank=True
    )
    topics = models.ManyToManyField(
        "ProjectTopic",
        verbose_name=_("topics"),
        related_name="%(class)ss",
        blank=True,
    )
    meta_category = models.ForeignKey("organization_core.MetaCategory",
        verbose_name=_("category"),
        related_name='%(class)ss',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    languages = models.ManyToManyField(
        "ProjectLanguage",
        verbose_name=_("languages"),
        related_name="project_languages",
        blank=True,
    )
    referring_person = models.ManyToManyField(
        "organization_network.Person",
        verbose_name=_("Referring Person"),
        related_name="projects_referring_person",
        blank=True,
    )
    manager = models.ManyToManyField(
        "organization_network.Person",
        verbose_name=_("Manager"),
        related_name="projects_manager",
        blank=True,
    )
    is_archive = models.BooleanField(
        verbose_name=_("Is Archive"),
        help_text="Hide project in Team Page",
        default=False,
    )
    is_private = models.BooleanField(
        verbose_name=_("Is private"),
        help_text="If the project is private, permissions will be enforced. Else, the project is considered public and they will be omitted.",
        default=False,
    )
    validation_status = models.IntegerField(
        _("validation status"), choices=PROJECT_STATUS_CHOICES, default=1
    )
    funding = models.CharField(
        _("funding"), choices=FUNDING_CHOICES, max_length=128, blank=True, null=True
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_("project owner"),
        related_name="owned_projects",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    version = models.CharField(_("version"), max_length=128, blank=True, null=True)
    external_url = models.URLField(
        _("external url"), max_length=1024, null=True, blank=True
    )
    external_git_repository = models.URLField(
        _("external git repository"), max_length=1024, null=True, blank=True
    )
    readme_cms_content = models.TextField(
        _("readme content from cms"), blank=True, null=True
    )
    banner_image = models.ImageField(upload_to="uploads/projects/images/", blank=True, null=True)
    banner_crop_data = models.CharField(max_length=1024, null=True, blank=True, default="")
    show_download_repo = models.BooleanField(
        verbose_name=_("show download repository"),
        help_text="Show download repository button.",
        default=False,
    )
    show_commits = models.BooleanField(
        verbose_name=_("show repository commits"),
        help_text="Show project repository commits.",
        default=True,
    )
    is_readme_in_repo = models.BooleanField(
        verbose_name=_("is readme in repository"),
        help_text="If the README is added to the repository.",
        default=True,
    )
    is_premium = models.BooleanField(
        verbose_name=_("is premium"),
        help_text="If this is a premium project.",
        default=False,
    )
    is_protected = models.BooleanField(
        verbose_name=_("is protected"),
        help_text="If this is a premium project protected by an authorization key.",
        default=False,
    )
    protection_endpoint = models.CharField(
        _("protection endpoint"), max_length=1024, blank=True, null=True
    )
    protection_unlock_url = models.CharField(
        _("protection unlock url"), max_length=1024, blank=True, null=True
    )
    active_strategy = models.CharField(
        _("active strategy"),
        max_length=128,
        choices=PROJECT_ACTIVE_STRATEGY,
        default="project_release",
    )
    git_ref_archive = models.CharField(
        _("git ref archive"), max_length=128, default="master"
    )
    # repository_release = models.CharField(_('repository release'), max_length=128, default='master')
    git_tag = models.CharField(_("git tag"), max_length=128, blank=True, null=True)
    include_sources = models.BooleanField(
        verbose_name=_("include sources"), default=True
    )
    include_binaries = models.BooleanField(
        verbose_name=_("include binaries"), default=True
    )
    custom_link_url = models.CharField(
        _("custom link url"), max_length=1024, blank=True, null=True
    )
    project_release_ref = models.CharField(
        _("project release ref"),
        blank=True,
        null=True,
        max_length=128,
        default="latest",
    )

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        # ordering = ['-date_from', '-date_to']
        ordering = ["title",]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization-project-detail", kwargs={"slug": self.slug})

    def project_status(self):
        if self.date_from and self.date_to:
            if datetime.date.today() >= self.date_from and\
                    datetime.date.today() <= self.date_to:
                return ('in progress')
            elif datetime.date.today() < self.date_from and\
                    datetime.date.today() < self.date_to:
                return ('pending')
            elif datetime.date.today() > self.date_to and\
                    datetime.date.today() > self.date_to:
                return ('completed')
        else:
            return ('pending')

    @property
    def download_urls(self):

        """
        /! OBSOLETE !\
        Now handled by ircamforum.templatetags.project_download_links
        Also it should return ProjectLinks, not primitives!
        SMELL: make it return ProjectLink, but for that rewrite get_links and dependencies
        """

        ret = []  # TODO: must set a schema for simple, clear format in the templates
        #       example: { version, platform, url, featured } or even more abstract

        direct_urls = self.get_links(
            "download"
        )  # First we try to get the "download" link type

        if len(direct_urls) > 0:
            for direct_url in direct_urls:
                ret.insert(
                    0,
                    {
                        "url": direct_url.url,
                        "title": direct_url.title,
                        #'featured': True
                    },
                )
        else:
            # If no 'download' link is found, fallback to the latest tag from the first repository
            # TODO: what about multiple repositories?
            for i, pr in enumerate(self.project_repositories.all()):
                if pr.repository.api:
                    ret.append(
                        {
                            "url": pr.repository.api.get_archive_url(),
                            "title": "Repository files",
                            "subtitle": "Branch `master` — ZIP archive",
                            #'featured': (not direct_url and i == 0)  # Only the first repository URL is featured,
                            # if and only if no direct link has been set up
                        }
                    )
        return ret

    @property
    def purchase_urls(self):

        ret = []
        direct_urls = self.get_links("purchase")

        if len(direct_urls) > 0:
            for direct_url in direct_urls:
                ret.insert(
                    0,
                    {
                        "url": direct_url.url,
                        "title": direct_url.title,
                        #'featured': True
                    },
                )

        return ret

    @property
    def documentation_url(self):
        links = self.get_links("documentation")
        return links.first()

    @property
    def repositories(self):
        return self.get_repositories()

    @property
    def discussion_rooms(self):
        return self.get_discussion_rooms()

    @property
    def contributors(self):
        def strip_emails(item):
            item.pop("email")
            return item

        def strip_owner(contributors):
            try:
                from ircamforum import utils  # SMELL
            except ImportError:
                return contributors
            else:
                owner_oauth_id = utils.get_oauth_id(user=self.owner)
                contributors = dsh.filter_(
                    contributors, lambda c: c["oauth_id"] != owner_oauth_id
                )
                return contributors

        contributors = self.get_contributors()
        contributors = list(map(strip_emails, contributors))
        contributors = strip_owner(contributors)
        return contributors

    def get_links(self, link_type_slug=None):
        link_type = LinkType.objects.get(slug=link_type_slug)
        urls = self.links.filter(link_type=link_type)
        return urls

    def get_discussion_rooms(self):
        from discussion import discussion as d

        s = {}
        s.update(settings.DISCUSSION)

        # Editable setting
        s.update({"LATEST_POSTS_LIMIT": m_settings.DISCUSSION_LATEST_POSTS_LIMIT})

        discussion_rooms = []
        for project_link in self.get_links(link_type_slug="discussion"):
            tmp = {}
            tmp["url"] = project_link.url
            tmp["summary"] = d.Discussion(
                project_link.url,
                "discourse",  # SMELL: should be detected or specified in project_link,
                #        not hardcoded
                settings=s,
                debug=settings.DEBUG,
            ).get_summary()
            discussion_rooms.append(tmp)

        return discussion_rooms

    def get_repositories(self):

        repositories = []

        for project_repository in self.project_repositories.all():
            tmp = {}
            repository = project_repository.repository
            if repository.api:
                tmp["readme"] = {}
                _, tmp["readme"]["html"] = repository.api.get_readme()
                tmp["summary"] = repository.api.get_summary()
                tmp["url"] = repository.url if not repository.api.private else None
                repositories.append(tmp)

        return repositories

    def get_contributors(self):

        # NOTE: will need a bigass cache because it fetch resources from everywhere

        # Project contributors are sourced from:
        # - Repositories (commits authors and members)
        # - Discussion rooms (participants)
        # - Forum project members

        from django.urls import reverse
        from discussion import discussion as d
        from ircamforum import (
            utils,
        )  # SMELL: makes the method forum-specific, move logic elsewhere?

        CONTRIBUTORS_SOURCES = [
            "repository_commits_contributors",
            "repository_members",
            "repository_issues_contributors",
            "forum_project_members",
            "discussion_participants",
        ]

        # Not actually enforced. For info only.
        CONTRIBUTOR_SCHEMA = {
            "display_name": None,  # Mandatory.
            "email": None,  # Mandatory. Be careful to not show it in public (like your mom taught you).
            "avatar_url": None,  # Optional. Getting it from Ircam OAuth server if email matches
            "source": None,  # Mandatory. One of CONTRIBUTORS_SOURCES
            "extra_data": {},  # Optional
        }

        contributors = []  # Holds all the contributors from all the sources

        # Getting each source
        for source in CONTRIBUTORS_SOURCES:

            # Commits and issues contributors
            if source in [
                "repository_commits_contributors",
                "repository_issues_contributors",
                "repository_members",
            ]:

                # For each project repository...
                for project_repository in self.project_repositories.all():

                    repository_contributors = []
                    repository = project_repository.repository

                    if repository.api:

                        if source == "repository_commits_contributors":
                            try:
                                repository_contributors = (
                                    repository.api.get_commits_contributors()
                                )
                            except Exception:
                                repository_contributors = []
                        elif source == "repository_issues_contributors":
                            try:
                                repository_contributors = (
                                    repository.api.get_issues_contributors()
                                )
                            except Exception:
                                repository_contributors = []
                        elif source == "repository_members":
                            try:
                                repository_contributors = repository.api.get_members()
                            except Exception:
                                repository_contributors = []

                        # Augmenting the contributors data with source
                        for c in repository_contributors:

                            tmp = copy.copy(c)
                            tmp[
                                "source"
                            ] = source  # IDEA: also include which repository, in case of multiple repositories

                            if c["email"]:

                                tmp["oauth_id"] = utils.get_oauth_id(email=c["email"])

                                if tmp["oauth_id"]:

                                    u = utils.get_user_by_oauth_id(tmp["oauth_id"])

                                    # Consumed by the API client, so we cannot build to URL with Django
                                    # in the template, we must give the client the full URLs
                                    tmp["profile_url"] = reverse(
                                        "ircam-forum-profile",
                                        kwargs={"username": u.username},
                                    )
                                    tmp["avatar_url"] = u.forum_user.avatar_url

                                    # TODO: build display_name from the OAuth profile ?
                            else:
                                tmp["oauth_id"] = None

                            contributors.append(tmp)

        # NOTE: there may be duplicates, leaving the function caller the care to deduplicate it
        # (duplicates can be used to determine a count, e.g. user posted X issues, etc.)
        # If deduplicating it, the OAuth ID is the only really unique value to be trusted

        return contributors

    @property
    def language_group(self):

        # TODO: cache the API endpoint instead when possible
        cache_key = "project_{}_language_group".format(self.pk)
        cached = cache.get(cache_key)

        if not cached:
            # WARNING: only implemented for one repository (the first)
            repository = self.main_repository

            group = None

            if repository and repository.api:
                languages = repository.api.get_languages()
                if len(languages) > 0:
                    languages_sorted = sorted(
                        languages.items(), key=lambda t: (t[1], t[0]), reverse=True
                    )
                    main_language = languages_sorted[0]  # -> (name, %)
                    main_language = main_language[0]  # -> name

                    for (key, value) in settings.REPOSITORY["LANGUAGES"][
                        "GROUPS"
                    ].items():
                        if main_language.lower() in value:
                            group = key

            ret = group or "unknown"
            cache.set(cache_key, ret, settings.CACHE_PROJECT_LANGUAGE_GROUP)

        else:
            ret = cached

        return ret

    @property
    def main_repository(self):
        # Later we might want to allow multiple repositories
        # but there will always be a "main" one
        if len(self.project_repositories.all()) < 1:
            repository = None
        else:
            repository = self.project_repositories.first().repository
        return repository


class ProjectTopic(Named, Dated, GuestContentMixin, Ownable):

    parent = models.ForeignKey(
        'ProjectTopic',
        verbose_name=_('parent topic'),
        related_name='topics',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    key = models.CharField(
        _('key'),
        unique=True,
        max_length=128
    )

    status = models.IntegerField(
        _("Status"),
        choices=PROJECT_TOPIC_STATUS_CHOICES,
        default=1,
    )

    is_faceted = models.BooleanField(
        default=False,
        help_text="wether this topic is displayed as a filter in the search facets list"
        )

    is_featured = models.BooleanField(
        default=False,
        help_text="wether this topic is featured for external applications"
        )

    score = models.IntegerField(
        _("Score"),
        default=1,
    )

    class Meta:
        verbose_name = _("topic")
        ordering = ["key",]

    def get_absolute_url(self):
        return reverse(
            'ircam-forum-projecttopic-detail',
            kwargs={'pk': self.pk, 'name': self.name}
        )


    def get_absolute_url(self):
        return reverse(
            "ircam-forum-projecttopic-detail", kwargs={"pk": self.pk, "name": self.name}
            )

    def __str__(self):
        if self.parent:
            return " - ".join((self.parent.name, self.name))
        else:
            return self.name

    def save(self, *args, **kwargs):
        if self.status == 3 and self.parent:
            objs = [self.projects.all(),
                    self.collections.all(),
                    self.forumarticles.all(),
                    self.events.all(),
                    ]
            for qs in objs:
                for obj in qs:
                    obj.topics.remove(self)
                    obj.topics.add(self.parent)
            self.status = 0
        super(ProjectTopic, self).save(args, kwargs)
        if self.status == 0:
            self.delete()


class ProjectProgram(Named):
    class Meta:
        verbose_name = _("program")
        verbose_name_plural = _("programs")
        ordering = ['name', ]


class ProjectProgramType(Named):
    class Meta:
        verbose_name = _("program type")
        verbose_name_plural = _("program types")
        ordering = ['name', ]


class ProjectWorkPackage(Titled, Description, Period):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='work_packages',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    number = models.IntegerField(_('number'))
    lead_organization = models.ForeignKey(
        'organization_network.Organization',
        verbose_name=_('lead organization'),
        related_name='leader_work_packages',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("work package")
        verbose_name_plural = _("work packages")
        ordering = ['number', ]


class ProjectPlaylist(PlaylistRelated):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='playlists',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectLink(Link):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='links',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectImage(Image):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectUserImage(UserImage):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='user_images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectFile(File):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='files',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectBlock(Block):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectTopicPage(Page, SubTitled):

    project_topic = models.ForeignKey(
        'ProjectTopic',
        verbose_name=_('project topic'),
        related_name="pages",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    display_navbar = models.BooleanField(default=True)
    displayed_in_navbars = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("project topic page")
        verbose_name_plural = _("project topic pages")


class ProjectCall(Displayable, Period, RichText, NamedOnly):

    project_form_content = RichTextField(
        _("Project form content"),
        blank=True,
        null=True
    )
    residency_form_content = RichTextField(
        _("Residency form content"),
        blank=True,
        null=True
    )
    producer_form_content = RichTextField(
        _("Producer form content"),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _("project call")
        verbose_name_plural = _("project calls")
        ordering = ['title', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization-call-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.name and self.title:
            self.name = self.title
        if not self.title and self.name:
            self.title = self.name
        super(ProjectCall, self).save(args, kwargs)

    @property
    def is_closed(self):
        """Return if the current date between 'from' and 'to' dates."""
        try:
            current_date = datetime.date.today()
            if current_date >= self.date_from and current_date <= self.date_to:
                return False
        except Exception:
            pass
        return True


class ProjectCallBlock(Block):

    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=_('project call'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectCallImage(Image):

    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=_('project call'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectCallFile(File):

    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=_('project call'),
        related_name='files',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectCallLink(Link):

    call = models.ForeignKey(
        'ProjectCall',
        verbose_name=_('project call'),
        related_name='links',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectDemo(Displayable, RichText, URL):

    project = models.ForeignKey(
        'Project',
        verbose_name=_('project'),
        related_name='demos',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    authors = models.ManyToManyField(
        Person,
        verbose_name=_('authors'),
        related_name='demos',
        blank=True
    )
    repository = models.ForeignKey(
        'Repository',
        verbose_name=_('repository'),
        related_name='demos',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    build_commands = models.TextField(
        _('build commands'),
        blank=True
    )
    directory = models.CharField(
        _('directory'),
        max_length=256,
        blank=True,
        null=True,
        help_text='Relative directory in repository'
    )

    class Meta:
        verbose_name = _("project demo")
        verbose_name_plural = _("project demos")

    def get_absolute_url(self):
        return reverse("organization-project-demo-detail", kwargs={"slug": self.slug})

    @property
    def relative_url(self):
        path = self.repository.directory.replace(settings.MEDIA_ROOT, "")
        return settings.MEDIA_URL + path + os.sep + self.directory + "/index.html"

    def build(self):
        os.chdir(self.repository.directory)
        for command in self.build_commands.split("\n"):
            os.system(command)

    def save(self, *args, **kwargs):
        super(ProjectDemo, self).save(args, kwargs)
        if self.repository:
            self.build()


class Repository(models.Model):

    system = models.ForeignKey(
        'RepositorySystem',
        verbose_name=_('system'),
        related_name='repositories',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    access = models.CharField(
        _('access rights'),
        max_length=64,
        choices=REPOSITORY_ACCESS_CHOICES,
        default='public'
    )
    branch = models.CharField(
        _('branch'),
        max_length=32,
        default='master'
    )
    url = models.CharField(
        _('URL'),
        max_length=256,
        help_text='http(s) or ssh'
    )
    vendor = models.CharField(
        _('vendor'),
        max_length=64,
        choices=REPOSITORY_VENDORS,
        default='gitlab'
    )

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = _("repository")
        verbose_name_plural = _("repositories")

    @property
    def api(self):

        s = {}
        s.update(settings.REPOSITORY)

        # Those are editable settings -> picking them from the Mezzanine helper
        s.update({"LATEST_COMMITS_LIMIT": m_settings.REPOSITORY_LATEST_COMMITS_LIMIT})
        s.update({"LATEST_TAGS_LIMIT": m_settings.REPOSITORY_LATEST_TAGS_LIMIT})

        try:
            from repository import repository as r
        except ImportError:
            logger.warning("Couldn't import repository module")
            instance = None
        else:
            import re

            url = self.url

            # Injecting the custom API key if the repo URL matches the regex
            for host in settings.REPOSITORY_HOSTS:
                if re.search(host["regex"], url) is not None:
                    s.update(host["credentials"])

            try:
                instance = r.Repository(
                    url, self.vendor, settings=s, debug=settings.DEBUG
                )
            except Exception as e:
                # Must be fail-safe to allow "if repo.api" form of check in the code
                logger.warning("unable to reach repo %s: %s", url, e)
                instance = None

        return instance


class RepositorySystem(Named):
    class Meta:
        verbose_name = _("repository system")
        verbose_name_plural = _("repository systems")


class ProjectRepository(models.Model):

    project = models.ForeignKey(
        Project,
        verbose_name=_("project"),
        related_name="project_repositories",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    repository = models.ForeignKey(
        Repository,
        verbose_name=_("repository"),
        related_name="project_repositories",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.repository.url

    class Meta:
        verbose_name = _("project repository")
        verbose_name_plural = _("project repositories")


class ProjectRelatedTitle(RelatedTitle):

    project = models.OneToOneField(
        Project,
        verbose_name=_('project'),
        related_name='related_title',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("related title")
        order_with_respect_to = "project"


class DynamicContentProject(DynamicContent, Orderable):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='dynamic_content_project',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Linked Project"


class DynamicMultimediaProject(DynamicContent, Orderable):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='dynamic_multimedia',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Multimedia'


class ProjectBlogPage(Displayable, RichText):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='blog_pages',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    login_required_content = RichTextField(_("Login required content"), null=True)

    class Meta:
        verbose_name = "Project blog page"
        verbose_name_plural = "Project blog pages"

    def get_absolute_url(self):
        return reverse(
            "organization-project-blogpage-detail",
            kwargs={"slug": self.slug}
        )


class ProjectPublicData(models.Model):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='public_data',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    brief_description = models.CharField(
        _('brief description'),
        max_length=110,
        help_text="Brief description of the technology/challenges"
        " faced by the project (110 characters max)."
    )
    challenges_description = models.TextField(
        _('challenges description'),
        help_text="Description of the project technology to be made"
        " available to artist + challenges it produces (100 words - must include"
        " the elements to be made available to the artist with sufficient functional"
        " and implementation details for enabling him/her to "
        "elaborate a technical approach)."
    )
    technology_description = models.TextField(
        _('technology description'),
        help_text="Must include the elements to be made available to the artist with"
        " sufficient functional and implementation details for enabling him/her to"
        " elaborate his/her technical approach (100-200 words)."
    )
    objectives_description = models.TextField(
        _('objectives description'),
        help_text="What the project is looking to gain from the collaboration"
        " and what kind of artist would be suitable (100 – 150 words)."
    )
    resources_description = models.TextField(
        _('resource description'),
        help_text="Resources available to the artist -- e.g. office facility, studio"
        " facility, technical equipment, internet connection, laboratory, and periods"
        " of availability for artistic production, staff possibly allocated to the"
        " project, available budget for travel, consumables and "
        "equipment, etc... (50 – 100 words)."
    )
    implementation_start_date = models.DateField(
        _('residency start date'),
        help_text="Possible period for the implementation of the residency"
        " (must be within the period of the project implementation workplan)"
        " (MM/DD/YYYY)"
    )
    implementation_period = models.DateField(
        _('period for direct cooperation'),
        blank=False,
        null=True,
        help_text="Possible period for direct cooperation with the"
        " artist (must be within the period of the project "
        "implementation workplan) (MM/DD/YYYY)"
    )
    implementation_duration = models.CharField(
        _('residency duration'),
        max_length=128, help_text="Possible duration of implementation in"
        " months (must be part of the project implementation workplan) (months)"
    )
    image = models.FileField(
        _("Image"),
        max_length=1024,
        upload_to="user/images/%Y/%m/%d/",
        help_text="Representing the project"
    )
    image_credits = models.CharField(
        _('Image credits'),
        max_length=256,
        null=True
    )

    class Meta:
        verbose_name = "Project public data"
        verbose_name_plural = "Project public data"

    @property
    def image_is_panoramic(self):
        """Return True if the image has a 3:2 ratio or bigger."""
        try:
            img_width, img_height = get_image_dimensions(self.image.file)
            # Images go in a 427x286 box -> 3:2 ratio
            if (img_width / img_height) >= 1.5:
                panoramic = True
            else:
                panoramic = False
        except Exception:
            panoramic = True
        return panoramic


class ProjectPrivateData(models.Model):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='private_data',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    description = models.TextField(
        _('project description'),
        help_text="(500 - 1000 words)"
    )
    funding_programme = models.CharField(
        _('funding programme'),
        max_length=512,
        blank=False,
        null=True,
        help_text="Designation of EU/National Funding Programme"
    )
    commitment_letter = models.FileField(
        _("letter of commitment by the project coordinator"),
        max_length=1024,
        upload_to="user/documents/%Y/%m/%d/",
        help_text=mark_safe(
            'Written on behalf of the whole project consortium'
            ', this letter will commit in implementing the collaboration'
            ' of a residency application selected by the VERTIGO jury, on'
            ' the conditions set by the project (in annex of letter: synthesis'
            ' of all related information entered by project).<br>Please '
            '<a href="http://vertigo.starts.eu/media/uploads/vertigo%20starts/CALL/vertigo_loc_v3.rtf">'  # noqa: E501
            'download and use the template letter.</a>'
        )
    )
    investor_letter = models.FileField(
        _("letter of recommendations from investor (e.g VC)"),
        max_length=1024,
        blank=False,
        null=True,
        upload_to="user/documents/%Y/%m/%d/",
        help_text="If the organisation is a Start-Up or micro enterprise"
        " (less than 3 years and/or less than 10 staff members), the presentation"
        " of letter of recommendation from an investor is mandatory"
        " to apply to this call."
    )
    persons = models.CharField(
        _('persons'),
        max_length=512,
        help_text="First name and last name of the persons from organization /"
        " project who will be part preliminary of the project team"
        " (separated by a comma)"
    )
    dimension = models.CharField(
        _('dimension'),
        max_length=128,
        choices=DIMENSION_CHOICES,
        blank=False,
        null=True
    )

    class Meta:
        verbose_name = "Project private data"
        verbose_name_plural = "Project private data"


class ProjectContact(Person):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='contacts',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    organization_name = models.CharField(
        _('organization name'),
        blank=True,
        null=True,
        max_length=128
    )
    position = models.CharField(_('position'), blank=True, null=True, max_length=128)

    class Meta:
        verbose_name = "Project contact"
        verbose_name_plural = "Project contacts"


class ProjectResidency(Displayable, Period, Address, RichText):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    artist = models.ForeignKey(
        Person,
        verbose_name=_('artist'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    validated = models.BooleanField(default=False)
    producer_commitment = models.TextField(_('producer commitment'), help_text="")

    @property
    def articles(self):
        # TODO: Any way to avoid magic number in status filter?
        articles = Article.objects.filter(residencies__residency=self)\
            .filter(status=2)\
            .filter(publish_date__lte=datetime.date.today())\
            .order_by("-publish_date")
        return articles

    @property
    def events(self):
        # TODO: Any way to avoid magic number in status filter?
        events = Event.objects.filter(residencies__residency=self)\
            .filter(status=2)\
            .filter(publish_date__lte=datetime.date.today())\
            .order_by("-publish_date")
        return events

    class Meta:
        verbose_name = "Project residency"
        verbose_name_plural = "Project residencies"

    def get_absolute_url(self):
        call_slug = ''
        if self.project:
            if self.project.call:
                call_slug = self.project.call.slug
        return reverse(
            "organization-residency-detail",
            kwargs={"call_slug": call_slug, "slug": self.slug}
        )


class ProjectResidencyProducer(models.Model):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('residency'),
        related_name='producers',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('producer'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyFile(File):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('project residency file'),
        related_name='files',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyImage(Image):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('project residency image'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyUserImage(UserImage):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('project residency user image'),
        related_name='user_images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyArticle(models.Model):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('residency'),
        related_name='residency_articles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    article = models.ForeignKey(
        Article,
        verbose_name=_('article'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectResidencyEvent(models.Model):

    residency = models.ForeignKey(
        ProjectResidency,
        verbose_name=_('residency'),
        related_name='residency_events',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    event = models.ForeignKey(
        Event,
        verbose_name=_('event'),
        related_name='residencies',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectCollection(Displayable):
    def get_absolute_url(self):
        return reverse(
            "organization-project-collection-detail", kwargs={"slug": self.slug}
        )


class ProjectCollectionImage(Image):

    collection = models.ForeignKey(
        ProjectCollection,
        verbose_name=_("collection"),
        related_name="images",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )


class Pivot_Project_ProjectCollection(DynamicContent, Orderable):

    project = models.ForeignKey(
        Project,
        verbose_name=_("project"),
        related_name="collections_pivot",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    collection = models.ForeignKey(
        ProjectCollection,
        verbose_name=_("collection"),
        related_name="projects_pivot",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Dynamic Collection Project"


class Pivot_ProjectTopic_Article(DynamicContent, Orderable):

    project_topic = models.ForeignKey(
        ProjectTopic,
        verbose_name=_("project topic"),
        related_name="articles_pivot",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Article,
        verbose_name=_("article"),
        related_name="project_topics_pivot",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.project_topic.__str__()

    class Meta:
        verbose_name = 'Project Topic'

class ProjectPage(Displayable, RichText, TeamOwnable):

    project = models.ForeignKey(
        Project,
        verbose_name=_('project'),
        related_name='pages',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    display_navbar = models.BooleanField(default=True)
    displayed_in_navbars = models.BooleanField(default=True)

    @property
    def is_archive(self):
        if self.project:
            return self.project.is_archive

    def get_absolute_url(self):
        return reverse(
            "organization-project-projectpage-detail",
            kwargs={'slug': self.slug}
        )

    class Meta:
        permissions = TeamOwnable.Meta.permissions


class ProjectPageImage(Image):

    project_page = models.ForeignKey(
        ProjectPage,
        verbose_name=_('project page'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProjectPageBlock(Block):

    project_page = models.ForeignKey(
        ProjectPage,
        verbose_name=_('project page'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class DynamicContentProjectPage(DynamicContent, Orderable):

    project_page = models.ForeignKey(
        ProjectPage,
        verbose_name=_('project page'),
        related_name='dynamic_content_project_pages',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Dynamic Content Project Page'


class ProjectLanguage(Named):
    class Meta:
        verbose_name = 'Language'

