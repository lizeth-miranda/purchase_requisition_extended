from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    def make_purchase_order(self, partner_id):
        """Sobreescribe el método que crea la orden de compra"""
        self.ensure_one()
        result = super(PurchaseRequisition, self).make_purchase_order(partner_id)
        
        if not result.get('res_id'):
            return result

        purchase_order = self.env['purchase.order'].browse(result['res_id'])
        purchase_order.order_line.unlink()  # Eliminar líneas creadas por defecto

        # Crear solo las líneas disponibles o parcialmente asignadas
        for requisition_line in self.line_ids:
            if requisition_line.estado_linea == 'completamente_asignado':
                continue

            # Crear línea de orden de compra
            self.env['purchase.order.line'].create({
                'order_id': purchase_order.id,
                'name': requisition_line.product_id.get_product_multiline_description_sale(),
                'product_id': requisition_line.product_id.id,
                'product_uom': requisition_line.product_uom_id.id,
                'product_qty': requisition_line.product_qty,  # Cantidad original
                'price_unit': requisition_line.product_id.standard_price,
                'requisition_line_ids': [(4, requisition_line.id)],
                'date_planned': fields.Date.today(),
            })

        return result
