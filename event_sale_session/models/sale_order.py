# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    registration_ids = fields.One2many(
        comodel_name='event.registration',
        inverse_name='sale_order_id',
        string='Attendees',
        readonly=True,
    )


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
    )
    event_sessions_count = fields.Integer(
        comodel_name='event.session',
        related='event_id.sessions_count',
        readonly=True,
    )
    event_session_seats_available = fields.Integer(
        related='session_id.seats_available',
        string='Available Seats',
        readonly=True,
    )
    registration_ids = fields.One2many(
        comodel_name='event.registration',
        inverse_name='sale_order_line_id',
        string='Attendees',
        readonly=True,
    )

    @api.multi
    def write(self, values):
        super(SaleOrderLine, self).write(values)
        for line in self:
            if not line._session_seats_available():
                raise ValidationError(_(
                    "There are sessions with no available seats!\n"
                    "Edit them so you can save the sale order"))

    @api.onchange('product_uom_qty')
    def product_uom_change(self):
        super(SaleOrderLine, self).product_uom_change()
        if not self._session_seats_available():
            self.product_uom_qty = 1.0
            raise UserError(_(
                "Not enough seats. Change quanty or session"))

    @api.multi
    def _session_seats_available(self):
        if self.session_id:
            if self.event_session_seats_available < self.product_uom_qty:
                return False
