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
