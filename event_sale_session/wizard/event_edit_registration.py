# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RegistrationEditor(models.TransientModel):
    """"""
    _inherit = "registration.editor"

    @api.model
    def default_get(self, fields):
        res = super(RegistrationEditor, self).default_get(fields)
        if not res.get('sale_order_id'):
            sale_order_id = res.get(
                'sale_order_id',
                self._context.get('active_id')
            )
            res['sale_order_id'] = sale_order_id
        sale_order = self.env['sale.order'].browse(res.get('sale_order_id'))
        registrations = self.env['event.registration'].search([
            ('sale_order_id', '=', sale_order.id),
            (
                'event_ticket_id',
                'in',
                sale_order.mapped('order_line.event_ticket_id').ids
             ),
            ('state', '!=', 'cancel')
        ])
        attendee_list = []
        for so_line in [l for l in sale_order.order_line if l.event_ticket_id]:
            existing_registrations = [
                r for r in registrations
                if r.event_ticket_id == so_line.event_ticket_id
            ]
            for reg in existing_registrations:
                attendee_list.append({
                    'event_id': reg.event_id.id,
                    'event_ticket_id': reg.event_ticket_id.id,
                    'registration_id': reg.id,
                    'name': reg.name,
                    'email': reg.email,
                    'phone': reg.phone,
                    'sale_order_line_id': so_line.id,
                    'session_id': so_line.session_id.id,
                })
            for count in range(int(so_line.product_uom_qty) - len(existing_registrations)):
                attendee_list.append([0, 0, {
                    'event_id': so_line.event_id.id,
                    'session_id': so_line.session_id.id,
                    'event_ticket_id': so_line.event_ticket_id.id,
                    'sale_order_line_id': so_line.id,
                }])
        res['event_registration_ids'] = attendee_list
        res = self._convert_to_write(res)
        return res


class RegistrationEditorLine(models.TransientModel):
    """Event Registration"""
    _inherit = "registration.editor.line"

    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
    )

    @api.multi
    def get_registration_data(self):
        self.ensure_one()
        res = super(RegistrationEditorLine, self).get_registration_data()
        res.update({
                'session_id': self.sale_order_line_id.session_id.id,
             })
        return res
