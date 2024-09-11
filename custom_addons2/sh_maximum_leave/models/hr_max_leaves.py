# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import calendar
from datetime import datetime

from odoo.exceptions import UserError

from odoo import fields, models, api


class HrLeaveStatus(models.Model):
    _inherit = 'hr.leave.type'

    set_max_days_leave = fields.Boolean("Maximum Days in Leave")
    no_max_days_leave = fields.Float("No. of Maximum Days in Leave")

    set_max_days_leave_month = fields.Boolean("Maximum Days Leave in Month")
    no_max_days_leave_month = fields.Float("No. of Maximum Days in Month")

    @api.onchange('request_unit')
    def date_from_onchange_max_days(self):
        if self:
            for rec in self:
                if rec.request_unit:

                    if rec.request_unit == 'hour':
                        rec.set_max_days_leave = False
                        rec.set_max_days_leave_month = False


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    is_changed_max_days = fields.Boolean("Is Changed Max Days", default=False)

    @api.model
    def create(self, values):

        if values and values.get('holiday_status_id', False) and values.get('date_from', False) and values.get(
                'date_to', False) and values.get('employee_id', False):

            hol_status_obj = self.env['hr.leave.type'].search(
                [('id', '=', values.get('holiday_status_id')), ('request_unit', '=', 'day')], limit=1)

            if hol_status_obj and (hol_status_obj.set_max_days_leave or hol_status_obj.set_max_days_leave_month):

                alert_date = True  # Must check for date
                loged_user_id = self.env.user.id

                if loged_user_id and values:
                    grp_id = self.env.ref('hr.group_hr_manager').id

                    if grp_id:
                        grps_obj = self.env['res.groups'].search(
                            [('id', '=', grp_id)], limit=1)
                        if grps_obj:
                            for record in grps_obj[0].users:
                                if record.id == loged_user_id:  # If Have "Hr Manager" Group

                                    if values.get('employee_id'):
                                        empl_obj = self.env['hr.employee'].search(
                                            [('id', '=', values.get('employee_id'))], limit=1)

                                        if empl_obj[0].user_id:

                                            # If User is applying for self having group
                                            if empl_obj[0].user_id.id == loged_user_id:
                                                alert_date = True
                                            else:
                                                alert_date = False

                    if alert_date == True:  # Need to check for date enter

                        ######### Total Continue Leave Check #############

                        if hol_status_obj.set_max_days_leave and hol_status_obj.no_max_days_leave:  # If check set to True for this leave

                            taken_leaves = 0
                            if values.get('number_of_days', False) and values.get('number_of_days') > 0:

                                taken_leaves = "%.2f" % values.get(
                                    'number_of_days')

                                if taken_leaves and float(taken_leaves) > hol_status_obj.no_max_days_leave:
                                    raise UserError(
                                        'You can apply maximum of ' + str(hol_status_obj.no_max_days_leave) +
                                        ' days leave for type ' + hol_status_obj.name + '. Please contact your manager for further approval.')

                        ######### Month Wise Leave Check #############

                        # If check set to True for this leave
                        if hol_status_obj.set_max_days_leave_month and hol_status_obj.no_max_days_leave_month:

                            raise_err = False

                            cur_month = datetime.now().month
                            cur_year = datetime.now().year
                            num_days = calendar.monthrange(cur_year, cur_month)

                            last_day = datetime(
                                year=cur_year, month=cur_month, day=num_days[1]).date()
                            first_day = datetime(
                                year=cur_year, month=cur_month, day=1).date()

                            hol_empl_obj = self.env['hr.leave'].search(
                                [('employee_id', '=', values.get('employee_id')), ('holiday_status_id', '=', values.get(
                                    'holiday_status_id')),
                                 ('state', 'in', ['draft', 'confirm', 'validate', 'validate1'])])
                            taken_tot_lvs = 0.0

                            if values.get('number_of_days', False) and values.get('number_of_days') > 0:
                                taken_tot_lvs += values.get('number_of_days')

                            if hol_empl_obj:
                                for rec in hol_empl_obj:
                                    rec_frm = datetime.strptime(
                                        str(rec.date_from), "%Y-%m-%d %H:%M:%S").date()
                                    rec_to = datetime.strptime(
                                        str(rec.date_to), "%Y-%m-%d %H:%M:%S").date()

                                    if (rec_frm >= first_day and rec_to <= last_day) and (
                                            rec_to >= first_day and rec_to <= last_day):
                                        taken_tot_lvs += rec.number_of_days

                            if taken_tot_lvs > hol_status_obj.no_max_days_leave_month:
                                raise_err = True

                            if raise_err == True:
                                raise UserError(
                                    'You can apply maximum of ' + str(hol_status_obj.no_max_days_leave_month) +
                                    ' days leave per month for type ' + hol_status_obj.name + '. Please contact your manager for further approval.')
        if values:
            values.update({'is_changed_max_days': True})

        res = super(HrLeave, self).create(values)
        return res

    @api.onchange('holiday_status_id', 'date_from', 'date_to', 'employee_id')
    def date_from_onchange_max_days(self):

        if self:
            for rec in self:
                if rec.date_from and rec.date_to and rec.holiday_status_id:

                    if rec.holiday_status_id.request_unit == 'day' and (
                            rec.holiday_status_id.set_max_days_leave or rec.holiday_status_id.set_max_days_leave_month):

                        start_dt = datetime.strptime(
                            str(rec.date_from), "%Y-%m-%d %H:%M:%S").date()
                        end_dt = datetime.strptime(
                            str(rec.date_to), "%Y-%m-%d %H:%M:%S").date()

                        cur_month = datetime.now().month
                        cur_year = datetime.now().year
                        num_days = calendar.monthrange(cur_year, cur_month)

                        last_day = datetime(
                            year=cur_year, month=cur_month, day=num_days[1]).date()
                        first_day = datetime(
                            year=cur_year, month=cur_month, day=1).date()

                        self_id = rec._origin.id

                        # and ( self.holiday_status_id.set_max_days_leave or self.holiday_status_id.set_max_days_leave_month ) : # This is called at Write / Update time only
                        if rec.is_changed_max_days == True and rec.employee_id and self_id:

                            alert_date = True  # Must check for date
                            loged_user_id = self.env.user.id

                            if loged_user_id:
                                grp_id = self.env.ref('hr.group_hr_manager').id

                                if grp_id:
                                    grps_obj = self.env['res.groups'].search(
                                        [('id', '=', grp_id)], limit=1)

                                    if grps_obj:
                                        for record in grps_obj[0].users:
                                            if record.id == loged_user_id:  # If Have "Hr Manager" Group

                                                if rec.employee_id:
                                                    empl_obj = self.env['hr.employee'].search(
                                                        [('id', '=', rec.employee_id.id)], limit=1)

                                                    if empl_obj[0].user_id:

                                                        # If User is applying for self having group
                                                        if empl_obj[0].user_id.id == loged_user_id:
                                                            alert_date = True
                                                        else:
                                                            alert_date = False

                                if alert_date == True:  # Need to check for date enter

                                    ######### Total Continue Leave Check #############

                                    # If check set to True for this leave
                                    if rec.holiday_status_id.set_max_days_leave and rec.holiday_status_id.no_max_days_leave:
                                        taken_leaves = 0

                                        if rec.number_of_days and rec.number_of_days > 0:
                                            taken_leaves = " %.2f" % rec.number_of_days

                                            if taken_leaves and float(
                                                    taken_leaves) > rec.holiday_status_id.no_max_days_leave:
                                                rec.date_from = ''
                                                rec.date_to = ''

                                                warning_mess = {
                                                    'message': ('You can apply maximum of ' + str(
                                                        rec.holiday_status_id.no_max_days_leave) + ' days leave for type ' + rec.holiday_status_id.name + '. Please contact your manager for further approval.'),
                                                    'title': "Warning"
                                                }
                                                return {'warning': warning_mess}

                                    ######### Month Wise Leave Check #############

                                    if rec.holiday_status_id.set_max_days_leave_month and rec.holiday_status_id.no_max_days_leave_month:  # If check set to True for this leave

                                        raise_err = False

                                        cur_month = datetime.now().month
                                        cur_year = datetime.now().year
                                        num_days = calendar.monthrange(
                                            cur_year, cur_month)

                                        last_day = datetime(
                                            year=cur_year, month=cur_month, day=num_days[1]).date()
                                        first_day = datetime(
                                            year=cur_year, month=cur_month, day=1).date()

                                        hol_empl_obj = self.env['hr.leave'].search(
                                            [('employee_id', '=', rec.employee_id.id), (
                                                'holiday_status_id', '=', rec.holiday_status_id.id),
                                             ('state', 'in', ['draft', 'confirm', 'validate', 'validate1'])])
                                        taken_tot_lvs = 0.0

                                        if rec.number_of_days and rec.number_of_days > 0:
                                            taken_tot_lvs += rec.number_of_days

                                        if hol_empl_obj:
                                            for data in hol_empl_obj:
                                                if data.id != self_id:  # Do not count leaves of record you are editing now

                                                    rec_frm = datetime.strptime(
                                                        str(data.date_from), "%Y-%m-%d %H:%M:%S").date()
                                                    rec_to = datetime.strptime(
                                                        str(data.date_to), "%Y-%m-%d %H:%M:%S").date()

                                                    if (rec_frm >= first_day and rec_to <= last_day) and (
                                                            rec_to >= first_day and rec_to <= last_day):
                                                        taken_tot_lvs += data.number_of_days
                                        if taken_tot_lvs > rec.holiday_status_id.no_max_days_leave_month:
                                            raise_err = True

                                        if raise_err == True:
                                            rec.date_from = ''
                                            rec.date_to = ''
                                            warning_mess = {
                                                'message': ('You can apply maximum of ' + str(
                                                    rec.holiday_status_id.no_max_days_leave_month) + ' days leave per month for type ' + rec.holiday_status_id.name + '. Please contact your manager for further approval.'),
                                                'title': "Warning"
                                            }
                                            return {'warning': warning_mess}
