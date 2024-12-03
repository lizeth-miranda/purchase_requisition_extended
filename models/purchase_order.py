from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    requisition_display = fields.Char(
        string='Contrato de Compra',
        compute='_compute_requisition_display',
        store=True
    )

    @api.depends('order_line.requisition_line_ids')
    def _compute_requisition_display(self):
        for order in self:
            requisitions = order.order_line.mapped('requisition_line_ids.requisition_id')
            if len(requisitions) > 1:
                names = ', '.join(requisitions.mapped('name'))
                order.requisition_display = f'Multi Orden: {names}'
            else:
                order.requisition_display = requisitions.name if requisitions else ''

    def action_multi_orden(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Multi Orden',
            'res_model': 'multi.orden.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
            }
        }