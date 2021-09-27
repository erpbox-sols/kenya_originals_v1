# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    division_id = fields.Many2one('division.name', string="Division", copy=False)
    region_id = fields.Many2one('region.name', string="Region", copy=False)
    area_id = fields.Many2one('region.areas', string="Area", copy=False)
    