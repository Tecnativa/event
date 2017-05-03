# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo.tests import common
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class EventSaleSession(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(EventSaleSession, cls).setUpClass()
        cls.product_category = cls.env['product.category'].create({
            'name': 'test_cat',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Test product event',
            'type': 'service',
            'event_ok': True,
            'lst_price': 10.0,
            'categ_id': cls.product_category.id,
        })
        cls.event = cls.env['event.event'].create({
            'name': 'Test event',
            'date_begin': datetime.today(),
            'date_end': datetime.today() + timedelta(days=7),
            'seats_availability': 'limited',
            'seats_max': '5',
            'seats_min': '1',
            'event_ticket_ids': [
                (0, 0, {'product_id': cls.product.id, 'name': 'test1'}),
                (0, 0, {'product_id': cls.product.id,
                        'name': 'test2', 'price': 8.0,}),
            ],
        })
        cls.session = cls.env['event.session'].create({
            'name': 'Test session',
            'date': datetime.today() + timedelta(days=1),
            'date_end': datetime.today() + timedelta(days=1),
            'event_id': cls.event.id,
            'start_time': 20.0,
            'end_time': 21.5,
            'seats_availability': cls.event.seats_availability,
            'seats_max': cls.event.seats_max,
            'seats_min': cls.event.seats_min,
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test partner',
        })

    def test_sale(self):
        """ sell event with session """
        sale = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'date_order': datetime.today(),
            'order_line': [
                (0, 0, {
                    'product_id': self.product.id,
                    'event_id': self.event.id,
                    'session_id': self.session.id,
                    'product_uom_qty': 5.0,
                    'event_ticket_id': self.event.event_ticket_ids[0].id,
                }),
            ]
        })
        sale.action_confirm()
        regs = self.env['event.registration'].search([
            ('sale_order_id', '=', sale.id)
        ])
        self.assertTrue(len(regs) > 0)
        for reg in regs:
            self.assertEqual(reg.event_id.id, self.event.id)
            self.assertEqual(reg.session_id.id, self.session.id)
            self.assertEqual(reg.partner_id.id, self.partner.id)
            self.assertEqual(reg.name, self.partner.name)
