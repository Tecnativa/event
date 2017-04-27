# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo import exceptions


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
                raise exceptions.ValidationError(_(
                    "There are sessions with no available seats!\n"
                    "Edit them so you can save the sale order"))

    @api.onchange(
        'product_uom_qty', 'event_id', 'session_id', 'event_ticket_id')
    def product_uom_change(self):
        super(SaleOrderLine, self).product_uom_change()
        if self.session_id:
            if not self._session_seats_available():
                raise exceptions.UserError(_(
                    "Not enough seats. Change quanty or session"))

    def _session_seats_available(self):
        self.ensure_one()
        if self.session_id and self.session_id.seats_availability == 'limited':
            seats = self.event_session_seats_available - self.product_uom_qty
            return True if seats > 0 else False
        else:
            return True
