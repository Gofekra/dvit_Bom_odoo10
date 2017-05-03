# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.multi
    def write(self, vals):
        res = super(MrpBom, self).write(vals)
        for bom in self:
            bom_cost = 0.0
            for line in bom.bom_line_ids:
                if line.product_id.uom_id == line.product_uom:
                    bom_cost += line.product_id.standard_price * line.product_qty
            self.product_tmpl_id.standard_price = bom_cost

        return res


class ProdTempl(models.Model):
    _inherit = "product.template"
    @api.multi
    def write(self,vals):
        res = super(ProdTempl,self).write(vals)
        for prod in self:
            # get all bom lines contain this prod
            bom_line_ids = self.env['mrp.bom.line'].search([('product_id.product_tmpl_id','=',prod.id)])

            for bom_line_id in bom_line_ids:
                #trigger write on bom to update the cost.
                bom_line = self.env['mrp.bom.line'].browse(bom_line_id.id)
                bom = bom_line.bom_id
                bom.write({'position':bom_line.bom_id.position})
        return res