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

from django import forms
from django.apps import apps
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from mezzanine.core.fields import RichTextField, FileField
from mezzanine.core.managers import SearchableManager
from mezzanine.core.models import RichText, SiteRelated, Orderable, MetaData, \
    TimeStamped, TeamOwnable
from mezzanine.pages.models import Page
from mezzanine.utils.models import AdminThumbMixin
from organization.core.models import NamedSlugged, Description, Address, URL,\
    AdminThumbRelatedMixin, TitledSlugged, RelatedTitle, DynamicContent,\
    Titled, Link, Image, File, Block, Named, UserImage, SubTitled, Period,\
    Label, Dated
from organization.media.models import Media, PlaylistRelated
from organization.network.validators import validate_positive, is_percent
from organization.pages.models import CustomPage

# Hack to have these strings translated
mr = _('Mr')
mrs = _('Ms')

GENDER_CHOICES = [
    ('male', _('male')),
    ('female', _('female')),
]

PERSON_LIST_STYLE_CHOICES = [
    ('square', _('square')),
    ('circle', _('circle')),
]

TITLE_CHOICES = [
    ('Dr', _('Dr')),
    ('Prof', _('Prof')),
    ('Prof Dr', _('Prof Dr')),
]

PATTERN_CHOICES = [
    ('pattern-bg--circles', _('circles')),
    ('pattern-bg--squares', _('squares')),
    ('pattern-bg--stripes', _('stripes')),
    ('pattern-bg--triangles', _('triangles')),
]

MONTH_CHOICES = [
    (1, _('January')),
    (2, _('February')),
    (3, _('March')),
    (4, _('April')),
    (5, _('May')),
    (6, _('June')),
    (7, _('July')),
    (8, _('August')),
    (9, _('September')),
    (10, _('October')),
    (11, _('November')),
    (12, _('December')),
]

ALIGNMENT_CHOICES = (('left', _('left')), ('left', _('left')), ('right', _('right')))

CSS_COLOR_CHOICES = [
    ('orange', _('orange')),
    ('blue', _('blue')),
    ('green', _('green')),
]

CSS_BANNER_CHOICES = [
    ('fsxxl', 'fsxxl'),
    ('fsxxxl', 'fsxxxl'),
]

BOX_SIZE_CHOICES = [
    (3, 3),
    (6, 6),
]

ORGANIZATION_STATUS_CHOICES = (
    (0, _('rejected')),
    (1, _('pending')),
    (2, _('in process')),
    (3, _('accepted')),
)


class Organization(
    NamedSlugged,
    Description,
    Address,
    URL,
    AdminThumbRelatedMixin,
    Orderable
):
    """(Organization description)"""

    type = models.ForeignKey(
        'OrganizationType',
        verbose_name=_('organization type'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    role = models.ForeignKey(
        'OrganizationRole',
        verbose_name=_('organization role'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    email = models.EmailField(_('email'), blank=True, null=True)
    initials = models.CharField(_('initials'), max_length=128, blank=True, null=True)
    is_on_map = models.BooleanField(_('is on map'), default=False, blank=True)
    is_host = models.BooleanField(_('is host'), default=False, blank=True)
    is_main = models.BooleanField(_('is main'), default=False, blank=True)
    telephone = models.CharField(_('telephone'), max_length=64, blank=True, null=True)
    opening_times = models.TextField(_('opening times'), blank=True)
    subway_access = models.TextField(_('subway access'), blank=True)
    bio = models.TextField(_('bio'), blank=True)
    admin_thumb_type = 'logo'
    validation_status = models.IntegerField(
        _('validation status'),
        choices=ORGANIZATION_STATUS_CHOICES,
        default=1
    )
    hal_id = models.CharField(_('HAL id'), max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = _('organization')
        ordering = ['name', ]

    def save(self, **kwargs):
        self.clean()
        super(Organization, self).save()

    def get_absolute_url(self):
        role, c = OrganizationRole.objects.get_or_create(key='Producer')
        if self.role == role:
            return reverse("organization-producer-detail", kwargs={"slug": self.slug})
        # TODO: Default organization view?
        return reverse("network")


class Person(
    TitledSlugged,
    MetaData,
    TimeStamped,
    AdminThumbMixin,
    Address,
    TeamOwnable
):
    """(Person description)"""

    objects = SearchableManager()
    search_fields = {"title": 5}

    user = models.OneToOneField(
        User,
        verbose_name=_('user'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    person_title = models.CharField(
        _('title'),
        max_length=16,
        choices=TITLE_CHOICES,
        blank=True
    )
    gender = models.CharField(
        _('gender'),
        max_length=16,
        choices=GENDER_CHOICES,
        blank=True
    )
    first_name = models.CharField(
        _('first name'),
        max_length=255,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=255,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('email'),
        blank=True,
        null=True
    )
    telephone = models.CharField(
        _('telephone'),
        max_length=64,
        blank=True,
        null=True
    )
    register_id = models.CharField(
        _('register ID'),
        blank=True,
        null=True,
        max_length=128
    )
    birthday = models.DateField(
        _('birthday'),
        blank=True,
        null=True
    )
    bio = RichTextField(
        _('biography'),
        blank=True
    )
    role = models.CharField(
        _('role'),
        max_length=256,
        blank=True,
        null=True
    )
    external_id = models.CharField(
        _('external ID'),
        blank=True,
        null=True,
        max_length=128
    )
    hal_url = models.URLField(
        _('HAL url'),
        max_length=512,
        blank=True
    )
    karma = models.IntegerField(
        default=0,
        editable=False
    )
    search_fields = {"title": 1}
    is_referenced = models.BooleanField(
        _('Is Referenced'),
        default=True,
        help_text=_("Determine if the Person has to be referenced on search")
    )

    class Meta:
        verbose_name = _('person')
        ordering = ['last_name', ]
        permissions = TeamOwnable.Meta.permissions

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization_network-person-detail", kwargs={'slug': self.slug})

    def set_names(self):
        names = self.title.split(' ')
        if len(names) == 1:
            self.first_name = ''
            self.last_name = names[0]
        elif len(names) == 2:
            self.first_name = names[0]
            self.last_name = names[1]
        else:
            self.first_name = names[0]
            self.last_name = ' '.join(names[1:])

    def save(self, *args, **kwargs):
        self.clean()
        if self.id and not self.user:
            old = Person.objects.get(id=self.id)
            self.user = old.user
        if self.first_name and self.last_name and (not self.title or self.title == '-'):
            self.title = self.first_name + ' ' + self.last_name
        super(Person, self).save(*args, **kwargs)
        for activity in self.activities.all():
            update_activity(activity)


class PersonRelatedTitle(RelatedTitle):
    person = models.OneToOneField(
        "Person",
        verbose_name=_('person'),
        related_name='related_title',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("related title")


class DynamicContentPerson(DynamicContent, Orderable):
    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        related_name='dynamic_content_person',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Dynamic Content Person'


class OrganizationLinkedBlockInline(Titled, Description, Orderable):
    organization_linked = models.ForeignKey(
        'OrganizationLinked',
        verbose_name=_('organization list'),
        related_name='organization_linked_block_inline_list',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    organization_main = models.ForeignKey(
        'Organization',
        verbose_name=_('organization'),
        related_name='organization_linked_block',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class OrganizationLinked(Titled, Description):
    class Meta:
        verbose_name = _('Organization Linked')

    def __str__(self):
        return self.title


class OrganizationLinkedInline(Titled, Description, Orderable):
    organization_list = models.ForeignKey(
        'OrganizationLinked',
        verbose_name=_('organization linked'),
        related_name='organization_linked_inline_linked',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    organization = models.ForeignKey(
        'Organization',
        verbose_name=_('organization'),
        related_name='organization_linked_inline_from',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class OrganizationPlaylist(PlaylistRelated):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='playlists',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class DynamicMultimediaOrganization(DynamicContent, Orderable):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='dynamic_multimedia',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Multimedia'


class DynamicMultimediaPerson(DynamicContent, Orderable):
    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        related_name='dynamic_multimedia',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Multimedia'


class OrganizationLink(Link):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='links',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class OrganizationImage(Image):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='images', blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class OrganizationBlock(Block):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class OrganizationService(Named, URL, Orderable):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='services',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    image = FileField(
        _("Image"),
        max_length=1024,
        format="Image",
        upload_to="images"
    )
    css_color = models.CharField(
        _('css color'),
        max_length=64,
        blank=True,
        null=True,
        choices=CSS_COLOR_CHOICES
    )
    css_banner_type = models.CharField(
        _('css banner type'),
        max_length=64,
        blank=True,
        null=True,
        choices=CSS_BANNER_CHOICES
    )
    box_size = models.IntegerField(_('box size'), default=3, choices=BOX_SIZE_CHOICES)


class OrganizationType(Named):
    """Type of Organizations"""

    css_class = models.CharField(_('class css'), max_length=64, blank=True, null=True,
                                 help_text="Determine color on map.")

    class Meta:
        verbose_name = _('organization type')
        ordering = ['name', ]


class OrganizationEventLocation(models.Model):
    organization = models.ForeignKey(
        'organization_network.Organization',
        verbose_name=_('Organization'),
        related_name='event_locations',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    event_location = models.ForeignKey(
        'mezzanine_agenda.EventLocation',
        verbose_name=_('Event location'),
        related_name='organizations',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Organization'


class OrganizationRole(Named):
    """Roles of Organizations"""

    key = models.CharField(
        _('key'),
        blank=False,
        null=False,
        unique=True,
        max_length=128,
        default="unknown"
    )

    class Meta:
        verbose_name = _('organization role')
        ordering = ['key', ]

    def __str__(self):
        return self.key


class OrganizationContact(Person):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='contacts',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Organization contact'
        verbose_name_plural = 'Organization contacts'


class OrganizationUserImage(UserImage):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='user_images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class Department(Named):
    """(Department description)"""

    organization = models.ForeignKey(
        'Organization',
        verbose_name=_('organization'),
        related_name="departments",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _('department')
        ordering = ['name', ]

    def __str__(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        return self.name


class DepartmentPage(Page, SubTitled, RichText):
    """(Department description)"""

    department = models.ForeignKey(
        'Department',
        verbose_name=_('department'),
        related_name="pages",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    weaving_css_class = models.CharField(
        _('background pattern'),
        choices=PATTERN_CHOICES,
        max_length=64,
        blank=True
    )
    display_navbar = models.BooleanField(default=True)
    displayed_in_navbars = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('department page')


class Team(NamedSlugged, Description, TeamOwnable):
    """(Team description)"""

    organization = models.ForeignKey(
        'Organization',
        verbose_name=_('organization'),
        related_name="teams",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    department = models.ForeignKey(
        'Department',
        verbose_name=_('department'),
        related_name="teams",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    code = models.CharField(
        _('code'),
        max_length=64,
        blank=True,
        null=True
    )
    is_legacy = models.BooleanField(
        _('is legacy'),
        default=False
    )
    parent = models.ForeignKey(
        'Team',
        verbose_name=_('parent team'),
        related_name="children",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    hal_tutelage = models.CharField(
        _('HAL Tutelage'),
        max_length=255,
        blank=True,
        null=True
    )
    hal_researche_structure = models.CharField(
        _('HAL Researche Structure'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('team')
        ordering = ['name', ]
        permissions = TeamOwnable.Meta.permissions

    def __str__(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        elif self.department:
            if self.department.organization:
                return ' - '.join(
                    (self.department.organization.name, self.department.name, self.name)
                )
            else:
                return ' - '.join((self.department.name, self.name))
        return self.name

    @property
    def short(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        elif self.department:
            if self.department.organization:
                return ' - '.join((self.department.organization.name, self.name))
            else:
                return ' - '.join((self.department.name, self.name))
        return self.name

    def get_absolute_url(self):
        return '/team/' + self.slug


class TeamPage(Page, SubTitled, RichText):
    """(Team description)"""

    team = models.ForeignKey(
        'Team',
        verbose_name=_('team'),
        related_name="pages",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    order_projects_by = models.CharField(
        _('Projects ordering'),
        max_length=16,
        choices=[
            ('creation_date', _('Creation Date')),
            ('manual', _('Manuel')),
        ]
    )
    display_navbar = models.BooleanField(default=True)
    displayed_in_navbars = models.BooleanField(default=True)

    class Meta():
        verbose_name = _('team page')
        permissions = TeamOwnable.Meta.permissions
        # We should put here a constraint between team and site_id
        # Note possible in Django 1.10, because the field are in two differents table in DB  # noqa: E501
        # Maybe possible in Django 2.2
        # https://docs.djangoproject.com/en/2.2/ref/models/constraints/
        # unique_together = (("team", "page__site_id"),)


class TeamLink(Link):
    team = models.ForeignKey(
        Team,
        verbose_name=_('team'),
        related_name='links',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class ProducerData(models.Model):
    """(ProducerData description)"""

    organization = models.ForeignKey(
        Organization,
        verbose_name=_('organization'),
        related_name='producer_data',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    experience_description = models.CharField(
        _('experience description'),
        max_length=60,
        help_text="Do you have prior experience with working"
        " in organizations in a co-creation process? If so,"
        " please describe it. (40 to 60 words)"
    )
    producer_description = models.TextField(
        _('producer description'),
        help_text="Description of the producer organization"
        " and the resources they bring for the proposal (100 to 150 words)."
    )

    class Meta:
        verbose_name = 'Producer data'
        verbose_name_plural = 'Producer data'


class ProducerMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ProducerMixin, self).get_context_data(**kwargs)
        self.producer = Organization.objects.get(slug=self.kwargs['slug'])
        context['producer'] = self.producer
        return context


class PersonPlaylist(PlaylistRelated):
    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        related_name='playlists',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class PersonLink(Link):
    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        related_name='links',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class PersonImage(Image):
    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        related_name='images',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class PersonFile(File):
    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        related_name='files',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class PersonBlock(Block):
    person = models.ForeignKey(
        Person,
        verbose_name=_('person'),
        related_name='blocks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class PageCustomPersonListBlockInline(Titled):
    page = models.ForeignKey(
        CustomPage,
        verbose_name=_('Page'),
        related_name='page_custom_person_list_block_inlines',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    person_list_block = models.ForeignKey(
        "PersonListBlock",
        related_name='page_custom_person_list_block_inlines',
        verbose_name=_('Person List Block'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _('Person List')

    def __str__(self):
        return self.title


class PersonListBlock(Titled, Description, Label, Dated, SiteRelated):
    style = models.CharField(
        _('style'),
        max_length=16,
        choices=PERSON_LIST_STYLE_CHOICES
    )

    class Meta:
        verbose_name = _('Person List')

    def __str__(self):
        return self.title


class PersonListBlockInline(SiteRelated):
    person_list_block = models.ForeignKey(
        PersonListBlock,
        verbose_name=_('Person List Block'),
        related_name='person_list_block_inlines',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    person = models.ForeignKey(
        Person,
        verbose_name=_('Person'),
        related_name='person_list_block_inlines',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _('Person autocomplete')


class ActivityStatus(Named):
    order = models.IntegerField(_('order number'), default=100)
    display = models.BooleanField(_('display on team page'), blank=True, default=True)
    parent = models.ForeignKey(
        'ActivityStatus',
        verbose_name=_('parent'),
        related_name='children',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _('status')
        ordering = ['order']


class ActivityGrade(Named):
    class Meta:
        verbose_name = _('grade')
        verbose_name_plural = _('grades')


class ActivityFramework(Named):
    class Meta:
        verbose_name = _('framework')
        verbose_name_plural = _('frameworks')


class ActivityFunction(Named):
    class Meta:
        verbose_name = _('function')
        verbose_name_plural = _('functions')


class BudgetCode(Named):
    class Meta:
        verbose_name = _('budget code')
        verbose_name_plural = _('budget codes')


class RecordPiece(Named):
    class Meta:
        verbose_name = _('record piece')
        verbose_name_plural = _('record pieces')


class TrainingType(Named):
    class Meta:
        verbose_name = _('training type')
        verbose_name_plural = _('training types')


class TrainingLevel(Named):
    class Meta:
        verbose_name = _('training level')
        verbose_name_plural = _('training levels')


class TrainingTopic(Named):
    class Meta:
        verbose_name = _('training topic')
        verbose_name_plural = _('training topics')


class TrainingSpeciality(Named):
    class Meta:
        verbose_name = _('training speciality')
        verbose_name_plural = _('training specialities')


class UMR(Named):
    class Meta:
        verbose_name = _('UMR')


class ActivityWeeklyHourVolume(Titled, Description):
    monday_am = models.FloatField(_('monday AM'), validators=[validate_positive])
    monday_pm = models.FloatField(_('monday PM'), validators=[validate_positive])
    tuesday_am = models.FloatField(_('tuesday AM'), validators=[validate_positive])
    tuesday_pm = models.FloatField(_('tuesday PM'), validators=[validate_positive])
    wednesday_am = models.FloatField(_('wednesday AM'), validators=[validate_positive])
    wednesday_pm = models.FloatField(_('wednesday PM'), validators=[validate_positive])
    thursday_am = models.FloatField(_('thursday AM'), validators=[validate_positive])
    thursday_pm = models.FloatField(_('thursday PM'), validators=[validate_positive])
    friday_am = models.FloatField(_('friday AM'), validators=[validate_positive])
    friday_pm = models.FloatField(_('friday PM'), validators=[validate_positive])

    class Meta:
        verbose_name = _('Activity Weekly Hour Volume')
        verbose_name_plural = _('Activity Weekly Hour Volumes')


class PersonActivity(Period):
    """(Activity description)"""

    person = models.ForeignKey(
        'Person',
        verbose_name=_('person'),
        related_name='activities',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    weeks = models.IntegerField(
        _('number of weeks'),
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        ActivityStatus,
        verbose_name=_('status'),
        blank=True,
        null=True,
        related_name='activities',
        on_delete=models.SET_NULL
    )
    is_permanent = models.BooleanField(_('permanent'), default=False)
    framework = models.ForeignKey(
        ActivityFramework,
        verbose_name=_('framework'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    grade = models.ForeignKey(
        ActivityGrade,
        verbose_name=_('grade'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    function = models.ForeignKey(
        ActivityFunction,
        verbose_name=_('function'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    organizations = models.ManyToManyField(
        Organization,
        verbose_name=_('organizations (attachment or subscribed)'),
        related_name='project_activities',
        blank=True
    )
    employers = models.ManyToManyField(
        Organization,
        verbose_name=_('employers'),
        related_name='employer_project_activities',
        blank=True
    )
    umr = models.ForeignKey(
        UMR,
        verbose_name=_('UMR'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    teams = models.ManyToManyField(
        'Team',
        verbose_name=_('teams'),
        related_name='team_activities',
        blank=True
    )
    team_text = models.CharField(
        _('other team text'),
        blank=True,
        null=True,
        max_length=256
    )
    rd_quota_float = models.FloatField(
        _('R&D quota (float)'),
        blank=True,
        null=True
    )
    rd_quota_text = models.CharField(
        _('R&D quota (text)'),
        blank=True,
        null=True,
        max_length=128
    )
    rd_program = models.TextField(
        _('R&D program'),
        blank=True
    )
    budget_code = models.ForeignKey(
        BudgetCode,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    supervisors = models.ManyToManyField(
        'Person',
        verbose_name=_('supervisors'),
        related_name='supervisor_activities',
        blank=True
    )

    phd_doctoral_school = models.ForeignKey(
        Organization,
        verbose_name=_('doctoral school'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    phd_directors = models.ManyToManyField(
        'Person',
        verbose_name=_('PhD directors'),
        related_name='phd_director_activities',
        blank=True
    )
    phd_defense_date = models.DateField(
        _('PhD defense date'),
        blank=True,
        null=True
    )
    phd_title = models.TextField(_('PhD title'), blank=True)
    phd_post_doctoral_situation = models.CharField(
        _('post-doctoral situation'),
        blank=True,
        max_length=256
    )
    hdr = models.BooleanField(_('HDR'), default=False)

    training_type = models.ForeignKey(
        TrainingType,
        verbose_name=_('training type'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    training_level = models.ForeignKey(
        TrainingLevel,
        verbose_name=_('training level'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    training_topic = models.ForeignKey(
        TrainingTopic,
        verbose_name=_('training topic'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    training_speciality = models.ForeignKey(
        TrainingSpeciality,
        verbose_name=_('training speciality'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    training_title = models.TextField(
        _('Training title'),
        blank=True
    )

    record_piece = models.ForeignKey(
        RecordPiece,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    date_added = models.DateTimeField(
        _('add date'),
        auto_now_add=True
    )
    date_modified = models.DateTimeField(
        _('modification date'),
        auto_now=True
    )
    date_modified_manual = models.DateTimeField(
        _('manual modification date'),
        blank=True,
        null=True
    )

    comments = models.TextField(
        _('comments'),
        blank=True
    )
    external_id = models.CharField(
        _('external ID'),
        blank=True,
        null=True,
        max_length=128
    )

    weekly_hour_volume = models.ForeignKey(
        'ActivityWeeklyHourVolume',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    monday_am = models.FloatField(
        _('monday AM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    monday_pm = models.FloatField(
        _('monday PM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    tuesday_am = models.FloatField(
        _('tuesday AM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    tuesday_pm = models.FloatField(
        _('tuesday PM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    wednesday_am = models.FloatField(
        _('wednesday AM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    wednesday_pm = models.FloatField(
        _('wednesday PM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    thursday_am = models.FloatField(
        _('thursday AM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    thursday_pm = models.FloatField(
        _('thursday PM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    friday_am = models.FloatField(
        _('friday AM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )
    friday_pm = models.FloatField(
        _('friday PM'),
        validators=[validate_positive],
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['-date_from', ]

    def __str__(self):
        if self.status:
            return ' - '.join(
                (self.status.name, str(self.date_from), str(self.date_to))
            )
        else:
            return ' - '.join((str(self.date_from), str(self.date_to)))

    def save(self, *args, **kwargs):
        super(PersonActivity, self).save(*args, **kwargs)
        update_activity(self)


class PersonActivityTimeSheet(models.Model):
    activity = models.ForeignKey(
        'PersonActivity',
        verbose_name=_('activity'),
        related_name='timesheets',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        'organization_projects.Project',
        verbose_name=_('project'),
        related_name='timesheets',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    work_packages = models.ManyToManyField(
        'organization_projects.ProjectWorkPackage',
        verbose_name=_('work package'),
        related_name='timesheets',
        blank=True
    )
    percentage = models.IntegerField(
        _('% of work time on the project'),
        validators=[is_percent],
        help_text="Percentage has to be an integer between 0 and 100"
    )
    month = models.IntegerField(_('month'), choices=MONTH_CHOICES)
    year = models.IntegerField(_('year'))
    accounting = models.DateField(blank=True, null=True)
    validation = models.DateField(blank=True, null=True)

    @property
    def date(self):
        pass

    class Meta:
        verbose_name = _('activity timesheet')
        verbose_name_plural = _('activity timesheets')
        ordering = ['-year', 'month', 'project']
        unique_together = (("activity", "project", "month", "year"),)


class ProjectActivity(Titled, Description, Orderable):
    activity = models.ForeignKey(
        'PersonActivity',
        verbose_name=_('activity'),
        related_name='project_activity',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        'organization_projects.Project',
        verbose_name=_('project'),
        related_name='project_activity',
        null=True,
        on_delete=models.SET_NULL
    )
    default_percentage = models.IntegerField(
        _('default %'),
        validators=[is_percent],
        blank=True,
        null=True,
        help_text="Percentage has to be an integer between 0 and 100"
    )
    work_packages = models.ManyToManyField(
        'organization_projects.ProjectWorkPackage',
        verbose_name=_('work package'),
        related_name='project_activity',
        blank=True
    )
    work_packages.widget = forms.CheckboxSelectMultiple()

    class Meta:
        verbose_name = _('project activity')
        verbose_name_plural = _('project activities')
        unique_together = (("activity", "project", "default_percentage",),)

    def save(self, **kwargs):
        self.title = self.activity.person.title
        super(ProjectActivity, self).save()


class PersonActivityVacation(Period):
    activity = models.ForeignKey(
        'PersonActivity',
        verbose_name=_('activity'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


def update_activity(a):
    if a.weekly_hour_volume:
        # caution : if 0 return False
        # caution : 'None' is not empty
        if not a.monday_am.__str__() != 'None' and \
                not a.monday_pm.__str__() != 'None' and \
                not a.tuesday_am.__str__() != 'None' and \
                not a.tuesday_pm.__str__() != 'None' and \
                not a.wednesday_am.__str__() != 'None' and \
                not a.wednesday_pm.__str__() != 'None' and \
                not a.thursday_am.__str__() != 'None' and \
                not a.thursday_pm.__str__() != 'None' and \
                not a.friday_am.__str__() != 'None' and \
                not a.friday_pm.__str__() != 'None':
            a.monday_am = a.weekly_hour_volume.monday_am
            a.monday_pm = a.weekly_hour_volume.monday_pm
            a.tuesday_am = a.weekly_hour_volume.tuesday_am
            a.tuesday_pm = a.weekly_hour_volume.tuesday_pm
            a.wednesday_am = a.weekly_hour_volume.wednesday_am
            a.wednesday_pm = a.weekly_hour_volume.wednesday_pm
            a.thursday_am = a.weekly_hour_volume.thursday_am
            a.thursday_pm = a.weekly_hour_volume.thursday_pm
            a.friday_am = a.weekly_hour_volume.friday_am
            a.friday_pm = a.weekly_hour_volume.friday_pm
            a.save()


class MediaDepartment(models.Model):
    media = models.ForeignKey(
        Media,
        verbose_name=_('media'),
        related_name='department',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    department = models.ForeignKey(
        Department,
        verbose_name=_('department'),
        related_name='medias',
        # limit_choices_to=dict(id__in=Department.objects.all()),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )


class TeamProjectOrdering(SiteRelated, Orderable):
    project_page = models.ForeignKey(
        'organization_projects.ProjectPage',
        verbose_name=_('Project'),
        related_name='teamprojectordering',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    team_page = models.ForeignKey(
        'TeamPage',
        verbose_name=_('Team'),
        related_name='teamprojectordering',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = (("project_page", "team_page",),)

    @receiver(post_save, sender='organization_projects.ProjectPage')
    def create_order(sender, instance, **kwargs):
        model_project_page = apps.get_model('organization_projects', 'ProjectPage')
        if type(instance) is model_project_page:
            for team in instance.project.teams.all():
                try:
                    TeamProjectOrdering.objects.get(
                        project_page=instance,
                        team_page=team.pages.first()
                    )
                except ObjectDoesNotExist:
                    tp = TeamProjectOrdering()
                    tp.project_page = instance
                    tp.team_page = team.pages.first()
                    tp.site_id = tp.team_page.site_id
                    tp.save()
