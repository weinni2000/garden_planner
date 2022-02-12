# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TaskCalendar(models.Model):
    _name = "lisigruen.taskcalendar"
    _description = "taskcalendar"
    _inherit = ['mail.thread', "mail.activity.mixin"]

    date = fields.Date(string='Aktivitätsdatum')
    crop = fields.Char(string='Crop Name', required=True)
    batchnr = fields.Char(string='Batch Nr')
    name_common = fields.Char(string='Vulgo')
    activity = fields.Char(string='Aktivität')
