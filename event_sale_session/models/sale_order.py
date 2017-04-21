# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
    )
    event_session_ids = fields.One2many(
        comodel_name='event.session',
        related='event_id.session_ids',
        readonly=True,
    )
    event_sessions_count = fields.Integer(
        comodel_name='event.session',
        related='event_id.sessions_count',
        readonly=True,
    )
