# -*- coding: utf-8 -*-

import itertools
import logging
from collections import defaultdict

from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = "product.category"

    category_type = fields.Selection([('raw_material', "Raw Materials"),
                                        ('packaging', "Packaging"),
                                        ('other', "Other")], string="Category Type", copy=False, default='other')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    sku_size = fields.Float("SKU Size (L)")
    prod_type = fields.Selection([('bottle', "Bottle"),
                                        ('can', "Can"),
                                        ('keg', "Keg")], string="Type", copy=False)
    rrp = fields.Float("RRP")

    @api.depends('product_variant_ids', 'product_variant_ids.default_code', 'categ_id')
    def _compute_default_code(self):
        for rec in self:
            if rec.categ_id.category_type == 'other':
                unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
                for template in unique_variants:
                    template.default_code = template.product_variant_ids.default_code
                for template in (self - unique_variants):
                    template.default_code = False
            elif rec.categ_id.category_type == 'raw_material' or rec.categ_id.parent_id.category_type == 'raw_material':
                seq = self.env['ir.sequence'].next_by_code('product.raw.material')
                if not rec.default_code:
                    rec.default_code = seq
            elif rec.categ_id.category_type == 'packaging' or rec.categ_id.parent_id.category_type == 'packaging':
                seq = self.env['ir.sequence'].next_by_code('product.template.packaging')
                if not rec.default_code:
                    rec.default_code = seq
