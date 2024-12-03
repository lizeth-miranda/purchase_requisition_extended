from odoo import models, fields, api

class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'


    estado_linea = fields.Selection([
        ('disponible', 'Disponible'),
        ('parcialmente_asignado', 'Parcialmente Asignado'),
        ('completamente_asignado', 'Completamente Asignado')
    ], string='Estado', compute='_compute_estado_linea', store=True)

    cantidad_asignada = fields.Float(
        string='Cantidad Asignada en OCs',
        compute='_compute_cantidad_asignada',
        store=True
    )

    cantidad_pendiente = fields.Float(
        string='Cantidad Pendiente',
        compute='_compute_cantidad_pendiente',
        store=True
    )

    @api.depends('requisition_id.purchase_ids.order_line.product_qty')
    def _compute_cantidad_asignada(self):
        for line in self:
            cantidad = 0.0
            for purchase in line.requisition_id.purchase_ids:
                for po_line in purchase.order_line:
                    if po_line.product_id == line.product_id and purchase.state != 'cancel':
                        cantidad += po_line.product_qty
            line.cantidad_asignada = cantidad

    @api.depends('product_qty', 'cantidad_asignada')
    def _compute_cantidad_pendiente(self):
        for line in self:
            line.cantidad_pendiente = max(0, line.product_qty - line.cantidad_asignada)

    @api.depends('cantidad_pendiente', 'product_qty')
    def _compute_estado_linea(self):
        for line in self:
            if line.cantidad_pendiente <= 0:
                line.estado_linea = 'completamente_asignado'
            elif line.cantidad_asignada > 0:
                line.estado_linea = 'parcialmente_asignado'
            else:
                line.estado_linea = 'disponible'

    @api.onchange('selected')
    def _onchange_selected(self):
        if self.selected:
            self.cantidad_a_asignar = self.cantidad_pendiente
        else:
            self.cantidad_a_asignar = 0.0