# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'


    def action_show_delivery_details(self):
        self.ensure_one()
        pickings = self._get_related_done_pickings()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Detalle de Entrega',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'views': [
                (self.env.ref('trescloud_test_jerry.stock_picking_inherit_tree_view').id, 'tree'),
                (self.env.ref('trescloud_test_jerry.stock_picking_inherit_view').id, 'form')],
            'domain': [('id', 'in', pickings.ids)],
        }

    def _get_related_done_pickings(self):
        """
            Obtiene todos los despachos en estado hecho de la factura actual.
        """
        self.ensure_one()
        # Obtener los pedidos de venta vinculados a las líneas de la factura
        pickings = self.env['stock.picking']
        sale_orders = self.invoice_line_ids.mapped('sale_line_ids.order_id')
        if sale_orders:
            # De los pedidos de venta, obtener los pickings en estado 'done'
            pickings = sale_orders.mapped('picking_ids').filtered(lambda p: p.state == 'done')
        return pickings

    def _compute_account_picking_count(self):
        """
            Calcula el número de pickings relacionados con la factura actual.
        """
        for move in self:
            move.account_picking_count = len(move._get_related_done_pickings())

    account_picking_count = fields.Integer(
        string='Picking Count',
        compute='_compute_account_picking_count',
    )
