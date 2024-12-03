from odoo import models, fields, api

class MultiOrdenWizard(models.TransientModel):
    _name = 'multi.orden.wizard'
    _description = 'Wizard de Multi Orden'

    order_id = fields.Many2one(
        'purchase.order',
        string="Orden de Compra",
        required=True
    )
    
    related_lines = fields.Many2many(
        'purchase.requisition.line',
        string="Líneas de Requisición Relacionadas",
        domain="[('requisition_id.state', '=', 'ongoing')]"
    )

    all_lines = fields.Many2many(
        'purchase.requisition.line',
        'wizard_all_lines_rel',
        string="Todo el Material",
        domain="[('requisition_id.state', '=', 'ongoing')]"
    )

    @api.onchange('order_id')
    def onchange_order_id(self):
        if not self.order_id:
            self.related_lines = False
            self.all_lines = False
            return

        existing_lines = self.order_id.order_line.mapped('requisition_line_ids')

        # Material Relacionado
        domain = [
            ('requisition_id.state', '=', 'ongoing'),
            ('estado_linea', 'in', ['disponible', 'parcialmente_asignado']),
            ('cantidad_pendiente', '>', 0),
            ('id', 'not in', existing_lines.ids)
        ]

        existing_products = self.order_id.order_line.mapped('product_id')
        if existing_products:
            domain.extend([
                '|',
                ('product_id', 'in', existing_products.ids),
                ('product_id.name', 'ilike', any(existing_products.mapped('name')))
            ])

        related_lines = self.env['purchase.requisition.line'].search(domain)
        self.related_lines = related_lines

        # Todo el Material
        all_domain = [
            ('requisition_id.state', '=', 'ongoing'),
            ('id', 'not in', existing_lines.ids)
        ]
        all_lines = self.env['purchase.requisition.line'].search(all_domain)
        self.all_lines = all_lines

    def action_process(self):
        self.ensure_one()
        active_page = self._context.get('active_page', 'related')
        lines_to_process = self.related_lines if active_page == 'related' else self.all_lines

        for line in lines_to_process:
            if line.estado_linea == 'completamente_asignado':
                continue

            vals = {
                'order_id': self.order_id.id,
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_qty': line.cantidad_pendiente,
                'product_uom': line.product_uom_id.id,
                'date_planned': fields.Date.today(),
                'requisition_line_ids': [(4, line.id)],
                'price_unit': line.product_id.standard_price,
            }
            self.env['purchase.order.line'].create(vals)

        return {'type': 'ir.actions.act_window_close'}