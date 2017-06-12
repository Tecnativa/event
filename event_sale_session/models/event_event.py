# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EventSession(models.Model):
    _inherit = 'event.event'

    order_line_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='event_id',
        string='Sales Order Lines'
    )
    unconfirmed_qty = fields.Integer(
        string='Unconfirmed Qty',
        compute='_compute_unconfirmed_qty',
        store=True,
    )

    @api.depends('order_line_ids', 'order_line_ids.product_uom_qty',
                 'order_line_ids.order_id.state')
    @api.multi
    def _compute_unconfirmed_qty(self):
        for event in self:
            event.unconfirmed_qty = int(sum(event.order_line_ids.filtered(
                lambda x: x.order_id.state in ('draft', 'sent')
            ).mapped('product_uom_qty')))
