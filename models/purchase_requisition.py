from odoo import models, fields, api

class PurchaseRequisitionLineExtended(models.Model):
    _inherit = 'purchase.requisition.line'

    cantidad_disponible_almacen = fields.Float(string='Cantidad disponible almacen')
    is_purchase_manager = fields.Boolean(compute='_compute_is_purchase_manager')

    @api.depends_context('uid')
    def _compute_is_purchase_manager(self):
        is_manager = self.env.user.has_group('purchase.group_purchase_manager')
        for record in self:
            record.is_purchase_manager = is_manager