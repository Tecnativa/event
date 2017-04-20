# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    event_session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
    )
    event_session_ids = fields.One2many(
        comodel_name='event.session',
        related='event_id.session_ids',
        readonly=True,
    )

    # @api.multi
    # def _prepare_invoice_line(self, qty):
    #     self.ensure_one()
    #     res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
    #     if self.event_session_ids:
    #         res['name'] = '%s: %s' % (
    #             res.get('name', ''),
    #             self.event_session_id.name
    #         )
    #     return res
