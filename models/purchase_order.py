from odoo import models, fields, api
from odoo.exceptions import AccessError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    service_status = fields.Selection([
        ('delivered', 'Servicio Finalizado')
    ], string='Estado del Servicio', copy=False)

    is_service_user = fields.Boolean(
        compute='_compute_is_service_user'
    )

    @api.depends_context('uid')
    def _compute_is_service_user(self):
        is_service = self.env.user.has_group('purchase_requisition_extended.group_purchase_service')
        for record in self:
            record.is_service_user = is_service

    def action_set_service_status(self):
        if not self.is_service_user:
            raise AccessError('No tiene permisos para marcar servicios como finalizados.')
        for record in self:
            record.write({'service_status': 'delivered'})
        return True