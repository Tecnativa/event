# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from datetime import datetime, timedelta


class EventEvent(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(EventEvent, cls).setUpClass()
        cls.event = cls.env['event.event'].create({
            'name': 'Test event',
            'date_begin': datetime.today(),
            'date_end': datetime.today() + timedelta(days=7),
            'seats_availability': 'limited',
            'seats_max': '5',
            'seats_min': '1',
        })
        cls.attendee1 = cls.env['event.registration'].create({
            'name': 'Test attendee',
            'event_id': cls.event.id,
            'email': '2CG2xHMd@test.com',
        })
        cls.attendee2 = cls.env['event.registration'].create({
            'name': 'Test attendee',
            'event_id': cls.event.id,
            'email': '2CG2xHMd@test.com',
        })
        cls.attendee3 = cls.env['event.registration'].create({
            'name': 'Test attendee',
            'event_id': cls.event.id,
            'email': '2CG2xHMd@test.com',
        })

    def test_mapped_mails(self):
        """ Scheduled emails must unique """
        self.event.mail_attendees(self.env.ref('event.event_reminder').id)
        self.assertEqual(len(self.env['mail.mail'].search(
            [('email_to', '=', self.attendee1.email),
             ('subject', 'ilike', self.env.ref(
                 'event.event_reminder').subject.partition(' ')[0])])), 1)