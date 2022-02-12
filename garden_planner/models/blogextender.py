# -*- coding: utf-8 -*-

from odoo import models, fields, api


class blog_blog_extender(models.Model):
    _name = "gardenplanner.blogtester"
    _description = 'blog_blog_extender'
    _inherit = "blog.blog"

    inst_type = fields.Text(default=False)
    short_code = fields.Text(default=False)
