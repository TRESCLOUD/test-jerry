# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError  


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def write(self, vals):
        for picking in self:
            if 'invoiced' in vals:
                if not picking.can_edit:
                    raise UserError("El usuario no tiene permisos para usar esta funcionalidad. Consulte con su administrador.")
        return super(StockPicking, self).write(vals)

    def action_change_invoiced(self):
        """Change the invoiced state of the picking."""
        for picking in self:
            if not picking._get_invoiced_payment_state():
                raise ValidationError(
                    "No se puede cambiar el estado de facturado porque no todas las facturas asociadas están pagadas."
                )
            else:
                picking.invoiced = True                

    def _get_invoiced_payment_state(self):
        self.ensure_one()
        sale_orders = self.sale_id or self.origin and self.env['sale.order'].search([('name', '=', self.origin)])
        if not sale_orders:
            return False

        invoices = sale_orders.mapped('invoice_ids').filtered(lambda inv: inv.move_type == 'out_invoice' and inv.state == 'posted')

        if not invoices:
            return False

        # Todas las facturas deben estar pagadas
        return all(inv.payment_state == 'paid' for inv in invoices)

            

    @api.model
    def default_get(self, default_fields):
        data = super(StockPicking, self).default_get(default_fields)
        can_edit = self.env.user.has_group('trescloud_test_jerry.group_verified_detail_delivery')
        data.update({
            'can_edit': can_edit}
        )
        return data

    # ------------------------------------------------------
    # COMPUTE METHODS
    # ------------------------------------------------------

    @api.depends_context('uid')
    def _compute_can_edit_stardard_price(self):
        self.update({'can_edit': self.env.user.has_group('trescloud_test_jerry.group_verified_detail_delivery')})


    invoiced = fields.Boolean(
        string='Invoiced'
    )
    can_edit = fields.Boolean(
        string='Can Edit',
        compute='_compute_can_edit',
    )

