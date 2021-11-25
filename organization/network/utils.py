# -*- coding: utf-8 -*-
import pandas as pd
from django.http import HttpResponse
from xlwt import Workbook, Font, Pattern, Style, XFStyle, Alignment
import calendar
import datetime
from django.apps import apps
from django.utils import timezone
from django.http import QueryDict
from organization.network.api import get_leave_days_per_month
from collections import OrderedDict
from workalendar.europe import France
from django.urls import reverse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings


def get_nb_half_days_by_period(date_from, date_to):
    day_list = pd.date_range(date_from, date_to).tolist()
    day_dict = {
      "monday_am": 0,
      "monday_pm": 0,
      "tuesday_am": 0,
      "tuesday_pm": 0,
      "wednesday_am": 0,
      "wednesday_pm": 0,
      "thursday_am": 0,
      "thursday_pm": 0,
      "friday_am": 0,
      "friday_pm": 0,
    }
    for day in day_list:
        if day.dayofweek == 0:
            day_dict['monday_am'] += 1
            day_dict['monday_pm'] += 1
        if day.dayofweek == 1:
            day_dict['tuesday_am'] += 1
            day_dict['tuesday_pm'] += 1
        if day.dayofweek == 2:
            day_dict['wednesday_am'] += 1
            day_dict['wednesday_pm'] += 1
        if day.dayofweek == 3:
            day_dict['thursday_am'] += 1
            day_dict['thursday_pm'] += 1
        if day.dayofweek == 4:
            day_dict['friday_am'] += 1
            day_dict['friday_pm'] += 1

    return day_dict


def get_nb_half_days_by_period_per_month(date_from, date_to):
    day_list = pd.date_range(date_from, date_to).tolist()
    cal = France()
    holidays = cal.holidays(date_from.year)
    holidays_date = [h[0] for h in holidays]
    md_dict = {}
    for i in range(1, 13):
        md_dict[i] = {
          "monday_am": 0,
          "monday_pm": 0,
          "tuesday_am": 0,
          "tuesday_pm": 0,
          "wednesday_am": 0,
          "wednesday_pm": 0,
          "thursday_am": 0,
          "thursday_pm": 0,
          "friday_am": 0,
          "friday_pm": 0,
        }

    # for each day of the period
    for day in day_list:
        if not day.date() in holidays_date:
            if day.dayofweek == 0:
                md_dict[day.month]['monday_am'] += 1
                md_dict[day.month]['monday_pm'] += 1
            if day.dayofweek == 1:
                md_dict[day.month]['tuesday_am'] += 1
                md_dict[day.month]['tuesday_pm'] += 1
            if day.dayofweek == 2:
                md_dict[day.month]['wednesday_am'] += 1
                md_dict[day.month]['wednesday_pm'] += 1
            if day.dayofweek == 3:
                md_dict[day.month]['thursday_am'] += 1
                md_dict[day.month]['thursday_pm'] += 1
            if day.dayofweek == 4:
                md_dict[day.month]['friday_am'] += 1
                md_dict[day.month]['friday_pm'] += 1

    return md_dict


class TimesheetXLS(object):

    sheet_title = "IRCAM Time sheet declaration"
    t_dict = OrderedDict()
    first_month_row = 5
    first_month_col = 4
    last_month_col = first_month_col + 13
    total_prod_hours_label = "Total productive hours for the reporting period :"
    total_prod_hours_label_col = 8
    total_prod_hours_label_row = 3
    total_prod_hours_label_val_col = 12
    total_prod_hours_label_val_row = 3
    month_label = "Months"
    month_label_col = 0
    month_label_row = 5
    project_margin_row = 4
    project_first_row = 6
    project_first_col = 0
    percent_margin = 1
    percent_label = "Percentage of time worked on project"
    percent_label_row = 7
    percent_label_col = 0
    hours_margin = 2
    hours_label = "Productive hours worked on project"
    hours_label_row = 8
    hours_label_col = 0
    wk_margin = 3
    wk_label = "Workpackages to which the person has contributed"
    wk_label_row = 9
    wk_label_col = 0
    accounting_margin = 4
    accounting_label = "Date of accounting by person working on the action"
    accounting_label_col = 0
    validation_margin = 5
    validation_label_row = 0
    validation_label = "Date of validation by the superior"
    validation_label_col = 0
    title_col = 0
    title_row = 0
    beneficiary_col = 0
    beneficiary_row = 2
    name_person_col = 0
    name_person_row = 3
    type_personal_col = 3
    type_personal_row = 3
    person_signature_label = "Signature of person working on the action :"
    person_signature_col = 1
    person_signature_row_margin = 9
    director_signature_label = "Signature of R&D Department Director:"
    director_signature_col = 7
    director_signature_row_margin = 9
    debug_col = 4
    debug_row = 38

    def __init__(self, timesheets, year=datetime.date.today().year):
        self.timesheets = timesheets.order_by(
            'activity__person',
            'project',
            'year',
            'month'
        )
        self.book = Workbook()
        self.year = int(year)
        font_header = Font()
        font_header.bold = True

        font_title = Font()
        font_title.bold = True

        grey_pattern = Pattern()
        grey_pattern.pattern = Pattern.SOLID_PATTERN
        grey_pattern.pattern_fore_colour = Style.colour_map['gray25']

        self.header_style = XFStyle()
        self.header_style.pattern = grey_pattern
        self.header_style.font = font_header

        self.header_title = XFStyle()
        self.header_title.font = font_title

        self.date_style = XFStyle()
        self.date_style.num_format_str = 'M/D/YY'

        self.title_style = XFStyle()
        self.title_style.pattern = grey_pattern
        self.title_style.font = font_title
        self.title_style.alignment.horz = self.title_style.alignment.HORZ_CENTER

        self.txt_centered_al = Alignment()
        self.txt_centered_al.horz = Alignment.HORZ_CENTER

        self.txt_centered = XFStyle()
        self.txt_centered.alignment = self.txt_centered_al

        self.header_date_style = XFStyle()
        self.header_date_style.pattern = grey_pattern
        self.header_date_style.font = font_header
        self.header_date_style.alignment = self.txt_centered_al

    def init_layout(self, sheet, year, activity):
        sheet.write_merge(
            0,
            self.title_row,
            self.title_col,
            self.title_col + 16,
            self.sheet_title,
            self.title_style
        )
        sheet.col(0).width = 0x0d00 + 6500
        sheet.col(1).width = 0x0d00 + 2000
        sheet.col(3).width = 0x0d00 + 1600
        row = sheet.row(self.first_month_row)
        for i in range(self.first_month_col + 1, self.last_month_col):
            row.write(
                i,
                calendar.month_name[i - self.first_month_col][:3] + "-" + str(year % 100),  # noqa: E501
                self.header_date_style
            )
        sheet.write_merge(
            self.month_label_row,
            self.month_label_row,
            self.month_label_col,
            self.month_label_col + 4,
            self.month_label,
            self.header_style
        )
        sheet.write(
            self.beneficiary_row,
            self.beneficiary_col,
            "Beneficiary :",
            self.header_style
        )
        sheet.write(
            self.beneficiary_row,
            self.beneficiary_col + 1,
            "IRCAM"
        )
        sheet.write(
            self.name_person_row,
            self.name_person_col,
            "Name of person working on the action :",
            self.header_style
        )
        sheet.write(
            self.name_person_row,
            self.name_person_col + 1,
            activity.person.title
        )
        sheet.write(
            self.type_personal_row,
            self.type_personal_col,
            "Type of personnel :",
            self.header_style
        )
        if activity.function.name:
            sheet.write_merge(
                self.type_personal_row,
                self.type_personal_row,
                self.type_personal_col + 1,
                self.type_personal_col + 3,
                activity.function.name
            )
        return sheet

    def format(self):
        self.t_dict = OrderedDict()

        for timesheet in self.timesheets:
            worked_hours_by_month = {}
            person_slug = timesheet.activity.person.slug
            date_from = datetime.date(timesheet.year, 1, 1)
            date_to = datetime.date(timesheet.year, 12, 31)
            # if new person
            if person_slug not in self.t_dict:
                self.t_dict[person_slug] = {}
                leave_days = get_leave_days_per_month(
                    date_from,
                    date_to,
                    timesheet.activity.person.external_id
                )
                # caculate for each person leaved days in year
            nb_half_days = get_nb_half_days_by_period_per_month(date_from, date_to)
            # for each month
            m_key = timesheet.month
            m_val = nb_half_days[m_key]
            if m_key not in worked_hours_by_month:
                worked_hours_by_month[m_key] = 0
            curr_date = datetime.date(self.year, m_key, 1)
            if timesheet.activity.date_from <= curr_date and\
                    curr_date <= timesheet.activity.date_to:
                # for each week day
                for nhd_k, nhd_v in m_val.items():
                    # get theorical hours worked by half days, taking in account full / half time contract  # noqa: E501
                    half_day_nb_hours = getattr(timesheet.activity, nhd_k)
                    if half_day_nb_hours is not None:
                        # has the person been present during current m_key month ?
                        if m_key in leave_days:
                            if nhd_k in leave_days[m_key]:
                                # has the person been absent during current half day nhd_d ?  # noqa: E501
                                worked_hours_by_month[m_key] +=\
                                    (
                                        nb_half_days[m_key][nhd_k] -
                                        leave_days[m_key][nhd_k]
                                    ) * half_day_nb_hours
                            else:
                                # if not, count theorical nb oh hours for this half day
                                worked_hours_by_month[m_key] +=\
                                    nb_half_days[m_key][nhd_k] * half_day_nb_hours
                        # if not, count theorical nb of hours for whole month
                        else:
                            worked_hours_by_month[m_key] +=\
                                nb_half_days[m_key][nhd_k] * half_day_nb_hours
                    # else :
                    #     # missing data...
                    #     worked_hours_by_month[m_key] = 0
            else:
                worked_hours_by_month[m_key] = 0

            # for each percent time worked on a project...
            project_slug = timesheet.project.slug
            if project_slug not in self.t_dict[person_slug]:
                self.t_dict[person_slug][project_slug] = []
            # ...calculate nb of worked hours proportionally
            # the property 'worked_hours' does not exists in the model,
            # it just calculated on the fly
            timesheet.worked_hours = worked_hours_by_month[timesheet.month]
            self.t_dict[person_slug][project_slug].append(timesheet)
        return self.t_dict

    def export(self):
        project_row_last = 6

        # for each person
        for person_k, person_v in self.t_dict.items():
            total_prod_hours = 0
            total_prod_hours_dict = dict()
            try:
                sheet = self.book.add_sheet(person_k)
                sheet.default_width = 200
            except Exception:
                pass
            # for each project
            number_of_projects = len(person_v)
            project_row_last = (number_of_projects - 1) * self.project_margin_row +\
                self.project_first_row
            for project_k, project_v in person_v.items():
                project_position = list(person_v.keys()).index(project_k)
                project_row_index = self.project_margin_row * project_position +\
                    self.project_first_row
                # for each timesheet
                for timesheet in project_v:
                    try:
                        sheet = self.init_layout(
                            sheet,
                            timesheet.year,
                            timesheet.activity
                        )
                    except Exception:
                        pass

                    # project name
                    try:
                        sheet.write(
                            project_row_index,
                            self.project_first_col,
                            timesheet.project.title,
                            self.header_style
                        )
                    except Exception:
                        pass

                    # percent
                    percent = timesheet.percentage / 100
                    try:
                        sheet.write(
                            project_row_index + self.percent_margin,
                            timesheet.month + self.first_month_col,
                            percent,
                            self.txt_centered
                        )
                    except Exception:
                        pass

                    # nb worked hours
                    if timesheet.month not in total_prod_hours_dict:
                        total_prod_hours_dict[timesheet.month] = timesheet.worked_hours
                    try:
                        sheet.write(
                            project_row_index + self.hours_margin,
                            timesheet.month + self.first_month_col,
                            timesheet.worked_hours * percent,
                            self.txt_centered
                        )
                        if settings.DEBUG:
                            sheet.write(
                                self.debug_row + project_position,
                                timesheet.month + self.debug_col,
                                timesheet.worked_hours,
                                self.txt_centered
                            )
                    except Exception:
                        pass

                    # work packages
                    work_packages = [
                        str(wk.number) for wk in timesheet.work_packages.all()
                    ]
                    work_packages = ",".join(work_packages)
                    try:
                        sheet.write(
                            project_row_index +
                            self.wk_margin,

                            timesheet.month +
                            self.first_month_col, work_packages,

                            self.txt_centered
                        )
                    except Exception:
                        pass

                    try:
                        sheet.write(
                            project_row_index,
                            self.project_first_col + 1,
                            "Grant agreement N°",
                            self.header_style
                        )
                        sheet.write_merge(
                            project_row_index,
                            project_row_index,
                            self.project_first_col + 2,
                            self.project_first_col + 4,
                            timesheet.project.external_id,
                            self.header_style
                        )
                        percent_row = project_row_index + self.percent_margin
                        sheet.write_merge(
                            percent_row,
                            percent_row,
                            self.percent_label_col,
                            self.percent_label_col + 4,
                            self.percent_label
                        )
                        hours_row = project_row_index + self.hours_margin
                        sheet.write_merge(
                            hours_row,
                            hours_row,
                            self.hours_label_col,
                            self.hours_label_col + 4,
                            self.hours_label
                        )
                        wk_row = project_row_index + self.wk_margin
                        sheet.write_merge(
                            wk_row,
                            wk_row,
                            self.wk_label_col,
                            self.wk_label_col + 4,
                            self.wk_label
                        )
                        for i in range(self.first_month_col + 1, self.last_month_col):
                            sheet.write(project_row_index,  i, "", self.header_style)

                    except Exception:
                        pass

                    try:
                        # accounting date
                        sheet.write(
                            project_row_last + self.accounting_margin,
                            timesheet.month + self.first_month_col,
                            timesheet.accounting,
                            self.date_style
                        )
                        # validation date
                        sheet.write(
                            project_row_last + self.validation_margin,
                            timesheet.month + self.first_month_col,
                            timesheet.validation,
                            self.date_style
                        )
                        sheet.write_merge(
                            project_row_last + self.accounting_margin,
                            project_row_last + self.accounting_margin,
                            self.accounting_label_col,
                            self.accounting_label_col + 4,
                            self.accounting_label,
                            self.date_style
                        )
                        sheet.write_merge(
                            project_row_last + self.validation_margin,
                            project_row_last + self.validation_margin,
                            self.accounting_label_col,
                            self.accounting_label_col + 4,
                            self.validation_label,
                            self.date_style
                        )
                    except Exception:
                        pass
                    try:
                        person_signature_row = project_row_last +\
                            self.person_signature_row_margin
                        sheet.write_merge(
                            person_signature_row,
                            person_signature_row,
                            self.person_signature_col,
                            self.person_signature_col + 3,
                            self.person_signature_label
                        )
                        director_signature_row = project_row_last +\
                            self.director_signature_row_margin
                        sheet.write_merge(
                            director_signature_row,
                            director_signature_row,
                            self.director_signature_col,
                            self.director_signature_col + 2,
                            self.director_signature_label
                        )
                    except Exception:
                        pass

            total_prod_hours = proccess_total_prod_hours(total_prod_hours_dict)
            try:
                # productive hours
                sheet.write_merge(
                    self.total_prod_hours_label_row,
                    self.total_prod_hours_label_row,
                    self.total_prod_hours_label_col,
                    self.total_prod_hours_label_col + 3,
                    self.total_prod_hours_label,
                    self.header_style
                )
                sheet.write(
                    self.total_prod_hours_label_val_row,
                    self.total_prod_hours_label_val_col,
                    total_prod_hours
                )
            except Exception:
                pass

    def write(self):
        self.format()
        self.export()
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=timesheet_ircam' +\
            str(self.year)+'.xls'
        self.book.save(response)
        return response


def set_timesheets_validation_date(timesheets):
    """ Admin action to set validation date for selected timesheets """
    for timesheet in timesheets :
        if not timesheet.validation:
            timesheet.validation = timezone.now()
            timesheet.save()


def timesheet_master_notification_for_validation(person, month, year, app_label, model):
    q = QueryDict(mutable=True)
    q['activity__person__id'] = person.id
    q['month__exact'] = str(month)
    q['year__exact'] = str(year)
    query_string = q.urlencode()
    url_admin = reverse("admin:%s_%s_changelist" % (app_label, model.lower()))
    current_site = Site.objects.get_current()

    ctx = {
        'url': "https://" + current_site.domain+url_admin + "?" + query_string,
        'person_first_name': person.first_name,
        'person_last_name': person.last_name,
        'month': month,
        'year': year
    }

    subject = "[WWW] " +\
        person.first_name +\
        " " +\
        person.last_name +\
        " vient de saisir ses timesheets"
    message = get_template(
        'email/timesheet_master_notification_for_validation.html'
    ).render(ctx)
    msg = EmailMessage(
        subject,
        message,
        to=(settings.TIMESHEET_MASTER_MAIL,),
        from_email=settings.DEFAULT_FROM_EMAIL
    )
    msg.content_subtype = 'html'
    msg.send()


def proccess_total_prod_hours(prod_hours_dict):
    total = 0
    for month, hours in prod_hours_dict.items():
        total += hours
    return total


def flatten_activities(activities, fields):
    flat = []
    for activity in activities:
        for field in fields:
            data = getattr(activity, field)
            if type(data).__name__ == 'ManyRelatedManager':
                data = data.all()
                data2 = []
                for d in data:
                    data2.append(d.name)
                data = ",".join(data2)
            flat.append(data)
    return flat


def get_users_of_team(team):
    users = set()
    person_activity_model = apps.get_model('organization_network.PersonActivity')
    activities = person_activity_model.objects.filter(teams=team)
    for activity in activities:
        users.add(activity.person.user)
    return users


def get_team_from_user(user):
    try:
        team = user.person.activities.latest('date_from').teams.first()
        if team.department.id == 1:  # Research Department
            return team
    except Exception:
        pass
