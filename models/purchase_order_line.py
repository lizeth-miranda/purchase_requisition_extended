from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    requisition_line_ids = fields.Many2many(
        'purchase.requisition.line',
        string='Líneas de Requisición'
    )

    requisition_reference = fields.Char(
        string='Referencia Contrato',
        compute='_compute_requisition_reference',
        store=True
    )

    @api.depends('requisition_line_ids.requisition_id.name')
    def _compute_requisition_reference(self):
        for line in self:
            refs = line.requisition_line_ids.mapped('requisition_id.name')
            line.requisition_reference = ', '.join(refs) if refs else ''